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

def getMatchingTransition(response, transitions):
    for t in transitions:
        if response.lower() == t.lower():
            return t

    assert False

class BotRunner:
    def __init__(self, isVerbose, builder):
        self.machine = builder.getMachine()
        self.model   = builder.getModel()
        self.beginState = builder.getBeginState()
        self.endState = builder.getCurrentState()
        
        if isVerbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    def RunCommandLineEvaluator(self):
        start = self.beginState
        end   = self.endState

        current = start
        self.machine.set_state(start)
        while True:
            current = self.model.state
            print('current state is: ' + current)
            if current == end:
                break
            transitions = self.machine.get_triggers(current)
            #print('possible transitions ' + str(transitions))
            assert len(transitions) > 0

            if len(transitions) == 1:
                if transitions[0] == 'advance':
                    self.model.trigger(transitions[0])
                    continue
            
            userResponse = input(transitions)
            self.model.trigger(
                    getMatchingTransition(userResponse, transitions))


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


