from ij import IJ
from ij import WindowManager
import os

# Should update this later so that channel names are not hardcoded
# should be able to get from metadata
channel_names = ['bf', 'yfp', 'dsred']

def save_tifs():
	# Get the active image, its title, and the directory where it lies
	imp = IJ.getImage()
	imp_title = imp.getTitle()
	path = IJ.getDirectory("image")
	IJ.log("Active image source: {}{}".format(path, imp_title))

	for i in range(0, len(channel_names)):
		current_name = channel_names[i]
		if "C={}".format(i) in imp_title:
			channel_name = current_name
			found_name = True
		else:
			pass

	# In the imp title string, find the index where .nd2 first appears. Everything
	# up to this point is kept for use in saving the file.
	end_of_title = imp_title.find('.nd2')
	tif_title = "{}_{}".format(imp_title[:end_of_title], channel_name)
	# Save the image
	save_path = "{}{}".format(path, tif_title)
	IJ.saveAsTiff(imp, save_path)
	IJ.log("Tif saved at {}.tif".format(save_path))
	# Close the image
	imp.close()

# Have the user choose the directory containing the .nd2 files
# to opened, split, and renamed.
data_dir = IJ.getDirectory("Choose the directory containing .nd2s")
filenames = os.listdir(data_dir)

for filename in filenames:
	IJ.open(filename)
	n_images = WindowManager.getImageCount()
	i = 0
	while i < n_images:
		save_tifs()
		i+= 1