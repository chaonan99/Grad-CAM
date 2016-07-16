import sys
import os
from docopt import docopt
import PyTorch
import PyTorchHelpers
import numpy as np



def run():

    proto_file = "models/VGG_ILSVRC_16_layers_deploy.prototxt"
    model_file = "models/VGG_ILSVRC_16_layers.caffemodel"
    backend = 'nn'
    input_sz = 224
    layer_name = 'relu5_3'
    input_image_path = 'images/cat_dog.jpg'
    label = 243
    seed = 123
    gpuid = -1
    out_path = 'output/'

    TorchModel = PyTorchHelpers.load_lua_class('new_classification.lua', 'TorchModel')
    torchModel = TorchModel(proto_file, model_file, backend, input_sz, layer_name, input_image_path, label, seed, gpuid, out_path)
    cnn = torchModel.processData(input_image_path, input_sz, input_sz)

run()