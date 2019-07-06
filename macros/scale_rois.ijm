 macro "Scale ROIs [S]" {

	x = getNumber("Choose x scale: ", 0.65);
	y = getNumber("Choose y scale", 0.65)
	
	// Iterate all ROIs in ROI Manager
	for (i=0; i<roiManager("count"); ++i) {
		roiManager("Select", i);
		
		// Scale ROI
		run("Scale... ", "x=x y=y centered");
	
		// Replace old ROI with scaled one
		roiManager("update")
	}
 }