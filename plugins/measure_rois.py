from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.gui import GenericDialog
from ij import WindowManager
from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.gui import GenericDialog
from ij import WindowManager

import os

def measure_rois():
	# Get the active image, its title, and the directory where it lies
	imp = IJ.getImage()
	imp_title = imp.getTitle()
	image_dir = IJ.getDirectory("image")
	image_path = os.path.join(image_dir, "{}".format(imp_title))
	IJ.log("Active image source: {}".format(image_path))

	# Set measurements to redirect to the active image
	IJ.run("Set Measurements...", "area mean standard min center perimeter bounding fit feret's integrated median stack display redirect={}".format(imp_title))

	# Instantiate RoiManager as rm, select all rois and measure them
	roim = RoiManager.getInstance()
	roim.runCommand("Select All")
	roim.runCommand("Measure")

	# Save the measurements just made using the name of the active image
	measurements_filename = imp_title[:-4]
	IJ.saveAs("Results", "{}{}.csv".format(image_dir, measurements_filename))
	IJ.selectWindow("Results")
	IJ.run("Close")
	IJ.log("Measurements saved at {}{}.csv".format(image_dir, measurements_filename))
	# Close the active image so IJ can move on to the next
	imp.close()
	return image_path

n_images = WindowManager.getImageCount()
i = 0
image_paths = []
while i < n_images:
	path = measure_rois()
	image_paths.append(path)
	i += 1
# Clear ROI manager (after OKing with user) so that there aren't still 
# ROIs that will be used in next measurement
gd = GenericDialog("ROI deletion warning")
gd.addMessage("Do you wish to clear current ROIs?")
gd.enableYesNoCancel()
choice = gd.showDialog()
roim = RoiManager.getInstance()

if gd.wasCanceled():
	pass
elif gd.wasOKed():
	roim.reset()
else:
	print("NO")

def get_cell_index_from_path(path):
	query = 'cell'
	start_index = path.rindex(query) + len(query)
	end_index = start_index + 3
	cell_index = int(path[start_index:end_index])
	return cell_index
	
def get_xy_from_path(path):
	query = 'xy'
	start_index = path.rindex(query) + len(query)
	end_index = start_index + 2
	xy = int(path[start_index:end_index])
	return xy

# Open the next set of cell trace images in the dataset
for path in image_paths:
	cell_index= get_cell_index_from_path(path)
	xy = get_xy_from_path(path)
	next_cell_index = cell_index + 1
	next_xy = xy + 1
	# Find cellNNN in the current filename and
	# replace it with the next cell index
	find = "{}{}".format('cell', str(cell_index).zfill(3))
	replace_with = "{}{}".format('cell', str(next_cell_index).zfill(3))
	next_path = path.replace(find, replace_with)
	try:
		imp = IJ.openImage(next_path)
		imp.show()
	except:
		# Try next xy coordinate just in case
		find = "{}{}".format('xy', str(xy).zfill(2))
		replace_with = "{}{}".format('xy', str(next_xy).zfill(2))
		next_xy_path = next_path.replace(find, replace_with)
		imp = IJ.openImage(next_xy_path)
		imp.show()

	IJ.log("Opened next image at {}".format(path))
