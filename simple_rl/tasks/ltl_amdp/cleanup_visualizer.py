# Python imports.
from __future__ import print_function
from collections import defaultdict

try:
    import pygame
except ImportError:
    print("Warning: pygame not installed (needed for visuals).")
import random
import sys

# Other imports.
# new version for ltl
from simple_rl.planning import ValueIteration
from simple_rl.utils import mdp_visualizer as mdpv


def draw_state(screen,
               cleanup_mdp,
               state,
               policy=None,
               action_char_dict={},
               show_value=False,
               agent=None,
               draw_statics=False,
               agent_shape=None):
    '''
    Args:
        screen (pygame.Surface)
        grid_mdp (MDP)
        state (State)
        show_value (bool)
        agent (Agent): Used to show value, by default uses VI.
        draw_statics (bool)
        agent_shape (pygame.rect)

    Returns:
        (pygame.Shape)
    '''

    print('\n\n\n\nInside draw state\n')
    # Make value dict.
    val_text_dict = defaultdict(lambda: defaultdict(float))

    # Make policy dict.
    policy_dict = defaultdict(lambda: defaultdict(str))

    # Prep some dimensions to make drawing easier.
    scr_width, scr_height = screen.get_width(), screen.get_height()
    width_buffer = scr_width / 10.0
    height_buffer = 30 + (scr_height / 10.0)  # Add 30 for title.

    width = cleanup_mdp.width
    height = cleanup_mdp.height

    cell_width = (scr_width - width_buffer * 2) / width
    cell_height = (scr_height - height_buffer * 2) / height

    print('Cell width: ', cell_width)
    print('Cell height: ', cell_height)
    print('Width buffer: ', width_buffer)
    print('Height buffer: ', height_buffer)



    # goal_locs = grid_mdp.get_goal_locs()
    # lava_locs = grid_mdp.get_lavacc_locs()
    font_size = int(min(cell_width, cell_height) / 4.0)
    reg_font = pygame.font.SysFont("CMU Serif", font_size)
    cc_font = pygame.font.SysFont("Courier", font_size * 2 + 2)

    # room_locs = [(x + 1, y + 1) for room in cleanup_mdp.rooms for (x, y) in room.points_in_room]
    door_locs = set([(door.x + 1, door.y + 1) for door in state.doors])

    # Draw the static entities.
    # print(draw_statics)
    # draw_statics = True
    # if draw_statics:
        # For each row:


    def draw_levels(i, j, level, cell_width, cell_height, width_buffer, height_buffer):
        x, y =  width_buffer + cell_height * i,  height_buffer + cell_width * j

        theta = math.pi/3
        #length = 80;  breadth = 40;
        length = cell_width; breadth = cell_height
        length = cell_height; breadth = cell_width
        p1 = (x, y); p2 = (x + length, y)
        p3 = (x + length - abs((breadth*math.cos(theta))), y + abs(int(breadth*math.sin(theta))))
        p4 = (x - abs(int(breadth*math.cos(theta))), y + abs(int(breadth*math.sin(theta))))

        point_list = [p1, p2, p3, p4]
        r = pygame.draw.lines(screen, (46, 49, 49), True, point_list, 1)


    ###############
    import math
    def draw_3D_room(i, j, level, cell_width, cell_height, width_buffer, height_buffer, theta, curr_x, curr_y, colour, room_name):
        print('Drawing room')

        x, y = curr_x, curr_y

        length = cell_height; breadth = cell_width
        p1 = (x, y); p2 = (x + length, y)
        p3 = (x + length - abs((breadth*math.cos(theta))), y + abs(int(breadth*math.sin(theta))))
        p4 = (x - abs(int(breadth*math.cos(theta))), y + abs(int(breadth*math.sin(theta))))

        point_list = [p1, p2, p3, p4]
        inner_points = [(p1[0] + 10, p1[1] + 10), (p2[0] - 10, p2[1] + 10), (p3[0] - 10, p3[1] -10), (p4[0] + 10, p4[1] - 10)]
        #r = pygame.draw.lines(screen, (255, 0, 0), True, inner_points, 13)

        r = pygame.draw.lines(screen, colour, True, inner_points, 13)

        r = pygame.draw.lines(screen, (46, 49, 49), True, point_list, 2)

        # connect elevator

        points_list = [[], [], [], []]
        #for points in points_list:
            #r = pygame.draw.lines(screen, (46, 49, 49), True, points, 2)

        return p4

    # (x, y, level)
    colour_dict = {'red': {2: [(0, 2), (1, 2), (0, 1), (1, 1)], 1: [], 0: []}, 'green': {2: [], 1: [], 0: []}, 'yellow': {2: [], 1: [], 0: []}}
    def draw_floor(level):
        print('\nDrawing floor\n')
        rooms_width, rooms_height = 4, 3
        theta = math.pi/3
        i, j = 0, 0
        curr_x, prev_x, curr_y, prev_y = 72, 72, 102, 102

        for i in range(rooms_width):
            for j in range(rooms_height):
            
                if j == 0: 
                    curr_x = prev_x = width_buffer + cell_height * i + 100
                    curr_y = prev_y = height_buffer + cell_width * j + 200*level

                else:
                    #curr_x = prev_x - abs((cell_height*math.cos(theta)))
                    curr_x, curr_y = prev_x, prev_y
                colour = (46, 49, 49)
                for key in colour_dict:
                    if (i, j) in colour_dict[key][level]:
                        colour = get_rgb(key)
                room_name = 'room_' + str(rooms_height*i+j)
                print(room_name)
                p4 = draw_3D_room(i, j, level, cell_width, cell_height, width_buffer, height_buffer, theta, curr_x, curr_y, colour, room_name)
                #prev_x = width_buffer + cell_height * i + 100
                prev_x, prev_y = p4[0], p4[1]

    

    draw_floor(0)
    draw_floor(1)
    draw_floor(2)

    return None




    for i in range(width):
        # For each column:
        for j in range(height):

            top_left_point = width_buffer + cell_width * i, height_buffer + cell_height * j
            r = pygame.draw.rect(screen, (46, 49, 49), top_left_point + (cell_width, cell_height), 3)

            # if grid_mdp.is_wall(i+1, grid_mdp.height - j):
            if (i + 1, height - j) not in cleanup_mdp.legal_states:
                # Draw the walls.
                top_left_point = width_buffer + cell_width * i + 5, height_buffer + cell_height * j + 5
                pygame.draw.rect(screen, (94, 99, 99), top_left_point + (cell_width - 10, cell_height - 10), 0)

            
            if (i + 1, height - j) in door_locs:
                # Draw door
                # door_color = (66, 83, 244)
                door_color = (0, 0, 0)
                top_left_point = width_buffer + cell_width * i + 5, height_buffer + cell_height * j + 5
                pygame.draw.rect(screen, door_color, top_left_point + (cell_width - 10, cell_height - 10), 0)

            else:
                room = cleanup_mdp.check_in_room(state.rooms, i + 1 - 1, height - j - 1)  # Minus 1 for inconsistent x, y
                if room:
                    top_left_point = width_buffer + cell_width * i + 5, height_buffer + cell_height * j + 5
                    room_rgb = _get_rgb(room.color)
                    pygame.draw.rect(screen, room_rgb, top_left_point + (cell_width - 10, cell_height - 10), 0)

            block = cleanup_mdp.find_block(state.blocks, i + 1 - 1, height - j - 1)
            # print(state)
            # print(block)

    pygame.display.flip()

    return agent_shape


