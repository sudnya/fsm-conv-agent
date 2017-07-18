###############################################################################
#
# \file    botbuilder.py
# \author  Sudnya Diamos <sudnyadiamos@gmail.com>
# \date    Saturday July 15, 2017
# \brief   Builder class to build a finite state machine
#
###############################################################################
'''
person_name
gender
for later -> number of lbs to lose
current_weight
reason for weight loss
favorite_song

upto 3 possible paths for user response

quiz -> 1 correct answer, other wrong

'''
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
        self.beginState = self.currentState
        
        self.bbot = OurBot()
        self.machine = Machine(model=self.bbot, 
            initial=self.convertStateIdToName(self.beginState), 
            auto_transitions=False)
        
        self.machine.add_states(State(name=self.getCurrentState()))
        self.labelToStateMap = {}
        self.stateIdToContent = {}
        self.returnStack = []
        logger.debug("Initialized BotBuilder with node:" + str(self.bbot.state))

    def botSays(self, botString):
        setattr(self.bbot, "on_enter_"+self.getCurrentState(),
                types.MethodType(lambda x: print(botString), self.bbot))
        self.machine.add_transition("advance",
            source=self.getCurrentState(),
            dest=self.convertStateIdToName(self.getNextStateId()))
        logger.debug("Tagging state " + self.getCurrentState() +
                " as bot says state")

        self.advanceState(botString)
        logger.debug("Creating fallthrough state " + self.getCurrentState())
        
    
    def singleOptionUserResponse(self, response):
        self.machine.add_transition(response, source=self.getCurrentState(),
                dest=self.convertStateIdToName(self.getNextStateId()))
        self.advanceState(response)
    
    def twoOptionUserResponse(self,
            ifTransitionName, ifTransitionFunction,
            elseTransitionName, elseTransitionFunction):
        
        currentState = self.getCurrentState()
        ifState = self.createNewState(ifTransitionName)
        elseState = self.createNewState(elseTransitionName)
        mergeState = self.createNewState("merge-block")

        logger.debug("Added if state " + self.convertStateIdToName(ifState))
        self.setCurrentState(ifState)
        self.pushReturnStack()
        ifTransitionFunction()
        self.machine.add_transition(ifTransitionName,
                source=self.convertStateIdToName(currentState),
                dest=self.convertStateIdToName(ifState))
        if self.popReturnStack():
            self.machine.add_transition("advance",
                    source=self.getCurrentState(),
                    dest=self.convertStateIdToName(mergeState))

        logger.debug("Added else state " + self.convertStateIdToName(elseState))
        self.setCurrentState(elseState)
        self.pushReturnStack()
        elseTransitionFunction()
        self.machine.add_transition(elseTransitionName,
                source=self.convertStateIdToName(currentState),
                dest=self.convertStateIdToName(elseState))

        if self.popReturnStack():
            self.machine.add_transition("advance",
                    source=self.getCurrentState(),
                    dest=self.convertStateIdToName(mergeState))

        logger.debug("Added merge state " + self.convertStateIdToName(mergeState))
        self.setCurrentState(mergeState)

    def gotoNode(self, nodeLabel):
        if len(self.returnStack) > 0:
            self.returnStack[-1] = False

        if not nodeLabel in self.labelToStateMap:
            self.labelToStateMap[nodeLabel] = self.createNewState(nodeLabel)
            logger.debug("Creating branch to node " + self.getCurrentState())

        self.machine.add_transition("advance", source=self.getCurrentState(),
            dest=self.convertStateIdToName(self.labelToStateMap[nodeLabel]))
            
        self.setCurrentState(self.labelToStateMap[nodeLabel])

    def getCurrentState(self):
        return self.convertStateIdToName(self.getCurrentStateId())

    def getCurrentStateId(self):
        return self.currentState

    def convertStateIdToName(self, identity):
        return str(identity)

    def createNewState(self, textStr):
        self.statesCounter = self.getNextStateId()
        logger.debug("Created state " +
            self.convertStateIdToName(self.statesCounter))
        self.machine.add_states(
            State(name=self.convertStateIdToName(self.statesCounter)))
        self.stateIdToContent[self.convertStateIdToName(self.statesCounter)] = textStr
        return self.statesCounter

    def getNextStateId(self):
        return self.statesCounter + 1

    def advanceState(self, textStr):
        self.setCurrentState(self.createNewState(textStr))

    def setCurrentState(self, state):
        self.currentState = state

    def plotStateMachine(self, name):
        self.bbot.get_graph().draw(name, prog='dot')

    def getBeginState(self):
        return self.convertStateIdToName(self.beginState)

    def getMachine(self):
        return self.machine

    def getModel(self):
        return self.bbot

    def pushReturnStack(self):
        self.returnStack.append(True)
    
    def popReturnStack(self):
        value = self.returnStack[-1]
        self.returnStack.pop()
        return value

    def getStateContent(self, stateId):
        return self.stateIdToContent.get(self.convertStateIdToName(stateId))

