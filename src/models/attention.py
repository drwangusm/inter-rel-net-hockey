import keras
import keras.backend as K
import tensorflow as tf
import tensorflow.nn as nn
import numpy as np

#first version of attention model

class IRNAttention(keras.layers.Layer):
    def __init__(self, num_head=1, projection_size=None, return_attention=False, **kwargs):
        self.return_attention = return_attention
        self.projection_size = projection_size
        self.num_head = num_head
        super(IRNAttention, self).__init__(**kwargs)

    def build(self, input_size):
        if self.projection_size is None:
            self.projection_size = input_size[0][1] # size of joint object

        #todo add another layer
        #todo add bias

        self.w1=self.add_weight(name="Att1", shape=(input_size[0][1], self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        self.w2=self.add_weight(name="Att2", shape=(self.projection_size, 1), initializer="normal")

        super(IRNAttention, self).build(input_size)

    def call(self, inputs):

        inputs = tf.transpose(tf.stack(inputs), perm=[1,0,2])
        e = K.tanh(K.dot(inputs,self.w1))
        e2 = K.dot(e, self.w2)
        a = K.softmax(e2, axis=1)
        output = inputs*a
        ##return the ouputs. 'a' is the set of attention weights
        ##the second variable is the 'attention adjusted o/p state' or context
        sentence = K.sum(output, axis=1)
        attention = a
        if self.return_attention:
            return [sentence, attention]
        else:
            return (sentence)

    def get_config(self):
        config = super(IRNAttention, self).get_config()
        config.update({"num_head": self.num_head,
                       "projection_size": self.projection_size,
                       "return_attention": self.return_attention})
        return config

'''
#this is the second version of self-attention ==> doesn't work well

class IRNAttention(keras.layers.Layer):
    def __init__(self, num_head=1, projection_size=None, return_attention=False, **kwargs):
        self.return_attention = return_attention
        self.projection_size = projection_size
        self.num_head = num_head
        super(IRNAttention, self).__init__(**kwargs)

    def build(self, input_size):
        self.num_obj = len(input_size)
        if self.projection_size is None:
            self.projection_size = input_size[0][1]*self.num_obj
        # size of joint object

        #todo add another layer
        #todo add bias

        self.w1=self.add_weight(name="Att1", shape=((input_size[0][1]*self.num_obj), self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        self.w2=self.add_weight(name="Att2", shape=(self.projection_size, self.num_obj), initializer="normal")

        super(IRNAttention, self).build(input_size)

    def call(self, inputs):

        inputs = tf.transpose(tf.stack(inputs), perm=[1,0,2])
        inputs_concat = tf.stack([tf.reshape(inputs, [-1,inputs.shape[1]*inputs.shape[2]])], axis=1)
        e = K.tanh(K.dot(inputs_concat,self.w1))
        e2 = K.dot(e, self.w2)
        a = K.softmax(e2, axis=2)
        a = tf.transpose(a, perm=[0,2,1])
        # a = tf.stack([a], axis=1)
        output = inputs*a
        ##return the ouputs. 'a' is the set of attention weights
        ##the second variable is the 'attention adjusted o/p state' or context
        sentence = K.sum(output, axis=1)
        attention = a
        if self.return_attention:
            return [sentence, attention]
        else:
            return (sentence)

    def get_config(self):
        config = super(IRNAttention, self).get_config()
        config.update({"num_head": self.num_head,
                       "projection_size": self.projection_size,
                       "return_attention": self.return_attention})
        return config
    
'''