def old_draw_state(screen,
               cleanup_mdp,
               state,
               policy=None,
               action_char_dict={},
               show_value=False,
               agent=None,
               draw_statics=False,
               agent_shape=None):
    '''
    Args:
        screen (pygame.Surface)
        grid_mdp (MDP)
        state (State)
        show_value (bool)
        agent (Agent): Used to show value, by default uses VI.
        draw_statics (bool)
        agent_shape (pygame.rect)

    Returns:
        (pygame.Shape)
    '''

    print('Inside draw state\n\n\n\n')
    # Make value dict.
    val_text_dict = defaultdict(lambda: defaultdict(float))
    if show_value:
        if agent is not None:
            # Use agent value estimates.
            for s in agent.q_func.keys():
                val_text_dict[s.x][s.y] = agent.get_value(s)
        else:
            # Use Value Iteration to compute value.
            vi = ValueIteration(cleanup_mdp)
            vi.run_vi()
            for s in vi.get_states():
                val_text_dict[s.x][s.y] = vi.get_value(s)

    # Make policy dict.
    policy_dict = defaultdict(lambda: defaultdict(str))
    if policy:
        vi = ValueIteration(cleanup_mdp)
        vi.run_vi()
        for s in vi.get_states():
            policy_dict[s.x][s.y] = policy(s)

    # Prep some dimensions to make drawing easier.
    scr_width, scr_height = screen.get_width(), screen.get_height()
    width_buffer = scr_width / 10.0
    height_buffer = 30 + (scr_height / 10.0)  # Add 30 for title.

    width = cleanup_mdp.width
    height = cleanup_mdp.height

    cell_width = (scr_width - width_buffer * 2) / width
    cell_height = (scr_height - height_buffer * 2) / height
    # goal_locs = grid_mdp.get_goal_locs()
    # lava_locs = grid_mdp.get_lavacc_locs()
    font_size = int(min(cell_width, cell_height) / 4.0)
    reg_font = pygame.font.SysFont("CMU Serif", font_size)
    cc_font = pygame.font.SysFont("Courier", font_size * 2 + 2)

    # room_locs = [(x + 1, y + 1) for room in cleanup_mdp.rooms for (x, y) in room.points_in_room]
    door_locs = set([(door.x + 1, door.y + 1) for door in state.doors])

    # Draw the static entities.
    # print(draw_statics)
    # draw_statics = True
    # if draw_statics:
        # For each row:



    for i in range(width):
        # For each column:
        for j in range(height):

            top_left_point = width_buffer + cell_width * i, height_buffer + cell_height * j
            r = pygame.draw.rect(screen, (46, 49, 49), top_left_point + (cell_width, cell_height), 3)

            '''
            # if policy and not grid_mdp.is_wall(i+1, height - j):
            if policy and (i + 1, height - j) in cleanup_mdp.legal_states:
                a = policy_dict[i + 1][height - j]
                if a not in action_char_dict:
                    text_a = a
                else:
                    text_a = action_char_dict[a]
                text_center_point = int(top_left_point[0] + cell_width / 2.0 - 10), int(
                    top_left_point[1] + cell_height / 3.0)
                text_rendered_a = cc_font.render(text_a, True, (46, 49, 49))
                screen.blit(text_rendered_a, text_center_point)

            # if show_value and not grid_mdp.is_wall(i+1, grid_mdp.height - j):
            if show_value and (i + 1, height - j) in cleanup_mdp.legal_states:
                # Draw the value.
                val = val_text_dict[i + 1][height - j]
                color = mdpv.val_to_color(val)
                pygame.draw.rect(screen, color, top_left_point + (cell_width, cell_height), 0)
                # text_center_point = int(top_left_point[0] + cell_width/2.0 - 10), int(top_left_point[1] + cell_height/7.0)
                # text = str(round(val,2))
                # text_rendered = reg_font.render(text, True, (46, 49, 49))
                # screen.blit(text_rendered, text_center_point)
            '''

            # if grid_mdp.is_wall(i+1, grid_mdp.height - j):
            if (i + 1, height - j) not in cleanup_mdp.legal_states:
                # Draw the walls.
                top_left_point = width_buffer + cell_width * i + 5, height_buffer + cell_height * j + 5
                pygame.draw.rect(screen, (94, 99, 99), top_left_point + (cell_width - 10, cell_height - 10), 0)

            
            if (i + 1, height - j) in door_locs:
                # Draw door
                # door_color = (66, 83, 244)
                door_color = (0, 0, 0)
                top_left_point = width_buffer + cell_width * i + 5, height_buffer + cell_height * j + 5
                pygame.draw.rect(screen, door_color, top_left_point + (cell_width - 10, cell_height - 10), 0)

            else:
                room = cleanup_mdp.check_in_room(state.rooms, i + 1 - 1, height - j - 1)  # Minus 1 for inconsistent x, y
                if room:
                    top_left_point = width_buffer + cell_width * i + 5, height_buffer + cell_height * j + 5
                    room_rgb = _get_rgb(room.color)
                    pygame.draw.rect(screen, room_rgb, top_left_point + (cell_width - 10, cell_height - 10), 0)

            block = cleanup_mdp.find_block(state.blocks, i + 1 - 1, height - j - 1)
            # print(state)
            # print(block)


            '''
            # ROMA: to draw objects if needed
            if block:
                circle_center = int(top_left_point[0] + cell_width / 2.0), int(top_left_point[1] + cell_height / 2.0)
                block_rgb = _get_rgb(block.color)
                pygame.draw.circle(screen, block_rgb, circle_center, int(min(cell_width, cell_height) / 4.0))
            
            # Current state.
            # ROMA: to draw the agent if needed
            if not show_value and (i + 1, height - j) == (state.x + 1, state.y + 1) and agent_shape is None:
                tri_center = int(top_left_point[0] + cell_width / 2.0), int(top_left_point[1] + cell_height / 2.0)
                agent_shape = _draw_agent(tri_center, screen, base_size=min(cell_width, cell_height) / 2.5 - 8)
            '''

    '''
    if agent_shape is not None:
        # Clear the old shape.
        pygame.draw.rect(screen, (255, 255, 255), agent_shape)
        top_left_point = width_buffer + cell_width * ((state.x + 1) - 1), height_buffer + cell_height * (
                height - (state.y + 1))
        tri_center = int(top_left_point[0] + cell_width / 2.0), int(top_left_point[1] + cell_height / 2.0)

        # Draw new.
        # if not show_value or policy is not None:
        agent_shape = _draw_agent(tri_center, screen, base_size=min(cell_width, cell_height) / 2.5 - 16)
    '''
    pygame.display.flip()

    return agent_shape


