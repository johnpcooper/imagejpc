from ij import IJ

imp = IJ.getImage()

title = imp.getTitle()
title = title[:-4]
interval_units = IJ.getString("Collection interval units: ", 'hrs')
start_time = IJ.getString("Start time: ", '0')
interval_by_units = IJ.getNumber("Collection interval in {}:".format(interval_units), 0.17)
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

IJ.run("Label...", "format=0 starting={} interval={} x=0 y={} font={} text=[{}] range=1-{}".format(start_time,
                                                                                                   interval_by_units,
                                                                                                   height,
                                                                                                   fontsize,
                                                                                                   interval_units,
                                                                                                   size))

IJ.saveAs("Tiff", "{}{}_time_stamped".format(path, title))