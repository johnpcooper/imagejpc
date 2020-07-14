from ij import IJ

values = [str(0),
		  r"C:\Users\John Cooper\Box Sync\Finkelstein-Matouschek\byc_data\example_byc_expts\20200221_byc_analysis\pJC069_rpn4d\image.tif",
		  "another path",
		  "death",
		  "measurement"]

arg = ' '.join(values)

IJ.runMacroFile('runpyscript.ijm', arg)