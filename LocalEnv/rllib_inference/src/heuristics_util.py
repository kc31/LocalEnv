def move_towards(snake_head, target_snake_body, state_has_border = True):
    t_x = target_snake_body[0]["x"]
    t_y = target_snake_body[0]["y"]
    
    if state_has_border == True:
        t_x, t_y = t_x + 1, t_y + 1
    target_snake_head = target_snake_body[0]
    directions = []
    if snake_head["x"] < t_x:
        directions.append(3)
    if snake_head["x"] > t_x:
        directions.append(2)
    if snake_head["y"] < t_y:
        directions.append(0)
    if snake_head["y"] > t_y:
        directions.append(1)
    return directions

def avoid_body(snake_head, your_snake_body, target_snake_body, state_has_border = True, distance = 1):
    avoid = set()
    for part in target_snake_body:
        p_x, p_y = part["x"], part["y"]
        if state_has_border == True:
            p_x, p_y = part["x"] + 1, part["y"] + 1
        
        if (snake_head["x"] - p_x) < 0 and abs(snake_head["x"] - p_x) <= distance:
            avoid.add(3)
        if (snake_head["x"] - p_x) > 0 and abs(snake_head["x"] - p_x) <= distance:
            avoid.add(2)
        if (snake_head["y"] - p_y) < 0 and abs(snake_head["y"] - p_y) <= distance:
            avoid.add(0)
        if (snake_head["y"] - p_y) > 0 and abs(snake_head["y"] - p_y) <= distance:
            avoid.add(1)
            
    for part in your_snake_body[1:]:
        p_x, p_y = part["x"], part["y"]
        if state_has_border == True:
            p_x, p_y = part["x"] + 1, part["y"] + 1
        
        if (snake_head["x"] - p_x) < 0 and abs(snake_head["x"] - p_x) <= distance:
            avoid.add(3)
        if (snake_head["x"] - p_x) > 0 and abs(snake_head["x"] - p_x) <= distance:
            avoid.add(2)
        if (snake_head["y"] - p_y) < 0 and abs(snake_head["y"] - p_y) <= distance:
            avoid.add(0)
        if (snake_head["y"] - p_y) > 0 and abs(snake_head["y"] - p_y) <= distance:
            avoid.add(1)
    return avoid
