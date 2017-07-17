###############################################################################
#
# \file    caller.py
# \author  Sudnya Diamos <sudnyadiamos@gmail.com>
# \date    Saturday July 15, 2017
# \brief   Test class to demonstrate the usage of the botbuilder and botrunner
#
###############################################################################

import argparse
import logging

import botbuilder
import botrunner


def cannot_persuade(builder):
    builder.botSays("I'm sorry you feel that way")
    builder.gotoNode("endJournal")


def conv_journaling_persuasion(builder):
    builder.botSays("Okay you don't like journaling")
    builder.twoOptionUserResponse(
        "Not really", lambda: buttonToFoodJournal(builder, "Great, you can do so here"), 
        "Yeah I hate you", lambda: cannot_persuade(builder))


def buttonToFoodJournal(builder, string):
    builder.botSays(string)
    builder.botSays("https://food-journal-fb.herokuapp.com/")
    #callPythonFunction(openLinkToFoodJournal())


def conv_breakfast_conversation(builder):
    builder.botSays("Happy to see you")
    builder.singleOptionUserResponse("Me too")
    builder.botSays("Great we're both happy to see each other.")

    builder.gotoNode("askUserToJournal")
    builder.botSays("Do you want to journal now?")

    builder.twoOptionUserResponse(
        "Sure thing", lambda: buttonToFoodJournal(builder, "Great, you can do so here"), 
        "No thanks", lambda: conv_journaling_persuasion(builder))

    builder.gotoNode("endJournal")
    builder.botSays("Bye for now")



def runTest(isVerbose):
    builder = botbuilder.BotBuilder(isVerbose)
    conv_breakfast_conversation(builder)
    builder.plotStateMachine('state_machine.png')

    evaluator = botrunner.BotRunner(isVerbose, builder)
    evaluator.RunCommandLineEvaluator()


def main():
    parser = argparse.ArgumentParser(description="Caller")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")

    parsedArguments = parser.parse_args()
    arguments = vars(parsedArguments)

    isVerbose = arguments['verbose']

    if isVerbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    print("Test driven development for a sample conversation spec")
    runTest(isVerbose)


if __name__ == '__main__':
    main()

