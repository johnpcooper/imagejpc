import os
from ij import IJ
import glob
from ij.plugin.frame import RoiManager

_threshold_percent = 0.9



def threshold_brightfield(imp, threshold_percent):
    # this code is based on my "Threshold brightfield [Q]" macro. Need to automate 
    # finding threshold values instead of hardcoding themm here.
    IJ.run("Find Edges")
    lower_threshold = get_percentile(imp, threshold_percent)
    IJ.setThreshold(lower_threshold, 65535)
    IJ.run("Convert to Mask")
    IJ.run("Fill Holes")
    IJ.run("Watershed")

imp = IJ.getImage()

threshold_brightfield(imp,. _threshold_percent)