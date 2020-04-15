from Libs.core import *
from settings import DEBUG



def run_from_command_line(args):
    if (len(args)==1)==DEBUG:
        startcmd() 
    else:
        startgui()