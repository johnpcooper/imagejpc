from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.gui import GenericDialog

gui = GenericDialog("ROI warning")

# Get the active image, its title, and the directory where it lies
imp = IJ.getImage()
imp_title = imp.getTitle()[:-4]
N_imp_frames = imp.getNSlices()
path = IJ.getDirectory("image")
#IJ.log("Active image source: {}{}".format(path, imp_title))

# Instantiate RoiManager as rm, select all rois and measure them
roim = RoiManager.getInstance()
# Run the sort and interpolate commands. Before running "save rois" the
# user should have define first and last ROIs and a few in between.
roim.runCommand("Sort")
roim.runCommand("Interpolate ROIs")
# Get the roi count for quality control loop below
rois_count = roim.getCount()
if rois_count == N_imp_frames:
	roi_save_path = str("{}{}_measurement_rois.zip".format(path, imp_title))
	roim.runCommand("Select All")
	roim.runCommand("Save", roi_save_path)
	print("ROIs saved at {}".format(roi_save_path))

else:
	print("ROI array was {} frames long, active image was {} frames long".format(rois_count, N_imp_frames))
	
	# get the indices of the roi and let the user know which slices the double ROIs are at
	rois_array = roim.getRoisAsArray()
	double_roi_slices = []

	for i in range(0, rois_count-1):
	
		slice_roi_n = rois_array[i].getZPosition()
		slice_roi_n_plus_1 = rois_array[i+1].getZPosition()
		slice_roi_n_min_1 = rois_array[i-1].getZPosition()
	
		if slice_roi_n == slice_roi_n_plus_1:
			double_roi_slices.append(slice_roi_n)
		elif slice_roi_n == slice_roi_n_min_1:
			print("Multiple ROIs at position {}".format(slice_roi_n))
			double_roi_slices.append(slice_roi_n)

	for double_roi_slice in list(set(double_roi_slices)):
		gui.addMessage("Multiple ROIs for slice {}".format(double_roi_slice))

	gui.showDialog()