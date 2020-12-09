from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import Roi
from ij.gui import GenericDialog
import os
from ij.plugin.filter import Analyzer

# The purpose of this script is to save a set of rois
# that in some way follow a cell through a stack
# where each frame is a different timepoint. 
class CellRoiSetter(object):

    def __init__(self):

        self._expt_type = 'byc'
        self._accepted_roi_file_types = ['.roi', '.zip']
        self._accepted_roi_set_types = ['measurement', 'bud', 'crop']
        self._accepted_end_event_types = ['death', 'escape', 'sen']
    
        self.active_imp = IJ.getImage()
        self.active_imp_dir = IJ.getDirectory("image")
        self.active_imp_path = '{}{}'.format(self.active_imp_dir, self.active_imp.getTitle())
                
        self.roi_set_type = self.get_roi_set_type()
        self.end_event_type = self.get_end_event_type()

        self.expt_title = self.get_expt_title(self.active_imp)
        self.roi_fns = self.get_roi_fns(self.active_imp_dir, self.roi_set_type)
        self.cell_index = len(self.roi_fns)
        
        self.roi_set_fn = self.get_roi_set_fn(self.expt_title, self.roi_fns, self.roi_set_type)
        self.roi_set_save_path = self.get_roi_set_save_path(self.roi_set_fn, self.active_imp_dir)
    
    # get active image source directory and title
    def get_expt_title(self, active_imp):
        # Everything except the file type part of the active image title
        active_imp_title = str(active_imp.getTitle())
        first_index = active_imp_title.find('_')
        expt_title = '{}_{}'.format(active_imp_title[:first_index], self._expt_type)
        
        IJ.log('Expt. title: {}'.format(expt_title))
        return expt_title
    
    # check active image source directory for files ending with .roi or .zip
    # and create a list with them. Check the length
    def get_roi_fns(self, directory, roi_set_type):
        # Return a list of filenmaes of all .roi or .zip files in path
        IJ.log('Checking {} for roi files of type .roi or .zip'.format(directory))
        fns = os.listdir(directory)
    
        roi_fns = []
        for fn in fns:
            if fn[-4:] in self._accepted_roi_file_types and roi_set_type in fn:
                roi_fns.append(fn)
            else:
                pass
    
        return roi_fns
    
    # Ask the user what type of roi set this is, can only specify types that are in list
    def get_roi_set_type(self):
    
        roi_set_type = None
        
        while roi_set_type not in self._accepted_roi_set_types: 
            roi_set_type = IJ.getString("Enter cell ROI set type \n({})".format(self._accepted_roi_set_types),
                                        self._accepted_roi_set_types[0])
            
        return roi_set_type

    def get_end_event_type(self):

        end_event_type = None
        
        while end_event_type not in self._accepted_end_event_types:
            end_event_type = IJ.getString("Enter cell end event type \n({})".format(self._accepted_end_event_types),
                                        self._accepted_end_event_types[0])
            
        return end_event_type
        
    # Save current roi set as the active image name (date_byc_cell_length_of_files_list)
    def get_roi_set_fn(self, expt_title, roi_fns, roi_set_type):
        
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

    def get_roi_set_save_path(self, roi_set_fn, data_dir):
    
        roi_set_save_path = '{}{}.zip'.format(data_dir, roi_set_fn)
        
        return roi_set_save_path
    
    def save_roi_set(self, roi_set_save_path):
    
        roim = RoiManager.getInstance()
        roim.runCommand("Select All")
        roim.runCommand("Save", roi_set_save_path)
        roim.reset()
    
    # Add name of roi set and the path to its source to a master_index csvs
    def add_result(self, column, row, value):
        
        self.table = Analyzer.getResultsTable()
        self.table.setValue(column, row, value)
        #self.table.show('Title')

    def add_cell_to_results(self):
    
        args = [str(self.cell_index),
                  self.active_imp_path,
                  self.roi_set_save_path,
                  self.end_event_type,
                  self.roi_set_type,
                  self.active_imp_dir]
        arg = '|'.join(args)
        # Run a macro from imagejpc that runs
        # the script byc/imagejpc/addcellroi.py
        IJ.runMacroFile('addCell.ijm', arg)
        
def run():

    crs = CellRoiSetter()
    if crs.roi_set_type == 'measurement':
        IJ.run("save cell measurement rois")
    else:   
        crs.save_roi_set(crs.roi_set_save_path)

    crs.add_cell_to_results()

run()