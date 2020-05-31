#!  /usr/bin/env python3
###
### chem driver program for equalizing chemical equasions
###
### main goal to behave like a console application
###
#   modes
#   --help              displays help
#   -f some_file1 some_file2        reads from a file;each reaction should be in plain teext
#   -i                  interactive mode; runs programme as a dialog in the shell
#   --ocr img1 img2...  run program in ocr mode(NYI);input is taken from images
#   (until another parameter)
#   -s                  silent mode; no output on
#   -v                  starts program in ui mode
#   -p                  read from stdin from a pipe


import sys
import chem_parcer
import chemist_ui
# TODO import chemist_dialogue

def solve(task):
    if type(task) is string:
        #test=chemical_reaction("C2H5OH + O2 -> H2O + CO2")
        try:
            test=chemical_reaction(task)
            print(test.solve_eq())
        except:
            print("bad reaction: {}".format(task),file=sys.stderr)
    else:
        print("bad reaction: {}".format(task),file=sys.stderr)
        return ""

#   starts it with a gui
def Start_visual():
    chemist_ui.Run_With_Window()
    return

#   starts it in dialogue mode
def Start_dialogue():
    # TODO chemist_dialogue.Start_dialogue()
    pass

#   starts it in bulk mode if input form file
def Bulk_Process(input_files):
    for inp in input_files
        try: 
            with open(file) as fp:
                line=fp.readline()
                while line:
                    line = line.strip("\"")
                    solve_eq(line)
        except:
            print("could not stat {}".format(inp),file=sys.stderr)
#   start in ocr processing mode
def Start_Ocr(input_files, output_file):
    #   NYI
    pass

arg_types = ["-i","-v","-s","--ocr",,"-f","--help"]

if __name__ == "__main__":
    sys.argv.pop(0)
    inp_files=[]
    ocr_files=[]
    output_file=""
    mode=0

    for arg in sys.argv:
        if arg in arg_types:
            mode = arg_types.index(arg)
        elif mode == arg_types.index("-f"):
            inp_files.append(arg)
        elif mode == arg_types.index("--ocr"):
            ocr_files.append(arg)
        elif mode == arg_types.index("-v"):
            Start_visual()
        elif mode == arg_types.index("-i"):
            Start_dialogue()
            exit(0)
        else:
            print ("unknown parameter  ", arg," at ",sys.argv.index(arg)+1 ,"")
            exit(1)
    if inp_files.__len__!=0:
        Bulk_Process(inp_files,output_file)
    if ocr_files.__len__!=0:
        Bulk_Process(inp_files,output_file)
