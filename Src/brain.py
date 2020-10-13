from Src.Helpers.singleton import Singleton
#from Src.Helpers.brainHelper import get_other_players_position
from Src.Models.direction import Direction
from Src.Models.turnInformation import TurnInformation
#from Src.Models.playerPosition import PlayerPosition
#import numpy as np


class Brain(metaclass=Singleton):
    # Random variable globale
    step_compter = 0
    directions_possibles = [Direction._UP, Direction._DOWN, Direction._RIGHT, Direction._LEFT, Direction._NONE]

    #remove direction "removeDirection" from array
    #Brain.directions_possibles.pop(directions_possibles.index(removeDirection))



    #turn_info.Map
    # directions_possibles = [Direction._UP, Direction._DOWN, Direction._RIGHT, Direction._LEFT, Direction._NONE]
    # [0,1,2,3]
    # def verifier_fonction_possible():
    #     risk = []
    #     for dir in directions_possibles:
    #         risk.append(calculer_risk(dir))
    #     return directions_possibles[argsortmin(risk)]
    
    # def calculer_mouvement(directions_possibles):

    # def wall_security(dir):
    #     if ()



    #     return action

    #MUR
    

    #sates : (xplore : augment the area, attack:path finding to kill, defend : still /wtv.)
    #but:
    #PlayerPosition.Head = vector2()
    #PlayerPosition.Body = []
    #PlayerPosition.Neck = []

    # def wallCollission(action, map, player_position):
    #     if action == Direction._UP:
    #         if map[player_position.Y + 1][player_position.X] == 'W':

    #     elif action == Direction._DOWN:

    #
    # def wallcheck(possible_action):
    #     new_possible_action
    #     for dir in possible_action:
    #         if 
        
    #     return new_possible 
    
    # def calculate_risk(dir):
    
    # def self_position(self_id, map, map_width):
    # '''
    # Gets the positions of all other players.
    # @param selfId: The id of the player calling the function.
    # @param map: The map of the current turn.
    # @param mapWidth: The size of a row in the map.
    # '''

    # other_players_position = {}
    # c_counter = 0
    # r_counter = map_width - 1

    # for pos in map:
    #     if "P" in pos or "p" in pos:
    #         splitPos = pos.split("-")
    #         splitPos = filter(lambda s: ("P" in s or "p" in s) and str(self_id) not in s, splitPos )
    #         for v in splitPos:
    #             playerId = v[1]
    #             if playerId not in other_players_position:
    #                 other_players_position[playerId] = PlayerPosition(Vector2(), [], [])

    #             if "*" in v:
    #                 other_players_position[playerId].Head = Vector2(X=c_counter, Y=r_counter)
    #             elif "p" in v:
    #                 other_players_position[playerId].Neck.append(Vector2(X=c_counter, Y=r_counter))
    #             else:
    #                 other_players_position[playerId].Body.append(Vector2(X=c_counter, Y=r_counter))


    #     c_counter += 1
    #     if c_counter >= map_width:
    #         c_counter = 0
    #         r_counter -= 1

    # return other_players_position

    
    
    def on_next_move(turn_info: TurnInformation):
        '''
        YOUR CODE GOES IN THIS FUNCTION. This is where your AI takes a decision on his next move.
        @param turn_info: Information from the current turn
        @return: The direction your AI chose as his next move.
        '''
        # player = get_other_player_position(turn_info.SelfId, )
        # print("La position de la tete est: ")

        print("the game server wants to know your next move and you have the following informations : the id is {0} and the current map is {1} ".format(turn_info.SelfId, turn_info.Map))
        # As a default we put that the direction to UP.
        # new_possibles = wallcheck(Brain.directions_possibles)
        Brain.step_compter+=1
        return Brain.directions_possibles[Brain.step_compter%len(Brain.directions_possibles)]
        
    def on_finalized(turn_info: TurnInformation):
        '''
        Once the game is finished, this method is triggered with the final state of the map. 
        It could be used to train the AI for example.
        @param turn_info: Information from the current turn
        '''
        print("the game has ended and the received id from the game server is {0} with the following map {1}".format(turn_info.SelfId, turn_info.Map)) 
