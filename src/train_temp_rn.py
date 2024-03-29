import numpy as np
import argparse, sys, os, time
import progressbar

from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping, CSVLogger
    
from datasets import UT, NTU_V2, SBU, NTU, YMJA
from datasets.data_generator import DataGeneratorSeq
from models.temporal_rn import get_model, get_fusion_model
from misc.utils import read_config
from train_rn import set_callbacks, train_model

np.random.seed(42)

#%% Functions
def load_args():
    ap = argparse.ArgumentParser(
        description='Train Relational Network.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # Positional arguments
    ap.add_argument('output_path',
        help='path to output the model snapshots and log',
        type=str)
    
    # Data arguments
    ap.add_argument('-d','--dataset-name',
        help="dataset to be used for training",
        default='UT',
        choices=['UT', 'SBU', 'NTU_V2', 'NTU'])
    ap.add_argument('-f','--dataset-fold',
        help="dataset fold to be used for training",
        default=9,
        type=int)
    ap.add_argument('-t', '--timesteps',
        type=int,
        default=16,
        help='how many timesteps to use')
    
    # Training arguments
    ap.add_argument('-l', '--learning-rate',
        type=float,
        default=1e-4,
        help='learning rate for training')
    ap.add_argument('-r', '--drop-rate',
        type=float,
        default=0.3,
        help='dropout rate for training')
    ap.add_argument('-b', '--batch-size',
        type=int,
        default=32,
        help='batch size used to train')
    ap.add_argument('-G', '--gpus',
        type=int,
        default=1,
        help='number of gpus to use')
    ap.add_argument('-e', '--epochs',
        type=int,
        default=20,
        help='number of epochs to train')
    ap.add_argument('-c', '--checkpoint-period',
        type=int,
        default=100,
        help='interval (number of epochs) between checkpoints')
    
    ap.add_argument('--print_args',
        help="whether to print current arguments' values",
        action='store_true')
    
    args = ap.parse_args()
    
    return args

def train_temp_rn(output_path, dataset_name, model_kwargs, data_kwargs,
        dataset_fold=None, drop_rate=0.1, 
        batch_size=32, epochs=100, checkpoint_period=5, learning_rate=1e-4, 
        kernel_init_type='TruncatedNormal', kernel_init_param=0.045, kernel_init_seed=None,
        subsample_ratio=None, gpus=1, verbose=2, use_data_gen=True):
    if verbose > 0:
        print("***** Training parameters for train_temp_rn *****")
        print("\t Output path:", output_path)
        print("\t Dataset:", dataset_name)
        print("\t Dataset fold:", dataset_fold)
        print("\t Skeleton info")
        for key, value in data_kwargs.items():
            print("\t > {}: {}".format(key, value))  
        print("\t Model info")
        for key, value in model_kwargs.items():
            print("\t > {}: {}".format(key, value))
        print("\t Kernel Init info")
        print("\t > kernel_init_type:", kernel_init_type)
        print("\t > kernel_init_param:", kernel_init_param)
        print("\t > kernel_init_seed:", kernel_init_seed)
        print("\t Training options")
        print("\t > Batch Size:", batch_size)
        print("\t > Epochs:", epochs)
        print("\t > Checkpoint Period:", checkpoint_period)
        print("\t > Learning Rate:", learning_rate)
        print("\t > Dropout rate:", drop_rate)
        print("\t > Training Subsample Ratio:", subsample_ratio)
    
    buffer_data = False
    if dataset_name == 'UT':
        dataset = UT
        buffer_data = True # Dataset is too small, reading all data at once is better
    elif dataset_name == 'SBU':
        dataset = SBU
    elif dataset_name == 'YMJA':
        dataset = YMJA
    elif dataset_name == 'NTU':
        dataset = NTU
        use_data_gen = True # Unable to read all data at once, dataset too big.
    
    if verbose > 0:
        print("Reading data...")
    
    timesteps = data_kwargs['timesteps']
    add_joint_idx = data_kwargs['add_joint_idx']
    add_body_part = data_kwargs['add_body_part']
    
    if use_data_gen:
        if verbose > 0:
            print("> Using DataGenerator")
        train_generator = DataGeneratorSeq(dataset_name, dataset_fold, 'train',
                batch_size=batch_size, reshuffle=True, shuffle_indiv_order=True, 
                pad_sequences=True, buffer_data=buffer_data, **data_kwargs)
        val_generator = DataGeneratorSeq(dataset_name, dataset_fold, 'validation',
                batch_size=batch_size, reshuffle=False, shuffle_indiv_order=False,
                pad_sequences=True, buffer_data=buffer_data, **data_kwargs)
        X_train, Y_train = train_generator[0]
        X_val, Y_val = val_generator[0]
        
        train_data = train_generator
        val_data = val_generator
    else: # Not implemented for seqs, padding is done by generator only
        if verbose > 0:
            print("> Reading all data at once")
        X_train, Y_train = dataset.get_train(dataset_fold, **data_kwargs)
        X_val, Y_val = dataset.get_val(dataset_fold, **data_kwargs)
        
        train_data = [X_train, Y_train]
        val_data = [X_val, Y_val]



    if 'arch' not in list(data_kwargs.keys()):

        _, seq_len, num_joints, *object_shape = np.array(X_train).shape
        num_joints = num_joints//2
        num_objs = num_joints
        object_shape = tuple(object_shape)
        output_size = len(Y_train[0])
        overhead = add_joint_idx + add_body_part # True/False = 1/0
        num_dim = (object_shape[0]-overhead)//timesteps

    elif data_kwargs['arch'] == 'joint-lstm':
        _, seq_len, num_joints, *object_shape = np.array(X_train).shape
        num_objs=num_joints
        object_shape = tuple(object_shape)
        output_size = len(Y_train[0])
        overhead = add_joint_idx + add_body_part # True/False = 1/0
        num_dim = (object_shape[0]-overhead)//timesteps

    elif data_kwargs['arch'] == 'temp-lstm':

        num_ppl = 2
        num_coord = 3
        if dataset_name == 'UT':
            num_coord = 2
        _, seq_len, num_frames, *object_shape = np.array(X_train).shape
        num_joints = object_shape[0]//(num_ppl * num_coord)
        num_objs = num_frames
        object_shape = tuple(object_shape)
        output_size = len(Y_train[0])
        overhead = add_joint_idx + add_body_part # True/False = 1/0
        #todo what does this do?
        num_dim = (object_shape[0]-overhead)//num_joints
    
    if verbose > 0:
        print("Creating model...")

    # if(model_kwargs['rel_type'] == 'joint_stream' or model_kwargs['rel_type'] == 'temp_stream'):
    #     num_joints = len(X_train)

    model = get_model(num_objs=num_objs, object_shape=object_shape,
        output_size=output_size, num_dim=num_dim, overhead=overhead,
        kernel_init_type=kernel_init_type, kernel_init_param=kernel_init_param, 
        kernel_init_seed=kernel_init_seed, drop_rate=drop_rate, seq_len=seq_len,
        **model_kwargs)

    return_attention = False
    if 'return_attention' in model_kwargs:
        return_attention = model_kwargs['return_attention']
    
    fit_history = train_model(model=model, verbose=verbose, learning_rate=learning_rate, 
        output_path=output_path, checkpoint_period=checkpoint_period, 
        batch_size=batch_size, epochs=epochs, use_data_gen=use_data_gen, 
        train_data=train_data, val_data=val_data, subsample_ratio=subsample_ratio,  return_attention=return_attention)
    
    return fit_history

def train_fused_temp_rn(output_path, dataset_name, dataset_fold,
        config_filepaths, weights_filepaths,
        batch_size=32, epochs=100, checkpoint_period=5, learning_rate=1e-4, 
        drop_rate=0.1, freeze_g_theta=False, fuse_at_fc1=False, new_arch=False, avg_at_end=False,
        initial_epoch=0, initial_weights=None, use_data_gen = True,
        subsample_ratio=None,
        gpus=1,verbose=2):
    
    data_kwargs, _, _ = read_config(config_filepaths[0])
    if new_arch:
        data_kwargs['arch'] = 'lstm_joint_temp_fused'
    
    if verbose > 0:
        print("***** Training parameters for train_fused_temp_rn *****")
        print("\t Output path:", output_path)
        print("\t Dataset:", dataset_name)
        print("\t Dataset fold:", dataset_fold)
        print("\t Fusion info")
        print("\t > config_filepaths:", config_filepaths)
        print("\t > weights_filepaths:", weights_filepaths)
        print("\t > freeze_g_theta:", freeze_g_theta)
        print("\t > fuse_at_fc1:", fuse_at_fc1)
        print("\t > New architecture:", new_arch)
        print("\t Training options")
        print("\t > Batch Size:", batch_size)
        print("\t > Epochs:", epochs)
        print("\t > Checkpoint Period:", checkpoint_period)
        print("\t > Learning Rate:", learning_rate)
        print("\t > Dropout rate:", drop_rate)
        print("\t > Training Subsample Ratio:", subsample_ratio)
        print("\t GPUs:", gpus)
        print("\t Skeleton info")
        for key, value in data_kwargs.items():
            print("\t > {}: {}".format(key, value))
    
    use_earlyStopping = True
    if dataset_name == 'UT':
        dataset = UT
        use_earlyStopping = False
    elif dataset_name == 'SBU':
        dataset = SBU
    #todo add NTU
    # elif dataset_name == 'NTU':
    #     dataset = NTU
    
    if verbose > 0:
        print("Reading data...")
    
    if use_data_gen:
        if verbose > 0:
            print("> Using DataGenerator")
        train_generator = DataGeneratorSeq(dataset_name, dataset_fold, 'train',
                batch_size=batch_size, new_arch=new_arch, reshuffle=True, shuffle_indiv_order=True,
                pad_sequences=True, **data_kwargs)
        val_generator = DataGeneratorSeq(dataset_name, dataset_fold, 'validation',
                batch_size=batch_size, new_arch=new_arch, reshuffle=False, shuffle_indiv_order=False,
                pad_sequences=True, **data_kwargs)

        #todo changes here: are they list in non-lstm version too?
        X_train, Y_train = train_generator[0]
        X_val, Y_val = val_generator[0]
        train_data = train_generator
        val_data = val_generator
    else:
        if verbose > 0:
            print("> Reading all data at once")
        X_train, Y_train = dataset.get_train(dataset_fold, **data_kwargs)
        X_val, Y_val = dataset.get_val(dataset_fold, **data_kwargs)
        train_data = [X_train, Y_train]
        val_data = [X_val, Y_val]

    models_kwargs = []

    if new_arch:

        check_configs = []
        for config_filepath in config_filepaths:
            data_kwargs, model_kwargs, train_kwargs = read_config(config_filepath)
            check_configs.append(model_kwargs)

        # Ensure that temporal stream and joint stream both included. Reorder if necessary so that joint stream first.
        if(len(check_configs) != 2):
            print("Error: Expecting Joint Stream and Temporal Stream")
            exit(0)

        # Should reorder both weights and config.
        if(check_configs[0]['rel_type'] == 'temp_stream'):
            config_filepaths.reverse()
            weights_filepaths.reverse()

        check_configs = []
        for config_filepath in config_filepaths:
            data_kwargs, model_kwargs, train_kwargs = read_config(config_filepath)
            check_configs.append(model_kwargs)

        # Ensure that both joint and temporal stream exist
        if(check_configs[0]['rel_type'] != 'joint_stream' or check_configs[1]['rel_type'] != 'temp_stream'):
            print("Error: Expecting Joint Stream and Temporal Stream")
            exit(0)

        # Ensure X_train has two components
        if(len(X_train) != 2):
            print("Error: Expecting X_train to consist of both joint and temporal components")
            exit(0)
        #todo this change
        for config_filepath, X_train_comp in zip(config_filepaths, X_train):

            #todo was this correct for before two_stream?
            _, seq_len, num_joints_or_frames, *object_shape = np.array(X_train_comp).shape
            object_shape = tuple(object_shape)
            output_size = len(Y_train[0])

            data_kwargs, model_kwargs, train_kwargs = read_config(config_filepath)
            timesteps = data_kwargs['timesteps']
            add_joint_idx = data_kwargs['add_joint_idx']
            add_body_part = data_kwargs['add_body_part']
            overhead = add_joint_idx + add_body_part # True/False = 1/0
            num_dim = (object_shape[0]-overhead)//num_joints_or_frames
            model_kwargs['num_dim'] = num_dim
            model_kwargs['overhead'] = overhead
            model_kwargs['num_objs'] = num_joints_or_frames
            model_kwargs['object_shape'] = object_shape

            models_kwargs.append(model_kwargs)

    else:

        #todo was this correct for before two_stream?
        _, seq_len, num_joints, *object_shape = np.array(X_train).shape
        num_joints = num_joints//2
        object_shape = tuple(object_shape)
        output_size = len(Y_train[0])

        for config_filepath in config_filepaths:
            data_kwargs, model_kwargs, train_kwargs = read_config(config_filepath)
            timesteps = data_kwargs['timesteps']
            add_joint_idx = data_kwargs['add_joint_idx']
            add_body_part = data_kwargs['add_body_part']
            overhead = add_joint_idx + add_body_part # True/False = 1/0
            num_dim = (object_shape[0]-overhead)//timesteps
            model_kwargs['num_dim'] = num_dim
            model_kwargs['overhead'] = overhead
            model_kwargs['num_objs'] = num_joints
            model_kwargs['object_shape'] = object_shape
            models_kwargs.append(model_kwargs)
    
    train_kwargs['drop_rate'] = drop_rate

    for mod_kwargs in models_kwargs:
        mod_kwargs['return_attention'] = False

    if verbose > 0:
        print("Creating model...")
        #todo object shape can vary
    model = get_fusion_model(new_arch, output_size, seq_len,
        train_kwargs, models_kwargs, weights_filepaths, 
        freeze_g_theta=freeze_g_theta, fuse_at_fc1=fuse_at_fc1, avg_at_end=avg_at_end)
    
    if initial_weights is not None:
        model.load_weights(initial_weights)
    
    fit_history = train_model(model=model, verbose=verbose, learning_rate=learning_rate, 
        output_path=output_path, checkpoint_period=checkpoint_period, 
        batch_size=batch_size, epochs=epochs, use_data_gen=use_data_gen, 
        train_data=train_data, val_data=val_data, subsample_ratio=subsample_ratio,
        use_earlyStopping=use_earlyStopping)
    
    return fit_history
    
#%% Main
if __name__ == '__main__':
    args = vars(load_args())

    print('> Starting Train RN - ', time.asctime( time.localtime(time.time()) ))

    print_args = args.pop('print_args')
    if print_args:
        print("Program arguments and values:")
        for argument, value in args.items():
            print('\t', argument, ":", value)
    
    train_temp_rn(**args)

    print('\n> Finished Train RN -', time.asctime( time.localtime(time.time()) ))
