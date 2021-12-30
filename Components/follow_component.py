from Components.position_component import Position_Component
from aux.auxiliary_functions import distance_between_points
from Components.component import Component
import aux.constants as constants
from aux.a_star_pathfinding import astar
import operator

class Follow_Component(Component):
    follower_component : Position_Component #Follower position
    followed_component : Position_Component #Followed position
    known_grid : list #Map to avoid hitting objects
    path : list #Path to creature to avoid hitting objects


    def __init__(self,grid,follower,followed):
        self.follower_component = follower
        self.followed_component = followed
        self.known_grid = grid
        self.path = list()

    def get_percentage_walkable(self):
        walkable = 0
        total = 0
        (x,y) = self.follower_component.position
        for x_aux in range(x-1,x+2):
            for y_aux in range(y-1,y+2):
                if (x_aux != x or y_aux != x) and 0 <= x_aux < constants.MAPWIDTH and 0 <= y_aux < constants.MAPHEIGHT: 
                    if self.known_grid[y_aux][x_aux] == constants.TILENAMES['grass']:
                        walkable +=1
                    total +=1
        return walkable/total


    def next_in_path(self):
        direction_tuple = tuple(map(operator.sub,self.path[0][::-1],self.follower_component.position))
        decision = constants.INVERSE_DIRECTIONS[direction_tuple]
        self.path = self.path[1:]
        return decision

    def update(self,possible_decisions):
        
        if len(self.path) > 1:
            return self.next_in_path()
        
        follow_vector = tuple(map(operator.sub,self.followed_component.position,self.follower_component.position))
        distance = distance_between_points(self.follower_component.position,self.followed_component.position)
        if distance==0:
            return 'stop'
        normalized_vector = tuple(pos/distance for pos in follow_vector)
        direction_vector = tuple(round(pos) for pos in normalized_vector)
        next_position = tuple(map(operator.add,self.follower_component.position,direction_vector))

        if self.known_grid[next_position[1]][next_position[0]] != 0:
            walkable_percentage = self.get_percentage_walkable() #Returns the percentage of tiles around the creature that are walkable
            if walkable_percentage > 0.7: #If there is more than 70 percent walkable terrain around it we dont need to calculate a path he will figure it out
                possible_decisions.remove('stop')
                possible_directions = list(constants.DIRECTIONS[t] for t in possible_decisions)
                shortest = possible_directions[0]
                for dir in possible_directions[1:]:
                    dist_new = distance_between_points(normalized_vector, dir)
                    dist_short = distance_between_points(normalized_vector, shortest)
                    if dist_short > dist_new:
                        shortest = dir
                direction_vector = shortest
            else: #Else calculates path and follows 50 percent of the path to it
                self.path = astar(self.known_grid,self.follower_component.position,self.followed_component.position)
                if self.path == None:
                    return 'stop'
                self.path = self.path[1:]
                mid_index = int(len(self.path)/2)
                self.path = self.path[:mid_index]
                return self.next_in_path()

        decision = constants.INVERSE_DIRECTIONS[direction_vector]
        return decision
