# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# or in the "license" file accompanying this file. This file is distributed 
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either 
# express or implied. See the License for the specific language governing 
# permissions and limitations under the License.

import numpy as np
import random

from rllib_inference.src.heuristics_util import move_towards, avoid_body

class MyBattlesnakeHeuristics:
    '''
    The BattlesnakeHeuristics class allows you to define handcrafted rules of the snake.
    '''
    FOOD_INDEX = 0
    def __init__(self):
        pass
    
    def aggressive(self, state, snake_id, turn_count, health, json):
        your_snake_body = json["you"]["body"]
        i, j = your_snake_body[0]["y"], your_snake_body[0]["x"]
        if -1 in state:
            i, j = i+1, j+1
            
        your_health = health[snake_id]
        your_snake = None
        for snake in json["board"]["snakes"]:
            if snake["id"] == snake_id:
                your_snake = snake
                break
                
        # should not happen, snake_id not found.
        if your_snake == None:
            return 0

        # aggressive. Hunt snakes
        # get snakes by sorted order.
        snakes = sorted(json["board"]["snakes"], key = lambda x: len(x["body"]))
        
        targets = list(filter(lambda x: len(x["body"]) < len(your_snake_body) and x["id"] != your_snake["id"], snakes))
        
        best_target = None
        min_dist = 10000
        #check mindist
        for target in targets:
            t_x = target["body"][0]["x"]
            t_y = target["body"][0]["y"]
            
            if -1 in state:
                t_x, t_y = t_x + 1, t_y + 1
            
            if (t_x - j) ** 2 + (t_y - i) ** 2 < min_dist:
                best_target = target
                min_dist = (t_x - j) ** 2 + (t_y - i)
        
        if best_target == None:
            return None
        
        target_body = best_target["body"]
        direction = move_towards({"x": j, "y": i}, target_body)
        avoid = avoid_body({"x": j, "y": i}, your_snake_body, target_body)
        for d in avoid:
            if d in direction:
                direction.remove(d)
        return direction, "moving towards snake %s".format(best_target["id"])
        
    def go_to_food_if_close(self, state, json):
        '''
        Example heuristic to move towards food if it's close to you.
        '''
        # Get the position of the snake head
        your_snake_body = json["you"]["body"]
        i, j = your_snake_body[0]["y"], your_snake_body[0]["x"]
        
        # Set food_direction towards food
        food = state[:, :, self.FOOD_INDEX]
        
        # Note that there is a -1 border around state so i = i + 1, j = j + 1
        if -1 in state:
            i, j = i+1, j+1
        
        food_direction = None
        if food[i-1, j] == 1:
            food_direction = 0 # up
        if food[i+1, j] == 1:
            food_direction = 1 # down
        if food[i, j-1] == 1:
            food_direction = 2 # left
        if food[i, j+1] == 1:
            food_direction = 3 # right
        return food_direction
    
    def run(self, state, snake_id, turn_count, health, json, action):
        '''
        The main function of the heuristics.
        
        Parameters:
        -----------
        `state`: np.array of size (map_size[0]+2, map_size[1]+2, 1+number_of_snakes)
        Provides the current observation of the gym.
        Your target snake is state[:, :, snake_id+1]
    
        `snake_id`: int
        Indicates the id where id \in [0...number_of_snakes]
    
        `turn_count`: int
        Indicates the number of elapsed turns
    
        `health`: dict
        Indicates the health of all snakes in the form of {int: snake_id: int:health}
        
        `json`: dict
        Provides the same information as above, in the same format as the battlesnake engine.

        `action`: np.array of size 4
        The qvalues of the actions calculated. The 4 values correspond to [up, down, left, right]
        '''
        log_string = ""
        # The default `best_action` to take is the one that provides has the largest Q value.
        # If you think of something else, you can edit how `best_action` is calculated
        best_action = int(np.argmax(action))
                
        # Example heuristics to eat food that you are close to.
        if health[snake_id] < 30:
            food_direction = self.go_to_food_if_close(state, json)
            if food_direction:
                best_action = food_direction
                log_string = "Went to food if close."
        aggro = self.aggressive(state, snake_id, turn_count, health, json)
        if aggro != None and len(aggro[0]) != 0:
            best_action = random.choice(aggro[0])
            log_string = aggro[1] + str(best_action)

        # TO DO, add your own heuristics
        
        assert best_action in [0, 1, 2, 3], "{} is not a valid action.".format(best_action)
        return best_action, log_string
