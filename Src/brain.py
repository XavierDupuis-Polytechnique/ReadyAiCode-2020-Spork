from Src.Helpers.singleton import Singleton
from Src.Helpers.brainHelper import get_other_players_position
from Src.Models.direction import Direction
from Src.Models.turnInformation import TurnInformation
from Src.Models.playerPosition import PlayerPosition
from Src.Models.vector2 import Vector2
import numpy as np
import random


class Brain(metaclass=Singleton):
    # Random variable globale
    #MEMO playerID : turn_info.SelfId, map : turn_info.Map
    counter = 0
    DIRECTIONS_POSSIBLES = [Direction._UP, Direction._DOWN, Direction._RIGHT, Direction._LEFT, Direction._NONE]
    directions_possibles = DIRECTIONS_POSSIBLES
    retournerBody = False
    nombreNeck = 3
    updateCounter1 = False
    updateCounter2 = False

    def ObstacleCheck(player_position_head : Vector2, possible_actions, turn_info):
        new_possible_actions = []
        map2d = np.array(turn_info.Map).reshape((turn_info.MapWidth, turn_info.MapWidth))
        #print(map2d)
        map2d = map2d.tolist()
        #print(player_position_head.X,player_position_head.Y)
        
        j = turn_info.MapWidth - player_position_head.Y - 1
        i = player_position_head.X
        #print(i, j)
        for action in possible_actions:
            # Check if wall up.
            if action == Direction._UP:
                if (map2d[j - 1][i] != 'W') and (map2d[j - 1][i] != ('p' + str(turn_info.SelfId))) and (map2d[j - 1][i] != 'B') and (map2d[j - 1][i] != 'I') and (map2d[j - 1][i] != 'D'):
                    new_possible_actions.append(action)
                    print('UP')
            # Check if wall down.
            elif action == Direction._DOWN:
                if (map2d[j + 1][i] != 'W') and (map2d[j + 1][i] != ('p' + str(turn_info.SelfId))) and (map2d[j + 1][i] != 'B') and (map2d[j + 1][i] != 'I') and (map2d[j + 1][i] != 'D'):
                    new_possible_actions.append(action)
                    print('DOWN')
            # Check if wall left.
            elif action == Direction._LEFT:
                if (map2d[j][i- 1] != 'W') and (map2d[j][i - 1] != ('p' + str(turn_info.SelfId))) and (map2d[j][i - 1] != 'B') and (map2d[j][i - 1] != 'I') and (map2d[j][i - 1] != 'D'):
                    new_possible_actions.append(action)
                    print('LEFT')
            # Check if wall right.
            elif action == Direction._RIGHT:
                if (map2d[j][i + 1] != 'W') and (map2d[j][i + 1] != ('p' + str(turn_info.SelfId))) and (map2d[j][i + 1] != 'B') and (map2d[j][i + 1] != 'I') and (map2d[j][i + 1] != 'D'):
                    new_possible_actions.append(action)
                    print('RIGHT')
        #print(len(new_possible_actions))  
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

    def IndiceBody(turn_information):
        player = Brain.get_players_position(turn_information)[str(turn_information.SelfId)]
        DistanceX =200
        DistanceY =200
        DistanceTotal = DistanceX + DistanceY
        DistanceTestX = 0
        DistanceTestY = 0
        DistanceTotalTest = DistanceTestX + DistanceTestY
        indice = 0
        for i in range(len(player.Body)):
            DistanceTestX = player.Head.X - player.Body[i].X
            DistanceTestY = player.Head.Y - player.Body[i].Y
            DistanceTotalTest = DistanceTestX + DistanceTestY
            if(DistanceTotalTest < DistanceTotal):
                DistanceTotal = DistanceTotalTest
                indice = i
        return indice

    def returnToBody(mouvementsPossibles : list, turn_info):

        DistanceX = Brain.get_players_position(turn_info)[str(turn_info.SelfId)].Body[Brain.IndiceBody(turn_info)].X - Brain.get_players_position(turn_info)[str(turn_info.SelfId)].Head.X
        DistanceY = Brain.get_players_position(turn_info)[str(turn_info.SelfId)].Body[Brain.IndiceBody(turn_info)].Y - Brain.get_players_position(turn_info)[str(turn_info.SelfId)].Head.Y
        
        if(DistanceX > 0):
            if Direction._RIGHT in mouvementsPossibles:
                return Direction._RIGHT
            elif (DistanceY > 0):
                if Direction._UP in mouvementsPossibles:
                    return Direction._UP
                elif Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                else:
                    return Direction._LEFT
            elif (DistanceY < 0):
                if Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                elif Direction._UP in mouvementsPossibles:
                    return Direction._UP
                else:
                    return Direction._LEFT
            else:
                if Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                elif Direction._UP in mouvementsPossibles:
                    return Direction._UP
                else:
                    return Direction._RIGHT
            
        elif(DistanceX < 0):
            if Direction._LEFT in mouvementsPossibles:
                return Direction._LEFT
            elif (DistanceY > 0):
                if Direction._UP in mouvementsPossibles:
                    return Direction._UP
                elif Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                else:
                    return Direction._RIGHT
            elif (DistanceY < 0):
                if Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                elif Direction._UP in mouvementsPossibles:
                    return Direction._UP
                else:
                    return Direction._RIGHT
            else:
                if Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                elif Direction._UP in mouvementsPossibles:
                    return Direction._UP
                else:
                    return Direction._LEFT
            
        elif (DistanceX == 0):
            if (DistanceY < 0):
                if Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                elif Direction._UP in mouvementsPossibles:
                    return Direction._UP
                elif Direction._LEFT in mouvementsPossibles:
                    return Direction._LEFT
                else:
                    return Direction._RIGHT
            elif (DistanceY > 0):
                if Direction._UP in mouvementsPossibles:
                    return Direction._UP
                elif Direction._DOWN in mouvementsPossibles:
                    return Direction._DOWN
                elif Direction._LEFT in mouvementsPossibles:
                    return Direction._LEFT
                else:
                    return Direction._RIGHT        

    def DistanceBody(turn_information):
        player = Brain.get_players_position(turn_information)[str(turn_information.SelfId)]
        return len(player.Neck)

    def on_next_move(turn_info: TurnInformation):

        currentPlayer = Brain.get_players_position(turn_info)[str(turn_info.SelfId)]

        # Counter Update 1
        if(Brain.counter >= 10 and Brain.updateCounter1 != True):
            Brain.nombreNeck -= 1
            Brain.updateCounter1 = True
        
        # Counter Update 2
        if(Brain.counter >= 15 and Brain.updateCounter2 != True) :
            Brain.nombreNeck -= 1
            Brain.updateCounter2 = True
        
        print(Brain.DistanceBody(turn_info))


        if(Brain.DistanceBody(turn_info) >= 2):
            Brain.retournerBody = True

        if(Brain.DistanceBody(turn_info) == 0):
            Brain.retournerBody = False

        print("the game server wants to know your next move and you have the following informations : the id is {0} and the current map is {1} ".format(turn_info.SelfId, turn_info.Map)) 
        
        while Brain.retournerBody == True:
            print("Je dois retourner au BODY")
            return Brain.returnToBody(Brain.ObstacleCheck(currentPlayer.Head, Brain.DIRECTIONS_POSSIBLES, turn_info), turn_info)
        
        return random.choice(Brain.ObstacleCheck(currentPlayer.Head, Brain.DIRECTIONS_POSSIBLES, turn_info))        


    def on_finalized(turn_info: TurnInformation):
        Brain.counter = 0
        Brain.updateCounter1 = False
        Brain.updateCounter2 = False
        '''
        Once the game is finished, this method is triggered with the final state of the map. 
        It could be used to train the AI for example.
        @param turn_info: Information from the current turn
        '''
        print("the game has ended and the received id from the game server is {0} with the following map {1}".format(turn_info.SelfId, turn_info.Map)) 
