import numpy as np
import sys
import tensorflow as tf
from preprocessing import *
import random
from nn import *

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def main():
     
    targets_names = ["un T-shirt/top", "un pantalon", "un pullover", "une robe", "un manteau", "une sandal", "un shirt", "une basket", "un sac", "une bottine"]
    
    model = network()
    model.load_save("save_model.json","save.h5")
    #m.train(image, target)
    #model.save("save")
    if (len(sys.argv) == 2):
        elt, color, rgb = main_prepro(sys.argv[1])
        elt = np.array(elt)
        elt = elt.reshape(28,28,1)
        
        res = list(model.run(np.array([elt]))[0])
        obj = targets_names[res.index(max(res))]
        print("L'image est",obj,"de couleur",color,"(RGB:",rgb,")")

main()
