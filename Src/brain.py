from Src.Helpers.singleton import Singleton
from Src.Models.direction import Direction
from Src.Models.turnInformation import TurnInformation

class Brain(metaclass=Singleton):

    def on_next_move(turn_info: TurnInformation):
        '''
        YOUR CODE GOES IN THIS FUNCTION. This is where your AI takes a decision on his next move.
        @param turn_info: Information from the current turn
        @return: The direction your AI chose as his next move.
        '''
        print("the game server wants to know your next move and you have the following informations : the id is {0} and the current map is {1} ".format(turn_info.SelfId, turn_info.Map))

        # As a default we put that the direction to UP.
        return Direction._UP

    def on_finalized(turn_info: TurnInformation):
        '''
        Once the game is finished, this method is triggered with the final state of the map. 
        It could be used to train the AI for example.
        @param turn_info: Information from the current turn
        '''
        print("the game has ended and the received id from the game server is {0} with the following map {1}".format(turn_info.SelfId, turn_info.Map)) 
