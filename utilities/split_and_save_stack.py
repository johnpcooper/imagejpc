from ij import IJ
from ij import WindowManager
import os

def split_stack():

	imp = IJ.getImage()
	path = IJ.getDirectory("image")
	
	IJ.run("Stack to Images", "")
	# close original image and leave split stacks open
	imp.close()

	n_images = WindowManager.getImageCount()

	for i in range(0, n_images):
		frame_imp = IJ.getImages()
		imp_title = frame_imp.getTitle()
		
		save_path = "{}{}".format(path, imp_title)
		IJ.saveAsTiff(frame_imp, save_path)
		IJ.log("{} saved at {}".format(frame_imp, save_path))

		frame_imp.close()

split_stack()
		