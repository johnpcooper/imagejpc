import os
from ij import IJ
import glob
from ij.plugin.frame import RoiManager

_threshold_percent = 0.9

bf_path = r"C:\Users\johnp\Box\Finkelstein-Matouschek\images\20220325_Moment_Panda_Demo\moment_data\20220325_BY4741_no-plasmid_exp030s_moment_004_bf.tif"

def get_percentile(imp, percentile):

    IJ.log("Segmenting brightfield with percentile threshold {}".format(percentile))

    stats = imp.getRawStatistics()
    hist = stats.histogram()
    
    hist_x_min = stats.histMin
    hist_x_max = stats.histMax
    hist_x_range = hist_x_max - hist_x_min
    
    hist_x_values = []
    
    for bin in range(0, stats.nBins):
    
        #print("Fraction pixels with intensity in bins 0 to {}".format(bin))
        integral = sum(hist[0:bin])/sum(hist)
        #print(integral)
    
        intensity = hist_x_range * bin/stats.nBins
        hist_x_values.append(intensity)
        
        #print(intensity)
    
        if integral > percentile:
            threshold_intensity = intensity
            break
        else:
            pass

    return threshold_intensity

def threshold_brightfield(imp, threshold_percent):
    # this code is based on my "Threshold brightfield [Q]" macro. Need to automate 
    # finding threshold values instead of hardcoding themm here.
    IJ.run("Find Edges")
    lower_threshold = get_percentile(imp, threshold_percent)
    IJ.setThreshold(lower_threshold, 65535)
    IJ.run("Convert to Mask")
    IJ.run("Fill Holes")
    IJ.run("Watershed")
    
def create_rois():
    # Create rois based on (in this script) the process brightfield image.
    # Also scale the rois down using my plugin scale_rois.py
    IJ.run("Set Measurements...", "area mean standard min centroid center perimeter bounding fit feret's integrated median stack display redirect=None decimal=3")
    IJ.run("Analyze Particles...", "size=100-8000 pixel circularity=0.60-1.00 exclude add in_situ")
    
#for i in range(-10, 10):
#	IJ.open(bf_path)
#	imp = IJ.getImage()
#	
#	threshold_value = _threshold_percent + i*0.01
#	threshold_brightfield(imp, threshold_value)
#	create_rois()


imp = IJ.getImage()
threshold_brightfield(imp, 0.85)