def _draw_agent(center_point, screen, base_size=20):
    '''
    Args:
        center_point (tuple): (x,y)
        screen (pygame.Surface)

    Returns:
        (pygame.rect)
    '''
    tri_bot_left = center_point[0] - base_size, center_point[1] + base_size
    tri_bot_right = center_point[0] + base_size, center_point[1] + base_size
    tri_top = center_point[0], center_point[1] - base_size
    tri = [tri_bot_left, tri_top, tri_bot_right]
    tri_color = (98, 140, 190)
    return pygame.draw.polygon(screen, tri_color, tri)


def _get_rgb(color):
    '''
    :param color: A String
    :return: triple that represents the rbg color
    '''
    color = color.lower().strip()
    if color == "red":
        return 255, 0, 0
    if color == "blue":
        return 0, 0, 255
    if color == "green":
        return 0, 255, 0
    if color == "yellow":
        return 255, 255, 0
    if color == "purple":
        return 117, 50, 219
    if color == "orange":
        return 237, 138, 18
    if color == "pink":
        return 247, 2, 243

def get_rgb(color):
    '''
    :param color: A String
    :return: triple that represents the rbg color
    '''
    color = color.lower().strip()
    if color == "red":
        return 255, 0, 0
    if color == "blue":
        return 0, 0, 255
    if color == "green":
        return 0, 255, 0
    if color == "yellow":
        return 255, 255, 0
    if color == "purple":
        return 117, 50, 219
    if color == "orange":
        return 237, 138, 18
    if color == "pink":
        return 247, 2, 243


