from Src.Helpers.singleton import Singleton
from Src.Helpers.brainHelper import get_other_players_position
from Src.Models.direction import Direction
from Src.Models.turnInformation import TurnInformation
from Src.Models.playerPosition import PlayerPosition
from Src.Models.vector2 import Vector2
import numpy as np


class Brain(metaclass=Singleton):
    # Random variable globale
    #MEMO playerID : turn_info.SelfId, map : turn_info.Map
    counter = 0
    DIRECTIONS_POSSIBLES = [Direction._UP, Direction._DOWN, Direction._RIGHT, Direction._LEFT, Direction._NONE]
    directions_possibles = DIRECTIONS_POSSIBLES

    def ObstacleCheck(player_position_head : Vector2, possible_actions, turn_info):
        new_possible_actions = []
        map2d = np.array(turn_info.Map).reshape((turn_info.MapWidth, turn_info.MapWidth))
        print(map2d)
        map2d = map2d.tolist()
        print(player_position_head.X,player_position_head.Y)
        
        j = turn_info.MapWidth - player_position_head.Y - 1
        i = player_position_head.X
        print(i, j)
        for action in possible_actions:
            # Check if wall up.
            if action == Direction._UP:
                if (map2d[j - 1][i] != 'W') and (map2d[j - 1][i] != ('p' + str(turn_info.SelfId))) and (map2d[j - 1][i] != 'B'):
                    new_possible_actions.append(action)
                    print('UP')
            # Check if wall down.
            elif action == Direction._DOWN:
                if (map2d[j + 1][i] != 'W') and (map2d[j + 1][i] != ('p' + str(turn_info.SelfId))) and (map2d[j + 1][i] != 'B'):
                    new_possible_actions.append(action)
                    print('DOWN')
            # Check if wall left.
            elif action == Direction._LEFT:
                if (map2d[j][i- 1] != 'W') and (map2d[j][i - 1] != ('p' + str(turn_info.SelfId))) and (map2d[j + 1][i] != 'B'):
                    new_possible_actions.append(action)
                    print('LEFT')
            # Check if wall right.
            elif action == Direction._RIGHT:
                if (map2d[j][i + 1] != 'W') and (map2d[j][i + 1] != ('p' + str(turn_info.SelfId))) and (map2d[j + 1][i] != 'B'):
                    new_possible_actions.append(action)
                    print('RIGHT')
        print(len(new_possible_actions))  
        return new_possible_actions
    
    def get_players_position(turn_info):
        players_position = {}
        c_counter = 0
        r_counter = turn_info.MapWidth - 1
        
        for pos in turn_info.Map:
            if "P" in pos or "p" in pos:
                splitPos = pos.split("-")
                splitPos = filter(lambda s: ("P" in s or "p" in s), splitPos)
                for v in splitPos:
                    playerId = v[1]
                    if playerId not in players_position:
                        players_position[playerId] = PlayerPosition(Vector2(), [], [])

                    if "*" in v:
                        players_position[playerId].Head = Vector2(X=c_counter, Y=r_counter)
                    elif "p" in v:
                        players_position[playerId].Neck.append(Vector2(X=c_counter, Y=r_counter))
                    else:
                        players_position[playerId].Body.append(Vector2(X=c_counter, Y=r_counter))

            c_counter += 1
            if c_counter >= turn_info.MapWidth:
                c_counter = 0
                r_counter -= 1
        return players_position


    def CalculMovement(movement):
        for i in range(50):
            for i in range(2):
                movement.append(Direction._UP)
            movement.append(Direction._RIGHT)
            movement.append(Direction._DOWN)
            movement.append(Direction._LEFT)
        return movement
    

    def MovementDeBase(currentPlayer, turn_info):

        movement = [Direction._UP, Direction._UP, Direction._RIGHT, Direction._DOWN, Direction._LEFT]
        movement = Brain.CalculMovement(movement)
        mouvementsPossibles = Brain.ObstacleCheck(currentPlayer.Head, Brain.directions_possibles, turn_info)

        if (movement[Brain.counter] not in mouvementsPossibles):
            return mouvementsPossibles[0]
        else:
            Brain.counter += 1
            return movement[Brain.counter]
    
    def on_next_move(turn_info: TurnInformation):
        '''
        YOUR CODE GOES IN THIS FUNCTION. This is where your AI takes a decision on his next move.
        @param turn_info: Information from the current turn
        @return: The direction your AI chose as his next move.
        '''
        # remise aux directions de base
        Brain.directions_possibles = Brain.DIRECTIONS_POSSIBLES
        players = Brain.get_players_position(turn_info) 
        currentPlayer = players[str(turn_info.SelfId)]

        return Brain.MovementDeBase(currentPlayer, turn_info)
        #return Brain.ObstacleCheck(currentPlayer.Head, Brain.directions_possibles, turn_info)[0]

    def on_finalized(turn_info: TurnInformation):
        '''
        Once the game is finished, this method is triggered with the final state of the map. 
        It could be used to train the AI for example.
        @param turn_info: Information from the current turn
        '''
        print("the game has ended and the received id from the game server is {0} with the following map {1}".format(turn_info.SelfId, turn_info.Map)) 
