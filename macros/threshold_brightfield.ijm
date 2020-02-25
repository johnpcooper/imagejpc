macro "Threshold brightfield [B]" {

	run("Find Edges");
	setAutoThreshold("Default dark");
	//run("Threshold...");
	setThreshold(2673, 65535);
	setOption("BlackBackground", false);
	run("Convert to Mask");
	run("Fill Holes");
	run("Watershed");

}