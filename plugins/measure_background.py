from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi

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
IJ.saveAs("Results", "{}{}_background.csv".format(path, measurements_filename))
IJ.selectWindow("Results")
IJ.run("Close")
IJ.log("Measurements saved at {}{}.csv".format(path, measurements_filename))