# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
# Modifications copyright (C) 2017 UT Austin/Taewan Kim
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Contains a factory for building various models."""
# Modified for deep learning based calibration code

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools

import tensorflow as tf
import tensorflow.contrib.slim as slim

from nets import vgg_calib as vgg
from nets import mobilenet_v1_calib as mobilenet_v1

networks_map = {'vgg_a': vgg.vgg_a,
                'vgg_16': vgg.vgg_16,
                'vgg_91': vgg.vgg_19,
                'mobilenet_v1': mobilenet_v1.mobilenet_v1
                }

arg_scopes_map = {'vgg_a': vgg.vgg_arg_scope,
                   'vgg_16': vgg.vgg_arg_scope,
                   'vgg_16': vgg.vgg_arg_scope,
                   'mobilenet_v1': mobilenet_v1.mobilenet_v1_arg_scope
                   }

# networks_map = {'alexnet_v2': alexnet.alexnet_v2,
#                 'cifarnet': cifarnet.cifarnet,
#                 'overfeat': overfeat.overfeat,
#                 'vgg_a': vgg.vgg_a,
#                 'vgg_16': vgg.vgg_16,
#                 'vgg_19': vgg.vgg_19,
#                 'inception_v1': inception.inception_v1,
#                 'inception_v2': inception.inception_v2,
#                 'inception_v3': inception.inception_v3,
#                 'inception_v4': inception.inception_v4,
#                 'inception_resnet_v2': inception.inception_resnet_v2,
#                 'lenet': lenet.lenet,
#                 'resnet_v1_50': resnet_v1.resnet_v1_50,
#                 'resnet_v1_101': resnet_v1.resnet_v1_101,
#                 'resnet_v1_152': resnet_v1.resnet_v1_152,
#                 'resnet_v1_200': resnet_v1.resnet_v1_200,
#                 'resnet_v2_50': resnet_v2.resnet_v2_50,
#                 'resnet_v2_101': resnet_v2.resnet_v2_101,
#                 'resnet_v2_152': resnet_v2.resnet_v2_152,
#                 'resnet_v2_200': resnet_v2.resnet_v2_200,
#                 'mobilenet_v1': mobilenet_v1.mobilenet_v1,
#                }

# arg_scopes_map = {'alexnet_v2': alexnet.alexnet_v2_arg_scope,
#                   'cifarnet': cifarnet.cifarnet_arg_scope,
#                   'overfeat': overfeat.overfeat_arg_scope,
#                   'vgg_a': vgg.vgg_arg_scope,
#                   'vgg_16': vgg.vgg_arg_scope,
#                   'vgg_19': vgg.vgg_arg_scope,
#                   'inception_v1': inception.inception_v3_arg_scope,
#                   'inception_v2': inception.inception_v3_arg_scope,
#                   'inception_v3': inception.inception_v3_arg_scope,
#                   'inception_v4': inception.inception_v4_arg_scope,
#                   'inception_resnet_v2':
#                   inception.inception_resnet_v2_arg_scope,
#                   'lenet': lenet.lenet_arg_scope,
#                   'resnet_v1_50': resnet_v1.resnet_arg_scope,
#                   'resnet_v1_101': resnet_v1.resnet_arg_scope,
#                   'resnet_v1_152': resnet_v1.resnet_arg_scope,
#                   'resnet_v1_200': resnet_v1.resnet_arg_scope,
#                   'resnet_v2_50': resnet_v2.resnet_arg_scope,
#                   'resnet_v2_101': resnet_v2.resnet_arg_scope,
#                   'resnet_v2_152': resnet_v2.resnet_arg_scope,
#                   'resnet_v2_200': resnet_v2.resnet_arg_scope,
#                   'mobilenet_v1': mobilenet_v1.mobilenet_v1_arg_scope,
#                  }


def get_network_fn(name, num_preds, weight_decay=0.0, is_training=False):
  """Returns a network_fn such as `y_preds, end_points = network_fn(images)`.

  Args:
    name: The name of the network.
    num_classes: The number of classes to use for classification.
    weight_decay: The l2 coefficient for the model weights.
    is_training: `True` if the model is being used for training and `False`
      otherwise.

  Returns:
    network_fn: A function that applies the model to a batch of images. It has
      the following signature:
        y_preds, end_points = network_fn(images)
  Raises:
    ValueError: If network `name` is not recognized.
  """
  if name not in networks_map:
    raise ValueError('Name of network unknown %s' % name)
  arg_scope = arg_scopes_map[name](weight_decay=weight_decay)
  func = networks_map[name]
  @functools.wraps(func)
  def network_fn(images,lidars):
    with slim.arg_scope(arg_scope):
      return func(images,lidars, num_preds, is_training=is_training)
  if hasattr(func, 'default_image_size'):
    network_fn.default_image_size = func.default_image_size

  return network_fn
