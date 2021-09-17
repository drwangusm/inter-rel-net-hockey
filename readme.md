# Interaction Relational Network
Code used at paper "Interaction Relational Network for Mutual Action Recognition".

See section below for modifications to IRN for Hockey Penalty Dataset.

It contains an implementation of our Interaction Relational Network (IRN), an end-to-end NN tailored for Interaction Recognition using Skeleton information. 

<div align="center">
    <img src="./summary_IRN.png", width="450">
</div>

More details at the preprint: https://arxiv.org/abs/1910.04963

```
@misc{perez2019interaction,
    title={Interaction Relational Network for Mutual Action Recognition},
    author={Mauricio Perez and Jun Liu and Alex C. Kot},
    year={2019},
    eprint={1910.04963},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```

## Contents
1. [Requirements](#requirements)
2. [Reproducing Experiments](#reproducing-experiments)
3. [Results](#results)

## Requirements

Our proposed method Interaction Relational Network (IRN) was implemented on Python, using Keras framework with TensorFlow as backend. Altough we have not tested with other backends, such as Theano, we believe it should not matter.

Software and libraries version:

- Python: 3.6.8
- Keras: 2.2.4
- TensorFlow: 1.14.0

## Reproducing Experiments

### Setting-up the datasets

Each dataset has a different initial setup, because of how they are made available at their respective project web-page, with SBU being the most straightforward to set-up.
Our code assume the data is available at *'data/'* folder at the same directory as *'src/'*, but that can be changed at the hard-coded parameter *DATA_DIR* in the source files at *'src/datasets/'*.

Here are the setup steps per dataset:

- **SBU**
	1. Download dataset from respective [project page](https://www3.cs.stonybrook.edu/~kyun/research/kinect_interaction/index.html) (Clean version)
	1. Unzip all zipped sets at the same folder: *'data/sbu/'*
- **UT**
	1. Download dataset from respective [project page](http://cvrc.ece.utexas.edu/SDHA2010/Human_Interaction.html#Data) (segmented_set1 & segmented_set2)
	1. Run [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to extract skeleton information
	1. Save extracted keypoints at *'data/ut-interaction/'*. Check *'src/datasets/UT.py'* for an explanation on the expected directory structure.
	- **Obs:** Alternatively we provide the skeleton information extracted by us [here](https://drive.google.com/file/d/1gh_1OBjUbfBg2KEmypfZxgmoguoXpRZp/view?usp=sharing)
- **NTU** and **NTU-V2**
	1. Download the skeleton information from the dataset [project page](http://rose1.ntu.edu.sg/datasets/actionrecognition.asp) or at the [github page](https://github.com/shahroudy/NTURGB-D/).
		- 'nturgbd_skeletons_s001_to_s017.zip' and 'nturgbd_skeletons_s018_to_s032.zip'
	1. Run script `src/set-up_ntu_skl.py` to read the skeletons from the zip files and generate a single csv file with all the normalized coordinates.
		- Run first for version 1: `python src/set-up_ntu_skl.py 1`
		- Then for version 2: `python src/set-up_ntu_skl.py 2`
		- **Obs:** These can take several minutes to complete.
	1. Run script `src/set-up_ntu_skl.py` with `-c` option to convert csv files to npy (faster to read).
		- Ex: `python src/set-up_ntu_skl.py 1 -c` and `python src/set-up_ntu_skl.py 2 -c`
		- **Obs:** These can take several minutes to complete.

If the data is obtained in a different way, or is stored at a different format,
it is necessary to adapt the code at *'src/datasets'* and *'src/misc/data_io.py'*.

### Running the code

Our experiments hyperparameters are stored in the configuration files at folder *'configs/'*, so to reproduce our experiments is only necessary to setup the datasets and run the script `run_protocol.py` with the adequate configuration files.

How to use `run_protocol.py`:

```
python src/run_protocol.py EXPERIMENT_NAME \
	configs/DATASET/EXPERIMENT_NAME.cfg \
	DATASET \
	[OPTIONS]
```

Usage examples:

```
python src/run_protocol.py IRN_inter \
	configs/SBU/IRN_inter.cfg SBU

python src/run_protocol.py IRN_inter+intra \
	configs/SBU/IRN_inter+intra.cfg SBU -F middle

python src/run_protocol.py LSTM-IRN_inter \
	configs/SBU/LSTM-IRN_inter.cfg SBU -t

python src/run_protocol.py LSTM-IRN_inter+intra \
	configs/SBU/LSTM-IRN_inter+intra.cfg SBU -t -F middle

python src/run_protocol.py LSTM-IRN_inter \
	configs/NTU-V1/LSTM-IRN_inter.cfg NTU -t -f cross_subject
```

Models and results will be saved at folder: *'models/DATASET/EXPERIMENT_NAME/'*. Use script `misc/print_train_stats.py` to print the results stored at the expreriment folder. Usage examples:

```
python src/misc/print_train_stats.py models/SBU/* -c val_accuracy

python src/misc/print_train_stats.py models/NTU/LSTM-IRN_inter/fold_cross_subject/ \
	models/NTU/LSTM-IRN_inter/fold_cross_view/ 
```

## Results

Results from some of our proposed methods on the following datasets:

### SBU

Method | Accuracy
------------ | -------------
LSTM-IRN_inter | 94.6%
LSTM-IRN_intra | 95.2%
LSTM-IRN-fc1_inter+intra | 98.2%

### UT

Method | Set 1 | Set 2
------------ | ------------- | -------------
LSTM-IRN_inter | 93.3% | 96.7%
LSTM-IRN_intra | 96.7% | 91.7%
LSTM-IRN-fc1_inter+intra | 98.3% | 96.7%

### NTU V1

Method | Cross-Subject | Cross-View
------------ | ------------- | -------------
LSTM-IRN_inter | 89.5% | 92.8%
LSTM-IRN_intra | 87.3% | 91.7%
LSTM-IRN-fc1_inter+intra | 90.5% | 93.5%

Obs: Mutual actions only

### NTU V2

Method | Cross-Subject | Cross-Setup
------------ | ------------- | -------------
LSTM-IRN_inter | 74.3% | 75.6%
LSTM-IRN_intra | 73.6% | 75.2%
LSTM-IRN-fc1_inter+intra | 77.7% | 79.6%

Obs: Mutual actions only

# IRN Modifications for Hockey Dataset

Several key modifications were made to the original IRN Model. All parameters for these modifications can be set in the `configs` files. Examples of usage can be found in `configs/YMJA`. Additional metrics were added including recall, precision, and F1. 
## Configuration Options
The model will revert to the default if the option is not specified in the configuration file.
* `data` section
	* `arch = 'joint' | 'temp | joint_lstm | temp_lstm'` - Default: None
		* This sets the architecture to use the new `joint` objects or `temp` objects. If this is set, the `rel_type` option in the `model` section must be set to `joint_stream` or `temp_stream` respectively. Removing this option can be used to test the original paper's models.
* `model` section
	* `rel_type = 'joint_stream' | 'temp_stream'`
		* This can normally be set to `indivs` for the paper's original models but if `arch` is set above, this also must be set correctly.
	* `use_attention = True | False` - Default: False
		* Whether to use attention or not after the _g_ layer. This has only been tested on the `joint_stream` and `temp_stream`.
	* `use_relations = True | False` - Default: True
		* Whether to use relations (feed pairs of objects into the _g_ layer). Relations are used by the paper by default. Removing relations basically means that only a single object is fed into each _g_ module instead of a pair of objects.
	* `projection_size = <Int>` - Default: None
		* This sets the output size of the first dense layer in the attention module. If it is not specified, the model will set it automatically to the size of the objects inputted. This is only useful with the attention enabled.
	* `return_attention = True | False` - Default: False
		* If set to true, the attention vectors are written to in `models/<model>/fold_X/rerun_X/attention.csv`. Each line corresponds to an attention vector for a single prediction generated at the end on the validation set once the model has already been trained. For instance, for the joint attention with no relations, 25 objects will be outputted each representing the attention for a single joint. The `view_att.py` script can be used to generate an average attention vector for each true prediction class. 
		* To see the order of the objects, (specifically for OpenPose), see `src/misc/data_io.py` and see the `POSE_BODY_25_BODY_PARTS` variable.
		* It is recommended to use this with `no_relations = False` because otherwise, attention is returned for each pair of objects. 
* `fusion` section
	* Make sure to set the `config_filepaths` and `weights_filepahts` variables corectly. Note that the individual streams specified in the config and weight filepaths must be trained _**before**_ training the fused model.
	* `new_arch = True | False` - Default: False 
		* For the fused `joint` and `temporal` stream, this should be set to True. Otherwise, for the paper's original fused models, this can be set to false.
	* `avg_at_end = True | False` - Default: False
		* If set to true, this does not fuse both streams after the _g_ layer and instead averages the outputs after the _f_ layer.
		* This has only been tested with the joint and temporal streams.
## Running the Models
### YMJA Dataset
* For all other datasets, follow the author's guide on how to load them. For the YMJA dataset, follow the instructions for how to use the data collection pipeline to generate the JSON files for each clip. Note that the number of timesteps in the configuration file should be set to the number of frames outputted in the last step of the pipeline process. Place the output in `data`. The structure of the directory should look like `data/YMJA/<Penalty Class>/<clip_name>.json`. See the `src/datasets/YMJA.py` for more details.
* Note that if a model has started running and has finished a run or a fold, the progress will be saved at that fold. If a model has finished training, trying to rerun the script with the specific model name (as the output file) will only print the results from the output file.
### Running the Scripts
* Examples for how to run the SBU scripts are in the `run_tests.sh` file and for how to run the YMJA scripts are in the `run_tests_ymja.sh`. Make sure that all dependencies are correctly installed. See the author's guide on which dependencies are required above. Alternatively, use conda to install the dependencies from `requirements.txt` into your environment.
## Overview of Modifications
* New Object Streams
	* There are two new formats for the objects that are inputted into each _g_ module. The `joint` stream groups a single joint from both persons into a single object across all timeframes. For instance, it could include the left elbows of both persons across all frames. Thus, the number of objects is the total number of joints. The `temporal` stream groups all joints for all players within a single frame in a single object. Thus, the number of objects is the total number of frames. 
	* For more information on the structure of each object, this is set in the `src/misc/data_io.py` at the bottom.
	* For more information on how the individuals in these objects are shuffled (normally set to true in most configuration files), see `src/datasets/data_generator.py`.
	* For information on how this affects the structure of the model, see `src/models/rn.py`.
* Attention Module
	* The code for this can be found in `src/models/attention.py`. It adds a custom Keras layer which serves as the attention module between the _g_ and _f_ layer. The attention module is applied to each pair of objects at the end of the _g_ layer. This has only been tested on the joint and temporal stream.
* Averaging at End
	* The code for this can be found in `src/models/rn.py`. Instead of fusing the individual streams before the _f_ layer, it averages the output of each stream's _f_ layer at the end of the layer. This has only been tested on the joint and temporal stream.
* No Relations
	* The code for this can be found in `src/models/rn.py`. Instead of inputting a pair of objects into each _g_ layer, only individual objects are inputted into the layer. For instance, for the joint stream, this would mean that each object would just be a single joint (for a total of 25 joints). 

## Other Notes

Here are some key modifications made to each file.
* `src/train_rn.py`
	* Made modifications to correctly load the configuration files for the joint and temporal stream. Also made modifications to support returning attention and printing the attention to the `attention.csv` file.
	* Made modifications to the way that the `training.log` file is saved for each model/fold_X/rerun_x. The issue arises because of the fact that when we return attention, the model will have two outputs (the original output and the attention weights). This causes Tensorflow to rename the default metrics that are outputted. These metrics however are used in order to identify the best-performing epoch. In order to fix this, we read from the `training.log` file and replace the column names (the metrics) after finishing training.
* `src/models/rn.py`
	* Made modifications to support joint and temporal stream objects and fusion of joint and temporal stream. Add support for attention module and returning attention weights. Made modifications to support when the no relations option is used. Made modifications to support averaging at end. Note that by default, if relations are used with the joint/temporal stream object, the `'p1_p1_all'` relationship is used. This is because we only want relations to be established within the joint or temporal stream objects and not between the joint and temporal stream objects. This is similar in nature to the intra-person relationships from the original model. This creates relationships between each joint object (joint_i, joint_j) and each temporal object (frame_i, frame_j). 
	* For the no relations option, we do not use any of the relationships and instead input an individual object (joint_i or frame_i) directly into the g_theta layer. 
	* For the averaging at end option, in the `fuse_rn` method, we do not prune the f-layer (unlike the other fused models). Instead, we keep the f-layer from both models that are being averaged and average the outputs at the end.
* `src/models/attention.py`
	* New Keras layer for attention module to insert between _g_ and _f_ layer.
* `src/data_io.py`
	* This is where the joint and temporal object formats are defined. Modifications are also made to support loading from the YMJA dataset.
* `src/datasets/YMJA.py`
	* This file is added to support the YMJA dataset. In this file, the `FOLD_MECH` variable can be set to either `'Uniform'` or `'Random'`. This defines how the folds are created. For Uniform, the five folds are uniformly distributed across the penalty classes. Thus, each fold will have more or less the same distribution. For Random, the fold distributions are selected randomly. All tests that are currently there are run in Uniform mode.
* `src/datasets/data_generator.py`
	* Modified shuffling mechanism so that it works on joint stream and temporal stream objects. The shuffling mechanism randomly shuffles the individuals in each batch so person 1 might be randomly switched with person 2 in some samples in each batch. The structure of the objects do not otherwise change (the joints or frames themselves are **NOT** shuffled).

