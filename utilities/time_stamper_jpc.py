from ij import IJ

imp = IJ.getImage()

title = imp.getTitle()
title = title[:-4]
interval_hours = IJ.getNumber("Collection interval in hours:", 0.17)
fontsize = IJ.getNumber("Fontsize:", 14)
#get the directory containing the active image
path = IJ.getDirectory("image")
# If the active image is a duplicate of another image open, its path will be False and
# will print as 'None'. If this is the case, have the user choose a directory to put the
# timestamped tif
if not path:
	IJ.log("Image has no source directory")
	path = IJ.getDirectory("Choose the directory to save the timestamped tif")
else: 
	pass

height = imp.getHeight()
width = imp.getWidth()
size = imp.getImageStackSize()

IJ.log("Image title: {}".format(title))
IJ.log("Save path: {}".format(path))
IJ.log("Height: {}".format(height))
IJ.log("Width: {}".format(width))
IJ.log("Size: {}".format(size))

IJ.run("Label...", "format=0 starting=0 interval={} x=0 y={} font={} text=[hrs] range=1-{}".format(interval_hours, height, fontsize, size))

IJ.saveAs("Tiff", "{}{}_time_stamped".format(path, title))