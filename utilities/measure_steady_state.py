import os
from ij import IJ
import glob

_threshold_percent = IJ.getNumber("Enter proportion to cut off in brightfield edge segmentation", 0.85)
_n_channels = IJ.getNumber("Enter proportion to cut off in brightfield edge segmentation", 3)

def get_percentile(imp, percentile):

	stats = imp.getRawStatistics()
	hist = stats.histogram()
	
	hist_x_min = stats.histMin
	hist_x_max = stats.histMax
	hist_x_range = hist_x_max - hist_x_min
	
	hist_x_values = []
	
	for bin in range(0, stats.nBins):
	
		print("Fraction pixels with intensity in bins 0 to {}".format(bin))
		integral = sum(hist[0:bin])/sum(hist)
		print(integral)
	
		intensity = hist_x_range * bin/stats.nBins
		hist_x_values.append(intensity)
		
		print(intensity)
	
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
	IJ.run("Analyze Particles...", "size=100-2000 circularity=0.60-1.00 exclude add in_situ")
	IJ.run("scale rois", "choose=0.65 choose=0.65")

def open_files(n_channels, threshold_percent):
	# Ask the user to choose a directory containing the images to be analyzed
	# Open each one, find the brightfield image and process it to make ROIs
	# then measure the ROIs, close that set and open the next
	data_dir = IJ.getDirectory("Choose the directory containing single channel tifs")
	IJ.log('Data directory > {}'.format(data_dir))
	files_list = os.listdir(data_dir)

	for i in range(0, len(files_list), n_channels):
		# Iterate over the group of images corresponding to the different
		# channels for this measurement condition. Open them, find the one
		# with 'bf' in the title and apply threshold
		for filename in files_list[i:i + n_channels]:
		
			path = '{}/{}'.format(data_dir, filename)
			IJ.log('Opening image > {}'.format(path))
			IJ.open(path)
			imp = IJ.getImage()

			# find the brightfield image and process it
			if 'bf' in imp.getTitle():
				IJ.log("Found bf image")
				threshold_brightfield(imp, threshold_percent)
				create_rois()
			else:
				pass
		# Run my measure_rois.py plug in. Closes this set of images after running
		IJ.run("measure rois")
		
open_files(int(_n_channels), _threshold_percent)

			
			
	