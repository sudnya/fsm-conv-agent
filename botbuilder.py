###############################################################################
#
# \file    botbuilder.py
# \author  Sudnya Diamos <sudnyadiamos@gmail.com>
# \date    Saturday July 15, 2017
# \brief   Builder class to build a finite state machine
#
###############################################################################

import argparse
import logging
import types
import imp

from transitions import Machine
from transitions import State
from transitions.extensions import GraphMachine as Machine


logger = logging.getLogger("BotBuilder")

class OurBot(object):
    def say_hello(self): 
        print("hello, new state!")


class BotBuilder:
    def __init__(self, isVerbose):
        if isVerbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        self.statesCounter = 0
        self.currentState = self.statesCounter
        self.bbot = OurBot()
        self.machine = Machine(model=self.bbot, initial=self.convertStateIdToName(0))
        self.labelToStateMap = {}
        logger.debug("Initialized BotBuilder with node: " + str(self.bbot.state))

    def botSays(self, botString):
        self.machine.add_states(State(name=self.getCurrentState()))
        setattr(self.bbot, "on_enter_"+self.getCurrentState(),
                types.MethodType(lambda: print(botString), self.bbot))
        self.machine.add_transition("advance",
            source=self.getCurrentState(),
            dest=self.convertStateIdToName(self.getNextStateId()))
        self.advanceState()
        
        logger.debug("Added bot says state " + self.getCurrentState())
    
    def singleOptionUserResponse(self, response):
        self.machine.add_transition(response, source=self.getCurrentState(),
                dest=self.convertStateIdToName(self.getNextStateId()))
        self.advanceState()
    
    def multipleOptionUserResponse(self,
            ifTransitionName, ifTransitionFunction,
            elseTransitionName, elseTransitionFunction):
        
        currentState = self.getCurrentState()
        ifState = self.createNewState()
        elseState = self.createNewState()
        mergeState = self.createNewState()

        logger.debug("Added if state " + self.convertStateIdToName(ifState))
        self.setCurrentState(ifState)
        ifTransitionFunction()
        self.machine.add_transition("if",
                source=self.convertStateIdToName(currentState),
                dest=self.convertStateIdToName(ifState))
        self.machine.add_transition("advance",
                source=self.getCurrentState(),
                dest=self.convertStateIdToName(mergeState))

        logger.debug("Added else state " + self.convertStateIdToName(elseState))
        self.setCurrentState(elseState)
        elseTransitionFunction()
        self.machine.add_transition("else",
                source=self.convertStateIdToName(currentState),
                dest=self.convertStateIdToName(elseState))
        self.machine.add_transition("advance",
                source=self.getCurrentState(),
                dest=self.convertStateIdToName(mergeState))

        logger.debug("Added merge state " + self.convertStateIdToName(mergeState))
        self.setCurrentState(mergeState)

    def gotoNode(self, nodeLabel):
        if not nodeLabel in self.labelToStateMap:
            self.labelToStateMap[nodeLabel] = self.createNewState()

        self.machine.add_transition("advance", source=self.getCurrentState(),
            dest=self.convertStateIdToName(self.labelToStateMap[nodeLabel]))
            
        self.setCurrentState(self.labelToStateMap[nodeLabel])

    def getCurrentState(self):
        return self.convertStateIdToName(self.getCurrentStateId())

    def getCurrentStateId(self):
        return self.currentState

    def convertStateIdToName(self, identity):
        return str(identity)

    def createNewState(self):
        self.statesCounter = self.getNextStateId()
        return self.statesCounter

    def getNextStateId(self):
        return self.statesCounter + 1

    def advanceState(self):
        self.setCurrentState(self.createNewState())

    def setCurrentState(self, state):
        self.currentState = state

    def plotStateMachine(self, name):
        self.bbot.get_graph().draw(name, prog='dot')
        
    
def main():
    parser = argparse.ArgumentParser(description="BotBuilder")
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


