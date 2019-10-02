from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi

# Get the active image, its title, and the directory where it lies
imp = IJ.getImage()
imp_title = imp.getTitle()[:-4]
N_imp_frames = imp.getNSlices()
path = IJ.getDirectory("image")
#IJ.log("Active image source: {}{}".format(path, imp_title))

# Instantiate RoiManager as rm, select all rois and measure them
roim = RoiManager.getInstance()
rois_count = roim.getCount()
if rois_count == N_imp_frames:
	roi_save_path = str("{}{}_measurement_rois.zip".format(path, imp_title))
	roim.runCommand("Select All")
	roim.runCommand("Save", roi_save_path)
	print("ROIs saved at {}".format(roi_save_path))

else:
	print("ROI array was {} frames long, active image was {} frames long".format(rois_count, N_imp_frames))