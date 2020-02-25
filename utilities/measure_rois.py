from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.gui import GenericDialog
from ij import WindowManager


def measure_rois():
	# Get the active image, its title, and the directory where it lies
	imp = IJ.getImage()
	imp_title = imp.getTitle()
	path = IJ.getDirectory("image")
	IJ.log("Active image source: {}{}".format(path, imp_title))

	# Set measurements to redirect to the active image
	IJ.run("Set Measurements...", "area mean standard min center perimeter bounding fit feret's integrated median stack display redirect={}".format(imp_title))

	# Instantiate RoiManager as rm, select all rois and measure them
	roim = RoiManager.getInstance()
	roim.runCommand("Select All")
	roim.runCommand("Measure")

	# Save the measurements just made using the name of the active image
	measurements_filename = imp_title[:-4]
	IJ.saveAs("Results", "{}{}.csv".format(path, measurements_filename))
	IJ.selectWindow("Results")
	IJ.run("Close")
	IJ.log("Measurements saved at {}{}.csv".format(path, measurements_filename))
	# Close the active image so IJ can move on to the next
	imp.close()

n_images = WindowManager.getImageCount()
i = 0
while i < n_images:
	measure_rois()
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
