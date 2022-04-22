from __future__ import print_function
import keras
import keras.backend as K
import tensorflow as tf
from keras.layers import Dropout

import tensorflow.nn as nn
import numpy as np

class IRNAttentionMLP(keras.layers.Layer):
    def __init__(self, num_head=1, projection_size=None, return_attention=False, **kwargs):
        self.return_attention = return_attention
        self.projection_size = projection_size
        self.num_head = num_head
        super(IRNAttentionMLP, self).__init__(**kwargs)

    '''
    att_weights = input -> w1 (-, proj_size) -> tanh -> w2 (proj_size, proj_size) -> softmax
    '''
    def build(self, input_size):
        if self.projection_size is None:
            self.projection_size = input_size[0][1] # size of joint object

        #todo add another layer
        #todo add bias

        self.w1=self.add_weight(name="Att1", shape=(input_size[0][1], self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        self.w2=self.add_weight(name="Att2", shape=(self.projection_size, 1), initializer="normal")

        super(IRNAttentionMLP, self).build(input_size)

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
        config = super(IRNAttentionMLP, self).get_config()
        config.update({"num_head": self.num_head,
                       "projection_size": self.projection_size,
                       "return_attention": self.return_attention})
        return config


#this is transformer attention: latest for parameter search

class IRNAttentionTrans(keras.layers.Layer):
    def __init__(self, num_head=1, projection_size=None, return_attention=False, motion=None, **kwargs):
        self.return_attention = return_attention
        self.projection_size = projection_size
        self.num_head = num_head
        # self.motion = motion

        super(IRNAttentionTrans, self).__init__(**kwargs)
        '''
        query_n = inputs * 1 (Q_i)
        key_n = inputs + 0 (K_i)
        values = inputs / 1 (V)
        
        Q -> dot(query_n * w1 (-, proj_size))
        K -> dot(key_n * w2 (-, proj_size))
        temper = sqrt(proj_size)
        attn = Matmul(Q, K) -> softmax -< dropout
        output= Matmul(att, V)
        att_weights = dot(output, w4(proj_size, 1) -> softmax      
        '''

    def build(self, input_size):
        if self.projection_size is None:
            # self.projection_size = input_size[0][1] # size of joint object
            self.projection_size = 500

        # self.w1=self.add_weight(name="Att1", shape=(input_size[0][1], self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        # self.w2=self.add_weight(name="Att2", shape=(input_size[0][1], self.projection_size), initializer="normal")
        # # self.w3=self.add_weight(name="Att3", shape=(input_size[0][1], self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        # self.w4=self.add_weight(name="Att4", shape=(self.projection_size, 1), initializer="normal")

        initializer_l = tf.initializers.random_uniform(minval=-0.05, maxval=0.05, seed=None)
        self.w1=self.add_weight(name="Att1", shape=(input_size[0][1], self.projection_size), initializer=initializer_l) #name property is useful for avoiding RuntimeError: Unable to create link.
        self.w2=self.add_weight(name="Att2", shape=(input_size[0][1], self.projection_size), initializer=initializer_l)
        # self.w3=self.add_weight(name="Att3", shape=(input_size[0][1], self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        self.w4=self.add_weight(name="Att4", shape=(self.projection_size, 1), initializer=initializer_l)

        super(IRNAttentionTrans, self).build(input_size)

    def call(self, inputs):

        inputs = tf.transpose(tf.stack(inputs), perm=[1,0,2])
        query_n = inputs * 1
        key_n = inputs + 0
        values = inputs / 1

        # query = K.tanh(K.dot(query_n,self.w1))
        # key = K.tanh(K.dot(key_n,self.w2))
        query = K.sigmoid(K.dot(query_n,self.w1))
        key = K.sigmoid(K.dot(key_n,self.w2))
        temper = tf.sqrt(tf.cast(self.projection_size, dtype='float32'))
        attn1 = tf.matmul(query, tf.transpose(key, perm=[0,2,1])) /temper
        attn_nod = K.softmax(attn1, axis=2)
        # attn_nod = K.print_tensor(attn_nod)
        # K.get_value(attn_nod[0,0,0])
        attn = Dropout(0.1)(attn_nod)
        output = tf.matmul(attn, values)
        # sentence = K.sum(output, axis=1)

        #here apply the self-attention mechansim we had before
        # e = K.tanh(K.dot(output,self.w3))
        #e2 = K.dot(e, self.w4)
        #e2 = K.tanh(K.dot(output,self.w4))
        e2 = (K.dot(output,self.w4))
        # e2 = K.relu(e22)
        a = K.softmax(e2, axis=1)
        new_output = inputs*a
        ##return the ouputs. 'a' is the set of attention weights
        ##the second variable is the 'attention adjusted o/p state' or context
        sentence = K.sum(new_output, axis=1)
        attention = a


        if self.return_attention:
            return [sentence, attention]
        else:
            return (sentence)

    def get_config(self):
        config = super(IRNAttentionTrans, self).get_config()
        config.update({"num_head": self.num_head,
                       "projection_size": self.projection_size,
                       "return_attention": self.return_attention})
        return config

#this is the second version of self-attention ==> doesn't work well

class IRNAttentionExtended(keras.layers.Layer):
    def __init__(self, num_head=1, projection_size=None, return_attention=False, **kwargs):
        self.return_attention = return_attention
        self.projection_size = projection_size
        self.num_head = num_head
        super(IRNAttentionExtended, self).__init__(**kwargs)
        '''
        input (objects, dim_size) => concat objects
        input -> w1 (-, proj_size) -> tanh -> w2 (proj_size, num_objs) -> softmax   
        '''

    def build(self, input_size):
        self.num_obj = len(input_size)
        if self.projection_size is None:
            self.projection_size = input_size[0][1]*self.num_obj
        # size of joint object

        #todo add another layer
        #todo add bias

        self.w1=self.add_weight(name="Att1", shape=((input_size[0][1]*self.num_obj), self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        self.w2=self.add_weight(name="Att2", shape=(self.projection_size, self.num_obj), initializer="normal")

        super(IRNAttentionExtended, self).build(input_size)

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
        config = super(IRNAttentionExtended, self).get_config()
        config.update({"num_head": self.num_head,
                       "projection_size": self.projection_size,
                       "return_attention": self.return_attention})
        return config

class IRNAttentionMotion(keras.layers.Layer):
    def __init__(self, num_head=1, projection_size=None, return_attention=False, motion=None, **kwargs):
        self.return_attention = return_attention
        self.projection_size = projection_size
        self.num_head = num_head
        self.motion = motion
        super(IRNAttentionMotion, self).__init__(**kwargs)
        '''
        attention_weights = softmax (motion)
        '''

    def build(self, input_size):
        # if self.projection_size is None:
        #     self.projection_size = input_size[0][1] # size of joint object
        #
        # #todo add another layer
        # #todo add bias
        #
        # self.w1=self.add_weight(name="Att1", shape=(input_size[0][1], self.projection_size), initializer="normal") #name property is useful for avoiding RuntimeError: Unable to create link.
        # self.w2=self.add_weight(name="Att2", shape=(self.projection_size, 1), initializer="normal")

        super(IRNAttentionMotion, self).build(input_size)

    def call(self, inputs):

        inputs = tf.transpose(tf.stack(inputs), perm=[1,0,2])
        motionm = tf.transpose(tf.stack(self.motion), perm=[1,0,2])
        # motionm = motionm / motionm
        a = K.softmax(motionm, axis=1)
        # a = tf.Print(a, [a])
        output = inputs*a
        # ##return the ouputs. 'a' is the set of attention weights
        # ##the second variable is the 'attention adjusted o/p state' or context
        sentence = K.sum(output, axis=1)
        attention = a

        if self.return_attention:
            return [sentence, attention]
        else:
            return (sentence)

    def get_config(self):
        config = super(IRNAttentionMotion, self).get_config()
        config.update({"num_head": self.num_head,
                       "projection_size": self.projection_size,
                       "return_attention": self.return_attention})
        return config

