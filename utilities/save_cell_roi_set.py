from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.gui import GenericDialog
import os


# Should probably set these variables below when instantiating a class so they
# can be attributes of class rather than global vairables
_expt_type = 'byc'
_accepted_roi_file_types = ['.roi', '.zip']
_accepted_roi_set_types = ['bud', 'crop', 'measurement', 'steady_state']

active_imp = IJ.getImage()
active_imp_path = IJ.getDirectory("image")

# get active image source directory and title
def get_expt_title(active_imp):
	# Everything except the file type part of the active image title
	active_imp_title = str(active_imp.getTitle()[:-4])
	first_index = active_imp_title.find('_')
	expt_title = '{}_{}'.format(active_imp_title[:first_index], _expt_type)
	
	IJ.log('Expt. title: {}'.format(expt_title))
	return expt_title

# check active image source directory for files ending with .roi or .zip
# and create a list with them. Check the length
def get_roi_fns(path):
	# Return a list of filenmaes of all .roi or .zip files in path
	IJ.log('Checking {} for roi files of type .roi or .zip'.format(path))
	fns = os.listdir(path)

	roi_fns = []
	for fn in fns:
		if fn[-4:] in _accepted_roi_file_types:
			roi_fns.append(fn)
		else:
			pass

	return roi_fns

# Ask the user what type of roi set this is, can only specify types that are in list
def get_roi_set_type():

	roi_set_type = IJ.getString("Enter cell roi set type", _accepted_roi_set_types[0])
	return roi_set_type
	
# Save current roi set as the active image name (date_byc_cell_length_of_files_list)
def get_roi_set_fn(expt_title, roi_fns, roi_set_type):
	
	cell_index = len(roi_fns)
	# As far as I can tell, jython doesn't interpret 
	# cell_index = f''
	if cell_index < 10:
		cell_index = '00{}'.format(cell_index)

	elif 10 <= cell_index < 100:
		cell_index = '0{}'.format(cell_index)
	else:
		pass
		
	roi_set_fn = '{}_{}_{}_rois'.format(expt_title, cell_index, roi_set_type)
	IJ.log('Saving roi set as {}'.format(roi_set_fn))

	return roi_set_fn

def save_roi_set(roi_set_fn, data_dir):

	roi_set_save_path = '{}{}.zip'.format(data_dir, roi_set_fn)
	roim = RoiManager.getInstance()
	roim.runCommand("Select All")
	roim.runCommand("Save", roi_set_save_path)

# Add name of roi set and the path to its source to a master_index csvs
def add_cell_to_database():
	pass

def run():

	expt_title = get_expt_title(active_imp)
	roi_fns = get_roi_fns(active_imp_path)
	roi_set_type = get_roi_set_type()
	roi_set_fn = get_roi_set_fn(expt_title, roi_fns, roi_set_type)
	save_roi_set(roi_set_fn, data_dir=active_imp_path)

run()

