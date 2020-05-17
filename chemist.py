#!  /usr/bin/env python3 
### 
### chem driver program for equalizing chemical equasions
### 
### main goal to behave like a console application
###
#   modes 
#   --help              displays help
#   -f some_file1 some_file2        reads from a file;ech reaction should be in plain text 
#   -o some_file1 some_file2       specifies output file to write output, if one is not specified stdout is used
#   -i                  interactive mode; runs programme as a dialog in the shell
#   --ocr img1 img2...  run program in ocr mode(NYI);input is taken from images 
#   (until another parameter)
#   -s                  silent mode; no output on
#   -v                  starts program in ui mode
#   -p                  read from stdin from a pipe


import sys
import chem_parcer

#   starts it with a gui 
def Start_visual():
    pass

#   starts it in dialogue mode
def Start_dialogue():
    pass

#   starts it in bulk mode if input form file
def Bulk_Process(input_files, output_file):
    pass

#   start in ocr processing mode
def Start_Ocr(input_files, output_file):
    pass
#   starts it in pipe mode to read form stdin
def Start_pipe():
    pass 

arg_types = ["-i","-v","-s","--ocr","-o","-f","--help","-p"]

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
        elif mode == arg_types.index("-o"):
            if output_file == "":
                output_file=arg
            else:
                print("output file already specified!") 
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
    

