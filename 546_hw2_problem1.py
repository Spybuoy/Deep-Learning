# -*- coding: utf-8 -*-
"""546_hw2_problem1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EjVkdptSakvywOXItxvs1UCcQASXZyeU
"""

import torchvision
from torchvision import models

resnet18 = models.resnet18()

for name, m in resnet18.named_children():
    print(name)
    # print(m.parameters())

from torch import conv_tbc
bn_params = {'weight':[], 'bias':[]}
fc_bias = []
conv_bias = []
rest = []
for name, param in resnet18.named_parameters(): 
  # print(name, param.shape)
  # print(type(name))
  if 'bn' in name:
    if 'weight' in name:
      bn_params['weight'].append(param)
    if 'bias' in name:
      bn_params['bias'].append(param)
  elif 'conv' in name:
    if 'bias' in name:
      conv_tbc.append(param)
  elif 'fc' in name:
    if 'bias' in name:
      fc_bias.append(param)
  else:
    rest.append(param)
# print(bn_params['weight'][0])
# print(fc_bias)
# print(conv_bias)
print(rest)