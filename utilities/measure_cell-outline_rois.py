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

def get_cell_index_from_path(path):
	query = 'cell'
	try:
		start_index = path.rindex(query) + len(query)
		end_index = start_index + 3
		cell_index = int(path[start_index:end_index])
	except:
		cell_index = None
		IJ.log('Failed to find cell index in filepath\n{}'.format(path))
	return cell_index


def measure_rois(close_imp=True, return_imp_path=True):

	# Get the active image, its title, and the directory where it lies
	imp = IJ.getImage()
	imp_title = imp.getTitle()
	image_dir = IJ.getDirectory("image")
	active_imp_path = os.path.join(image_dir, "{}".format(imp_title))
	IJ.log("Active image source: {}".format(active_imp_path))

	# Set measurements to redirect to the active image
	IJ.run("Set Measurements...", "area mean standard min center perimeter bounding fit feret's integrated median stack display redirect={}".format(imp_title))

	# Instantiate RoiManager as rm, select all rois and measure them
	roim = RoiManager.getInstance()
	roim.runCommand("Select All")
	roim.runCommand("Measure")

	# Save the measurements just made using the name of the active image
	active_imp_based_measfilename = "{}.csv".format(imp_title[:-4]
)
	for channelname in ['bf', 'yfp', 'rfp', 'mko', 'gfp', 'bfp']:
		if channelname in active_imp_based_measfilename:
			channel = channelname
		else:
			pass
	if channel == None:
		channel = 'unknown-channel'
	# Adding option to save using roi names in active image directory
	filetype = 'crop_rois.zip'
	files = os.listdir(image_dir)
	zip_names = []
	existing_csv_names = []
	# Found the highest cell index (most recently created) channel
	# measurement csv and set current cell index to that channel
	# measurement csv's cell index + 1s
	for filename in files:
		if filetype in filename:
			zip_names.append(filename)
			csv_name = filename.replace('.zip', '.csv')
			csv_name = csv_name.replace('.csv', '_{}.csv'.format(channel))
			if os.path.exists(os.path.join(image_dir, csv_name)):
				existing_csv_names.append(csv_name)
			else:
				pass
	if len(existing_csv_names) > 0:
		# pre existing csvs were found so add
		# 1 to the cell index of the most recently
		# created one and make that current filename
		previous_csv = existing_csv_names[-1]
		previous_cell_index = get_cell_index_from_path(previous_csv)
		if previous_cell_index != None:
			max_cell_index = previous_cell_index
			max_csv_name = previous_csv
			current_cell_index = max_cell_index + 1
		else:
			print("Cell index not found in filename\n{}".format(filename))
			IJ.log("Cell index not found in filename\n{}".format(filename))
	else:
		csv_name = zip_names[0].replace('.zip', '.csv')
		max_csv_name = csv_name.replace('.csv', '_{}.csv'.format(channel))
		max_cell_index = 0
		current_cell_index = 0
	
	find = "cell{}".format(str(max_cell_index).zfill(3))
	replace_with = "cell{}".format(str(current_cell_index).zfill(3))
	measurements_filename = max_csv_name.replace(find, replace_with)
	measurement_filename = measurements_filename.replace('.csv', "_{}.csv".format(channel))
	measurements_savepath = os.path.join(image_dir, measurements_filename)
	IJ.saveAs("Results", measurements_savepath)
	IJ.selectWindow("Results")
	IJ.run("Close")
	IJ.log("Measurements saved at\n{}".format(measurements_savepath))
	# Close the active image so IJ can move on to the next
	if close_imp:
		imp.close()
	return (measurements_savepath
, active_imp_path)

n_images = WindowManager.getImageCount()
i = 0
image_paths = []
while i < n_images:
	measpath, active_imp_path = measure_rois()
	image_paths.append(active_imp_path)
	i += 1
# Reopen images used for measurements
for path in image_paths:
	IJ.open(path)
# Clear ROI manager (after OKing with user) so that there aren't still 
# ROIs that will be used in next measurement
gd = GenericDialog("ROI deletion warning")
gd.addMessage("Do you wish to clear current ROIs?")
gd.enableYesNoCancel()
gd.showDialog()

if gd.wasCanceled():
	pass
elif gd.wasOKed():
	roim = RoiManager.getInstance()
	roim.reset()
