import os
from ij import IJ
import glob
from ij.plugin.frame import RoiManager

_threshold_percent = 0.9
_n_channels = IJ.getNumber("Enter the number of channels used in this experiment (including brightfield)", 3)

def get_percentile(imp, percentile):

    IJ.log("Segmenting brightfield with percentile threshold {}".format(percentile))

    stats = imp.getRawStatistics()
    hist = stats.histogram()
    
    hist_x_min = stats.histMin
    hist_x_max = stats.histMax
    hist_x_range = hist_x_max - hist_x_min
    
    hist_x_values = []
    
    for bin in range(0, stats.nBins):
    
        #print("Fraction pixels with intensity in bins 0 to {}".format(bin))
        integral = sum(hist[0:bin])/sum(hist)
        #print(integral)
    
        intensity = hist_x_range * bin/stats.nBins
        hist_x_values.append(intensity)
        
        #print(intensity)
    
        if integral > percentile:
            threshold_intensity = intensity
            break
        else:
            pass

    return threshold_intensity

def threshold_brightfield(imp, threshold_percent):
    # this code is based on my "Threshold brightfield [Q]" macro. Need to automate 
    # finding threshold values instead of hardcoding themm here.
    IJ.run("Find Edges")
    lower_threshold = get_percentile(imp, threshold_percent)
    IJ.setThreshold(lower_threshold, 65535)
    IJ.run("Convert to Mask")
    IJ.run("Fill Holes")
    IJ.run("Watershed")

def create_rois():
    # Create rois based on (in this script) the process brightfield image.
    # Also scale the rois down using my plugin scale_rois.py
    IJ.run("Set Measurements...", "area mean standard min centroid center perimeter bounding fit feret's integrated median stack display redirect=None decimal=3")
    IJ.run("Analyze Particles...", "size=100-8000 pixel circularity=0.60-1.00 exclude add in_situ")

def analyze_files(n_channels, threshold_percent):
    # Ask the user to choose a directory containing the images to be analyzed
    # Open each one, find the brightfield image and process it to make ROIs
    # then measure the ROIs, close that set and open the next
    data_dir = IJ.getDirectory("Choose the directory containing single channel tifs")
    IJ.log('Data directory > {}'.format(data_dir))
    files_list = os.listdir(data_dir)

    for i in range(0, len(files_list), n_channels):
        # Iterate over the group of images corresponding to the different
        # channels for this measurement condition. Open them, find the one
        # with 'bf' in the title and apply threshold
        for filename in files_list[i:i + n_channels]:
        
            path = '{}/{}'.format(data_dir, filename)
            IJ.log('Opening image > {}'.format(path))
            IJ.open(path)
            imp = IJ.getImage()

            # find the brightfield image and process it
            if 'bf' in imp.getTitle():
                # Closing the found bf image here cleans up the loop below
                imp.close()
                bf_path = path
                IJ.log("Found bf image at {}".format(bf_path))     
                # Try 14 different threshold values and use the one
                # that yields the highest number of rois
                roiCounts = []
                threshold_values = []
                for i in range(-15, 10):
                    IJ.open(bf_path)
                    imp = IJ.getImage()
                    threshold_value = threshold_percent + i*0.01
                    threshold_brightfield(imp, threshold_value)
                    create_rois()
                    
                    roim = RoiManager.getInstance()
                    # if roim == None, then no ROIs
                    # were found with this threshold 
                    # value
                    if roim == None:
                        roiCount = 0
                    else:
                        try:
                            roiCount = roim.getCount()
                        except:
                            print('Failed to get ROI manager instance. Probably no ROIs found')
                            roiCount = 0
                    roiCounts.append(roiCount)
                    threshold_values.append(threshold_value)

                    IJ.log("Found {} ROIs".format(roiCount))
                    imp.changes = False
                    imp.close()
                    if roiCount != 0:
                        roim.reset()
                # sorted() returns a sorted list of keys of
                # the dictionary passed to the function
                IJ.open(bf_path)
                imp = IJ.getImage()
                dic = dict(zip(roiCounts, threshold_values))
                if len(dic) > 0:
                    try:
                        sorted_dic = sorted(dic)
                        # Find the threshold value at which 
                        # the most cell ROIs were identified
                        final_threshold_value = dic[sorted_dic[-1]] 
                        threshold_brightfield(imp, final_threshold_value)
                        create_rois()
                        IJ.run("scale rois", "choose=0.8 choose=0.8")
                        # Save the rois generated above
                        roiCount = roim.getCount()
                        if roiCount > 1:
                            ext = '.zip'
                        else:
                            ext = '.roi'
                        rois_save_path = "{}_cell_rois{}".format(bf_path[0:-4], ext)
                        roim = RoiManager.getInstance()
                        roim.runCommand("Select All")
                        roim.runCommand("Save", rois_save_path)
                        # Set the public variable changes to false so that 
                        # the save changes dialog won't pop up
                        imp.changes = False
                        measureable = True
                    except:
                        print('Unable to find cell ROIs for this image')
                        measureable = False
                else:
                    imp.close()
                    
            else:
                pass
        # Run my measure_and_clear_rois.py plug in. Closes this set of images after running
        if len(dic) > 0 and measureable == True:
            IJ.run("measure and clear rois")
        else:
            print("No cells found in image")
        
analyze_files(int(_n_channels), _threshold_percent)