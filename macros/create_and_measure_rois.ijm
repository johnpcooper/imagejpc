macro "Create and Measure ROIs [L]" {

	run("Set Measurements...", "area mean standard min centroid center perimeter bounding fit feret's integrated median stack display redirect=None decimal=3");
	run("Analyze Particles...", "size=100-2000 circularity=0.60-1.00 exclude add in_situ");
	run("scale rois", "choose=0.65 choose=0.65");
	run("Focus Search Bar");
	run("measure rois");

}
