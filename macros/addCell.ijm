// You need to change the script file location and
// python.exe location according to your byc installation and byc
// environment locations

macro "addCell" {
    // Description coming soon
    arg = getArgument();
    string=arg;
    delimiter="|";
    args=split(string, delimiter)
    // Call python from the .byc environment
    // so it has access to byc source etc.
    script = "c:\\Users\\usrname\\Projects\\byc\\byc\\imagejpc\\addcellroi.py";
    python = "c:\\Users\\usrname\\Projects\\envs\\.byc\\Scripts\\python.exe"
    exec(python, script, args[0], args[1], args[2], args[3], args[4], args[5], args[6])

}