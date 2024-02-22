from PIL import Image, ImageFilter
from pathlib import Path
import numpy as np
from .colorTransform import SRGBToSRGBLinear

def loadImage(path):
    img = Image.open(Path(path))
    return np.asarray(img)/256.0

def loadImageWithBlur(path, blur = 0.0):
    img = Image.open(Path(path))
    img = img.filter(ImageFilter.GaussianBlur(radius = blur))

    return np.asarray(img)/256.0

def loadImageAsLinearSRGB(path, blur = 0.0):
    img = Image.open(Path(path))

    if blur != 0.0:
        img = img.filter(ImageFilter.GaussianBlur(radius = blur))
    
    imgArray = np.asarray(img)/256.0
    imgSRGBLinearArray = SRGBToSRGBLinear(imgArray)
    
    return imgSRGBLinearArray