from ij import IJ

def get_percentile(percentile):

	imp = IJ.getImage()
	stats = imp.getRawStatistics()
	hist = stats.histogram()
	
	hist_x_min = stats.histMin
	hist_x_max = stats.histMax
	hist_x_range = hist_x_max - hist_x_min
	
	hist_x_values = []
	
	for bin in range(0, stats.nBins):
	
		print("Fraction pixels with intensity in bins 0 to {}".format(bin))
		integral = sum(hist[0:bin])/sum(hist)
		print(integral)
	
		intensity = hist_x_range * bin/stats.nBins
		hist_x_values.append(intensity)
		
		print(intensity)
	
		if integral > percentile:
			threshold_intensity = intensity
			break
		else:
			pass

	return threshold_intensity

# example run
threshold_value = get_percentile(0.80)
print(threshold_value)

IJ.setThreshold(threshold_value, 65535)
IJ.run("Convert to Mask")