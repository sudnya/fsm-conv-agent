import random
import logging

from transitions import Machine
from transitions import logger
from transitions import State

logger.setLevel(logging.INFO)

#class Matter(object):
#    pass
# Our old Matter class, now with  a couple of new methods we
# can trigger when entering or exit states.
class OurBot(object):
    def say_hello(self): print("hello, new state!")
    def say_goodbye(self): print("goodbye, old state!")
    def say_welcome(self): print("Hey! Welcome back. Did you fill your food journal today?")
    def celebrate(self): print("YAY! You did it! <<GIF>>")
    def want_to_fill_now(self): print("Would you like to fill it now?")
    def send_link(self): print("You can fill it at https://food-journal-fb.herokuapp.com/ ")


def main():
    bbot = OurBot()

    states = [
        State(name='Start'),
        State(name='Did_you_fill', on_enter=['say_welcome']),
        State(name='Fill_now', on_enter=["want_to_fill_now"]),
        State(name='link', on_enter=["send_link"]),
        State(name='Stop', on_exit=['say_goodbye']),

        ]

    transitions = [ #trigger, source, destination
        ['Hi',  'Start', 'Did_you_fill'],
        ['yes_filled', 'Did_you_fill', 'Stop'],
        ['not_filled', 'Did_you_fill', 'Fill_now'],
        ['yes', 'Fill_now', 'link'],
        ['no',  'Fill_now', 'Start']
    ]
    
    machine = Machine(model=bbot, states=states, transitions=transitions, initial='Start')
    machine.add_transition('done', source='link', dest='Stop')

    # Callbacks can also be added after initialization using
    # the dynamically added on_enter_ and on_exit_ methods.
    # Note that the initial call to add the callback is made
    # on the Machine and not on the model.
    machine.on_enter_Stop('celebrate')

    # Test out the callbacks...
    machine.set_state('Start')
    logger.info(bbot.state)

    if bbot.is_Start():
        bbot.Hi()
        logger.info(bbot.state)
        bbot.yes_filled()
        logger.info(bbot.state)
        
        
    print("Let's try again")
    # Test out the callbacks...
    machine.set_state('Start')
    logger.info(bbot.state)

    if bbot.is_Start():
        bbot.Hi()
        logger.info(bbot.state)
        bbot.not_filled()
        logger.info(bbot.state)
        bbot.yes()
        logger.info(bbot.state)
        bbot.done()
        logger.info(bbot.state)

    
    print("and again")
    # Test out the callbacks...
    machine.set_state('Start')
    logger.info(bbot.state)

    if bbot.is_Start():
        bbot.Hi()
        logger.info(bbot.state)
        bbot.not_filled()
        logger.info(bbot.state)
        bbot.no()
        logger.info(bbot.state)

    
    
    
if __name__ == '__main__':
    main()

