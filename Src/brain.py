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
    step_compter = 0
    DIRECTIONS_POSSIBLES = [Direction._UP, Direction._DOWN, Direction._RIGHT, Direction._LEFT, Direction._NONE]
    directions_possibles = DIRECTIONS_POSSIBLES

    #remove direction "removeDirection" from array
    #Brain.directions_possibles.pop(directions_possibles.index(removeDirection))

    #MUR
    

    #sates : (xplore : augment the area, attack:path finding to kill, defend : still /wtv.)
    #but:
    #PlayerPosition.Head = vector2()
    #PlayerPosition.Body = []
    #PlayerPosition.Neck = []
    def wallcheck(player_position_head : Vector2, possible_actions, turn_info):
        new_possible_actions = []
        map2d = np.array(turn_info.Map).reshape((turn_info.MapWidth, turn_info.MapWidth))
        print(map2d)
        map2d = map2d.tolist()
        for action in possible_actions:
            # Check if wall up.
            if action == Direction._UP:
                if map2d[player_position_head.Y + 1][player_position_head.X] != 'W':
                    new_possible_actions.append(action)
                    print('UP')
            
            # Check if wall down.
            elif action == Direction._DOWN:
                if map2d[player_position_head.Y - 1][player_position_head.X] != 'W':
                    new_possible_actions.append(action)
                    print('DOWN')
            # Check if wall left.
            elif action == Direction._LEFT:
                if map2d[player_position_head.Y][player_position_head.X - 1] != 'W':
                    new_possible_actions.append(action)
                    print('LEFT')
            # Check if wall right.
            elif action == Direction._RIGHT:
                if map2d[player_position_head.Y][player_position_head.X + 1] != 'W':
                    new_possible_actions.append(action)
                    print('RIGHT')
        print(len(new_possible_actions))  
        return new_possible_actions
    
    def neckcheck(player_position_head : Vector2, possible_actions, turn_info):
        #str(turn_info.SelfId)
        new_possible_actions = []
        map2d = np.array(turn_info.Map).reshape((turn_info.MapWidth, turn_info.MapWidth))
        map2d = map2d.tolist()
        for action in possible_actions:
            # Check if wall up.
            if action == Direction._UP:
                if map2d[player_position_head.Y + 1][player_position_head.X] != 'p3':
                    new_possible_actions.append(action)
                    print('UP')
            
            # Check if wall down.
            elif action == Direction._DOWN:
                if map2d[player_position_head.Y - 1][player_position_head.X] != 'p3':
                    new_possible_actions.append(action)
                    print('DOWN')
            # Check if wall left.
            elif action == Direction._LEFT:
                if map2d[player_position_head.Y][player_position_head.X - 1] != 'p3':
                    new_possible_actions.append(action)
                    print('LEFT')
            # Check if wall right.
            elif action == Direction._RIGHT:
                if map2d[player_position_head.Y][player_position_head.X + 1] != 'p3':
                    new_possible_actions.append(action)
                    print('RIGHT')
        print(len(new_possible_actions))  
        return new_possible_actions

    # def calculate_risk(dir):
    
    
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

    
    def on_next_move(turn_info: TurnInformation):
        Brain.directions_possibles = Brain.DIRECTIONS_POSSIBLES
        '''
        YOUR CODE GOES IN THIS FUNCTION. This is where your AI takes a decision on his next move.
        @param turn_info: Information from the current turn
        @return: The direction your AI chose as his next move.
        '''
        players = Brain.get_players_position(turn_info) 
        #print("La position de la tete est: ", players[str(turn_info.SelfId)].Head.X, players[str(turn_info.SelfId)].Head.Y)
        
        #print("the game server wants to know your next move and you have the following informations : the id is {0} and the current map is {1} ".format(turn_info.SelfId, turn_info.Map))
        # As a default we put that the direction to UP.
        # new_possibles = wallcheck(Brain.directions_possibles)
        Brain.step_compter+=1
        currentPlayer = players[str(turn_info.SelfId)]
        #return Brain.directions_possibles[Brain.step_compter%len(Brain.directions_possibles)]
        a = Brain.wallcheck(currentPlayer.Head, Brain.directions_possibles, turn_info)
        b = Brain.neckcheck(currentPlayer.Head, a, turn_info)
        (b[0],b[1]) = (b[1],b[0])
        return b[0]
        
    def on_finalized(turn_info: TurnInformation):
        '''
        Once the game is finished, this method is triggered with the final state of the map. 
        It could be used to train the AI for example.
        @param turn_info: Information from the current turn
        '''
        print("the game has ended and the received id from the game server is {0} with the following map {1}".format(turn_info.SelfId, turn_info.Map)) 
