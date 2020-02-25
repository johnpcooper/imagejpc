import os
from ij import IJ
import glob

def threshold_brightfield(imp):
	# this code is based on my "Threshold brightfield [Q]" macro. Need to automate 
	# finding threshold values instead of hardcoding themm here.
	IJ.run("Find Edges");
	IJ.setThreshold(2654, 65535)
	IJ.run("Convert to Mask")
	IJ.run("Fill Holes")
	IJ.run("Watershed")

def create_rois():
	# Create rois based on (in this script) the process brightfield image.
	# Also scale the rois down using my plugin scale_rois.py
	IJ.run("Set Measurements...", "area mean standard min centroid center perimeter bounding fit feret's integrated median stack display redirect=None decimal=3")
	IJ.run("Analyze Particles...", "size=100-2000 circularity=0.60-1.00 exclude add in_situ")
	IJ.run("scale rois", "choose=0.65 choose=0.65")

def open_files(n_channels):
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
				threshold_brightfield(imp)
				create_rois()
			else:
				pass
		# Run my measure_rois.py plug in. Closes this set of images after running
		IJ.run("measure rois")
		
open_files(3)

			
			
	