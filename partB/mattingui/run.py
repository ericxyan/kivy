## CSC320 Winter 2016 
## Assignment 1 - Part B
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY


##
## DO NOT MODIFY ANY PART OF THIS FILE
##

import sys
import argparse


# import the modules from A1 partA
newsys = [sys.path[0], sys.path[0]+'/../partA/'] + sys.path[1:]
sys.path = newsys
from matting.run import main as mattingMain

# import the UI-related modules
from mattingui import viewer
from mattingui.widgets import VisCompApp


# Routine for parsing command-line arguments
# Upon success, it returns any unprocessed/unrecognized arguments 
# back to the caller
#
# Input arguments
#   - argv:   input command line arguments (as returned by sys.argv[1:])
#   - prog:   name of the executable (as returned by sys.argv[0])
# Return values
#   - True if all the required arguments are specified and False otherwise
#   - a Namespace() object containing the user-specified arguments and
#     any optional arguments that take default values
#   - a string containing any unrecognized/unprocessed command-line
#     arguments
#   - an error message (if success=False)
#     
def parseArguments(argv, prog=''):
    # Initialize the command-line parser by including the --usegui option
    parser = argparse.ArgumentParser(prog)

    # The only argument for the UI-based matting application, beyond
    # the terminal-based application is
    #    --usegui run the matting application in GUI mode
    #
    # NOTE: Kivy parses all command-line arguments and runs its GUI
    # initialization code before returning any arguments to the 
    # python library command-line parser. For this reason, the
    # application needs to be invoked using
    #    python main.py -- -usegui
    # the '--' tells the kivy argument parser that all following arguments
    # should be passed unprocessed to the standard python argument parser

    # We use the following statement to define the --usegui option
    parser.add_argument('--usegui', action='store_true',default=False, help='Use GUI')
    args, unprocessedArgv = parser.parse_known_args(argv)

    #
    return True, args, unprocessedArgv, ''

def main(argv, prog=''):
    # Parse the command-line arguments
    success, args, unprocessedArgv, msg = parseArguments(argv, )
    # search for the --usegui option
    if args.usegui == False:
        # if this option does not exist, we run the batch version of the code
        mattingMain(unprocessedArgv, prog)
    else:
        VisCompApp().run()
        

if __name__ == '__main__':
    main(sys.argv[1:], sys.argv[0])
