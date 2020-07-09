macro "addCell" {
	// Description coming soon
	arg = getArgument();
	string=arg;
	delimiter="|";
	args=split(string, delimiter);
	script = "c:\\Users\\John Cooper\\Projects\\byc\\byc\\imagejpc\\addcell.py";
	exec("python", script, args[0], args[1], args[2], args[3], args[4], args[5])

}