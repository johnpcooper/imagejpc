macro "runpyscript" {

	arg = getArgument()
	print(arg)
	//script = "c:\\Users\\John Cooper\\Projects\\byc\\byc\\imagejpc.py";
	//exec("python", script, arg1, arg2, arg3, arg4, arg5)
	exec("python", "-c", "print(123)")

}