import numpy as np

def SRGBLinearToSRGB(rgbLinear):
    rgb = np.where(rgbLinear <= 0.00304, 12.92 * rgbLinear, 1.055 * np.power(rgbLinear, 1.0/2.4) - 0.055)

    rgbMax = np.amax(rgb, axis=0) + 0.00001
    intensityCutoff = 1.0
    rgb = np.where(rgbMax > intensityCutoff, rgb * intensityCutoff / (rgbMax), rgb)

    return rgb

def SRGBToSRGBLinear(rgb):
    rgbLinear = np.where(rgb <= 0.03928, rgb / 12.92, np.power((rgb + 0.055) / 1.055, 2.4))

    return rgbLinear