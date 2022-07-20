from ij import IJ
from ij.plugin.frame import RoiManager

def name_roi(daughter_shape="round"):
	roim = RoiManager.getInstance()
	if roim == None:
		# If no ROI manager window is already open,
		# getInstance() returns None
		IJ.run("ROI Manager...")
		roim = RoiManager.getInstance()
	else:
		pass
	roim.runCommand("Add")
	# Need to deselect all ROIs because if one
	# is selected, then getIndexes() will only
	# get the index of the selected ROI
	roim.runCommand("Deselect")
	indexes = roim.getIndexes()
	last_index = max(indexes)
	last_roi = roim.getRoi(last_index)
	roi_name = last_roi.getName()
	roim.rename(last_index, "{}-{}".format(roi_name, daughter_shape))
	
if __name__=="__main__":
	name_roi()