import keras
from keras import backend as K
import numpy as np
import tensorflow as tf

# credits to https://github.com/fizyr/keras-retinanet/blob/01737e6523c09df922d36edac332a68bcda4af90/keras_retinanet/callbacks/common.py
class RedirectModel(keras.callbacks.Callback):
    """Callback which wraps another callback, but executed on a different model.
    ```python
    model = keras.models.load_model('model.h5')
    model_checkpoint = ModelCheckpoint(filepath='snapshot.h5')
    parallel_model = multi_gpu_model(model, gpus=2)
    parallel_model.fit(X_train, Y_train, callbacks=[RedirectModel(model_checkpoint, model)])
    ```
    Args
        callback : callback to wrap.
        model    : model to use when executing callbacks.
    """

    def __init__(self,
                 callback,
                 model):
        super(RedirectModel, self).__init__()

        self.callback = callback
        self.redirect_model = model

    def on_epoch_begin(self, epoch, logs=None):
        self.callback.on_epoch_begin(epoch, logs=logs)

    def on_epoch_end(self, epoch, logs=None):
        self.callback.on_epoch_end(epoch, logs=logs)

    def on_batch_begin(self, batch, logs=None):
        self.callback.on_batch_begin(batch, logs=logs)

    def on_batch_end(self, batch, logs=None):
        self.callback.on_batch_end(batch, logs=logs)

    def on_train_begin(self, logs=None):
        # overwrite the model with our custom model
        self.callback.set_model(self.redirect_model)

        self.callback.on_train_begin(logs=logs)

    def on_train_end(self, logs=None):
        self.callback.on_train_end(logs=logs)


class Evaluate(keras.callbacks.Callback):
    def __init__(
        self,
        generator,
        mode,
        verbose=1
    ):
        """ Evaluate a given dataset using a given model at the end of every epoch during training.
        """
        self.generator       = generator
        self.mode = mode
        self.verbose         = verbose

        super(Evaluate, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        print("\nevaluating model!\n")

        metrics = self.model.evaluate_generator(self.generator, steps=None, max_queue_size=10, workers=8)
        print(f'\n\nmetrics is {metrics}\n\n')
