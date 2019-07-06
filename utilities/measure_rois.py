from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi

# Get the active image, its title, and the directory where it lies
imp = IJ.getImage()
imp_title = imp.getTitle()
path = IJ.getDirectory("image")

# Set measurements to redirect to the active image
IJ.run("Set Measurements...", "area mean standard min center perimeter bounding fit feret's integrated median stack display redirect={}".format(imp_title))

# Instantiate RoiManager as rm, select all rois and measure them
roim = RoiManager.getInstance()
roim.runCommand("Select All")
roim.runCommand("Measure")

# Save the measurements just made using the name of the active image
title = imp_title[:-4]
IJ.saveAs("Results", "{}{}.csv".format(path, title))
IJ.selectWindow("Results")
IJ.run("Close")

# Just leaving this here for future reference
#results = ij.measure.ResultsTable()
#results.saveAs("{}{}.csv".format(path, title))