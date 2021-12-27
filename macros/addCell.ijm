// This macro file needs to be added to be copied in
// C:\Users\John Cooper\appdata\Local\fiji-win64\Fiji.app\macros>
// in order to be callable by "IJ.runMacroFile('addCell.ijm', arg)" in
// save_cell_roi_set.py

// You'll also need to change the script file location and
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
    script = "c:\\Users\\johnp\\Dropbox\\Projects\\byc\\byc\\imagejpc\\addcellroi.py";
    python = "C:\\.byc\\Scripts\\python.exe"
    exec(python, script, args[0], args[1], args[2], args[3], args[4], args[5])

}