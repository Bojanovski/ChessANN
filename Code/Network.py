# definitions

import tensorflow as tf
import numpy as np


def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


class FCLayer():
  def __init__(self, inputs, outputs, nonlinearity = tf.nn.relu):
    self.W = weight_variable([inputs, outputs])
    self.b = bias_variable([outputs])
    self.nonlinearity = nonlinearity
  
  def forward(self, X):
    s = tf.matmul(X, self.W) + self.b
    return self.nonlinearity(s)

import pdb
class GroupLayer():
  def __init__(self, input_groups, output_groups, nonlinearity = tf.nn.relu):
    self.ingroups = [sum(input_groups[:i]) for i in range(len(input_groups) + 1)]
    self.sublayers = [FCLayer(input_groups[i], output_groups[i], nonlinearity) for i in range(0,len(input_groups))]
  
  def forward(self, X):
    h = [];
    for i in range(len(self.sublayers)):
      h += [self.sublayers[i].forward(X[:,self.ingroups[i] : self.ingroups[i+1]])]
    return tf.concat(1,h)

# group_dimens - 2D matrica, u prvom retku su dimenzije ulaza svake grupe
# a u drugom dimenzije izlaza
# [[10, 10, 20], [4, 4, 1]] će biti sloj sa 40 ulaza i 9 izlaza
# prva vrijednost u architecture mora biti jednaka sumi prve dimenzija group_dimens
# druga vrijednost u architecture je jednaka sumi vrijednosti druge dimenzije group_dimens
class GroupNetwork():
  def __init__(self, architecture, group_dimens, nonlinearity = tf.nn.relu):
    self.layers = [GroupLayer(group_dimens[0], group_dimens[1], nonlinearity=nonlinearity)]
    
    for i in range(1, len(architecture)-2):
      self.layers.append(FCLayer(architecture[i], architecture[i+1], nonlinearity=nonlinearity))
    
    self.layers.append(FCLayer(architecture[-2], architecture[-1], nonlinearity=tf.tanh))
    
    self.inputs = tf.placeholder(tf.float32, shape=[None, sum(group_dimens[0])])
    self.output = tf.placeholder(tf.float32, shape= [None, architecture[-1]])
    
    self.out = self.layers[0].forward(self.inputs)
    for i in range(1, len(self.layers)):
      self.out = self.layers[i].forward(self.out)
      
    self.session = tf.Session();
    self.session.run(tf.initialize_all_variables())
  
  def train(self, X, Y_, lr, niter):
    mse = tf.reduce_sum((self.out - self.output)**2)
    train_step = tf.train.GradientDescentOptimizer(lr).minimize(mse)
    
    errs = [];
    for i in range(niter):
      train_step.run(feed_dict={self.inputs: X, self.output: Y_},session=self.session)
      errs.append(mse.eval(feed_dict={self.inputs: X, self.output: Y_},session=self.session))
    
    return errs;
  
  def predict(self, X):
    return self.out.eval(feed_dict={self.inputs: X}, session = self.session)
