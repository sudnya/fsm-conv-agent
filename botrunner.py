###############################################################################
#
# \file    botrunner.py
# \author  Sudnya Diamos <sudnyadiamos@gmail.com>
# \date    Saturday July 16, 2017
# \brief   Runner class to execute the model defined for finite state machine
#
###############################################################################

import argparse
import logging
import types
import imp

from transitions import Machine
from transitions import State
from transitions.extensions import GraphMachine as Machine


logger = logging.getLogger("BotRunner")

class BotRunner:
    def __init__(self, isVerbose, builder):
        self.machine = builder.getMachine()
        if isVerbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def run(self):
        pass
        
    
def main():
    parser = argparse.ArgumentParser(description="BotRunner")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")

    parsedArguments = parser.parse_args()
    arguments = vars(parsedArguments)

    isVerbose = arguments['verbose']

    if isVerbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    

if __name__ == '__main__':
    main()


