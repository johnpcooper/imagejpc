import os
from ij.plugin.frame import RoiManager
from ij import IJ

_accepted_roi_file_types = ['.zip', '.roi']
_expt_type = 'byc'
# check active image source directory for files ending with .roi or .zip
# and create a list with them. Check the length
def get_roi_fns(directory, roi_set_type):
    # Return a list of filenmaes of all .roi or .zip files in path
    IJ.log('Checking {} for roi files of type .roi or .zip'.format(directory))
    fns = os.listdir(directory)

    roi_fns = []
    for fn in fns:
        if fn[-4:] in _accepted_roi_file_types and roi_set_type in fn:
            roi_fns.append(fn)
        else:
            pass

    return roi_fns
    
# get active image source directory and title
def get_expt_title(active_imp):
    # Everything except the file type part of the active image title
    active_imp_title = str(active_imp.getTitle())
    first_index = active_imp_title.find('_')
    expt_title = '{}_{}'.format(active_imp_title[:first_index], _expt_type)
    
    IJ.log('Expt. title: {}'.format(expt_title))
    return expt_title
    
# Save current roi set as the active image name (date_byc_cell_length_of_files_list)
def get_roi_set_fn(expt_title, roi_fns, roi_set_type):
    
    cell_index = len(roi_fns)
    # As far as I can tell, jython doesn't interpret 
    # cell_index = f'{len(roi_fns):03}' which would do the same thing
    # as this if loop
    if cell_index < 10:
        cell_index = '00{}'.format(cell_index)

    elif 10 <= cell_index < 100:
        cell_index = '0{}'.format(cell_index)
    else:
        pass
        
    roi_set_fn = '{}_cell{}_{}_rois'.format(expt_title, cell_index, roi_set_type)
    IJ.log('Saving roi set as {}'.format(roi_set_fn))

    return roi_set_fn

def get_roi_set_save_path(roi_set_fn, data_dir):

    roi_set_save_path = '{}{}.zip'.format(data_dir, roi_set_fn)
    
    return roi_set_save_path

def save_roi_set(roi_set_save_path):

    roim = RoiManager.getInstance()
    roim.runCommand("Select All")
    roim.runCommand("Save", roi_set_save_path)
    roim.reset()
    
if __name__=="__main__":
    
	active_imp = IJ.getImage()
	active_imp_dir = IJ.getDirectory("image")
	IJ.log(active_imp_dir)
	roi_set_type = 'daughter'
	daughter_roi_fns = get_roi_fns(active_imp_dir, roi_set_type)
	IJ.log("Found daughter rois:\n{}".format(daughter_roi_fns))
	expt_title = get_expt_title(active_imp)
	roi_set_fn = get_roi_set_fn(expt_title, daughter_roi_fns, roi_set_type)
	roi_set_save_path = get_roi_set_save_path(roi_set_fn, active_imp_dir)
	save_roi_set(roi_set_save_path)
	IJ.log("Saved daughter cell roi set at \n{}".format(roi_set_save_path))