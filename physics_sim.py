""" Cloth Sim """

import math
import random
from copy import deepcopy
import pygame

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Cloth Sim")

class Controller:
    def __init__(self):
        self.num_nodes = [3, 3] # [amt_horizontal, amt_vertical]
        self.nodes = [] # will be: 2d array - width = amt_horizontal, height = amt_vertical
        self.x_facing_connections = []
        # will be: 2d array - width = amt_horizontal - 1, height = amt_vertical
        self.y_facing_connections = []
        # will be: 2d array - width = amt_horizontal, height = amt_vertical - 1

        self.stat_points_dist = 12 # float
        self.str_max_len = 5 # float
        self.spring_constant = 10 # float

        self.node_mass = 0.05
        self.node_rad = 5

        self.grav_force = [0, -9.8] # float
        self.wind_force = [5, 5] # [x_force, y_force]
        #self.wind_cycle = 5 # float (s)
        self.wind_ferocity = 3 # float 0 -> 1

        self.x_percent_takeover = 0.6
        self.y_percent_takeover = 0.6

        self.x_useable = SCREEN_WIDTH * self.x_percent_takeover
        self.y_useable = SCREEN_HEIGHT * self.y_percent_takeover

        self.x_coord_buffer = SCREEN_WIDTH * (1 - self.x_percent_takeover) // 2
        self.y_coord_buffer = SCREEN_HEIGHT * (1 - self.y_percent_takeover) // 2

    def create_cloth(self):
        """
        Initialises cloth nodes and connections
        """
        for i in range(self.num_nodes[1]):
            for j in range(self.num_nodes[0]):
                node_id = j + i * self.num_nodes[0]

                x_connection = j + i * (self.num_nodes[0] - 1)
                y_connection = j + i * self.num_nodes[0]

                connections = [x_connection - 1 if j != 0 else None,
                               x_connection if j != self.num_nodes[0] - 1 else None,
                               y_connection - self.num_nodes[0] if i != 0 else None,
                               y_connection if i != self.num_nodes[1] - 1 else None]

                x_conn_nodes = [node_id, node_id + 1]
                y_conn_nodes = [node_id, node_id + self.num_nodes[0]]


                x_coord = self.stat_points_dist / (self.num_nodes[0] - 1) * j
                y_coord = i * self.str_max_len

                self.nodes.append(
                    Node(node_id, connections, [x_coord, y_coord]))

                if j != self.num_nodes[0] - 1:
                    self.x_facing_connections.append(
                        Connection(x_connection, x_conn_nodes, [[None, None], [None, None]]))

                if i != self.num_nodes[1] - 1:
                    self.y_facing_connections.append(
                        Connection(y_connection, y_conn_nodes, [[None, None], [None, None]]))

    def update(self, frame_time):
        current_wind = self.adjust_wind(frame_time)

        # Draw nodes to the screen
        for node in self.nodes:
            node.update(self.stat_points_dist, self.str_max_len * (self.num_nodes[1] - 1),
                        self.x_useable, self.y_useable, self.x_coord_buffer, self.y_coord_buffer,
                        self.node_rad,
                        [self.grav_force[0] + current_wind[0],
                         self.grav_force[1] + current_wind[1]])

    def adjust_wind(self, frame_time):
        current_wind = deepcopy(self.wind_force)

        current_wind[0] *= random.random()**self.wind_ferocity
        current_wind[1] *= random.random()**self.wind_ferocity

        return current_wind

    def __str__(self):
        string = ""
        string += "All Nodes:"
        for node in self.nodes:
            string += f"\n{node}"

        string += "\n\nAll X Facing Connections:"
        for conn in self.x_facing_connections:
            string += f"\n{conn}"

        string += "\n\nAll Y Facing Connections:"
        for conn in self.y_facing_connections:
            string += f"\n{conn}"

        return string

class Node:
    def __init__(self, id_, connections, coords):
        self.id_ = id_ # [x/y facing, id]
        self.conn = connections # [id, id, id, id]

        self.coord = coords # [x, y]
        self.accel = [0, 0] # [x_acceleration, y_acceleration]
        self.velo = [0, 0] # [x_velocity, y_velocity]

    def update(self, max_x, max_y,
               x_useable, y_useable, x_coord_buffer, y_coord_buffer,
               node_rad, current_force):
        self.calc_coord()
        self.draw_node(max_x, max_y, x_useable, y_useable, x_coord_buffer, y_coord_buffer, node_rad)

        self.calc_force(current_force)

    def calc_velo(self):
        pass

    def calc_coord(self):
        pass

    def calc_force(self, current_force):
        for connection in controller.x_facing_connections:
            if connection.node[0] == self.id_:
                current_force[0] += connection.force[0][0]
                current_force[1] += connection.force[0][1]
            elif connection.node[1] == self.id_:
                current_force[0] += connection.force[1][0]
                current_force[1] += connection.force[1][1]

        for connection in controller.y_facing_connections:
            if connection.node[0] == self.id_:
                current_force[0] += connection.force[0][0]
                current_force[1] += connection.force[0][1]
            elif connection.node[1] == self.id_:
                current_force[0] += connection.force[1][0]
                current_force[1] += connection.force[1][1]

    def calc_accel(self):
        pass

    def draw_node(self, max_x, max_y,
                  x_useable, y_useable, x_coord_buffer, y_coord_buffer, node_rad):
        """
        Draws the node to the screen
        """
        x = self.coord[0] / max_x * x_useable + x_coord_buffer
        y = self.coord[1] / max_y * y_useable + y_coord_buffer
        pygame.draw.circle(win, (255, 255, 255), [x, y], node_rad)

    def __str__(self):
        return f"id: {self.id_}, conns: {self.conn}"

class Connection:
    def __init__(self, id_, nodes, coords):
        self.id_ = id_ # int
        self.node = nodes # [id, id]

        self.coord = coords # [[fr_x, fr_y], [end_x, end_y]]
        self.force = [[0, 0], [0, 0]] # [[fr_x_force, fr_y_force], [end_x_force, end_y_force]]

    def update(self, max_len):
        pass

    def get_coords(self):
        pass

    def calc_forces(self, max_len, spring_constant):
        spring_force = self.calc_spring_force(max_len, spring_constant)
        change_x = self.coord[0][0] - self.coord[1][0]
        change_y = self.coord[0][1] - self.coord[1][1]
        x_spring_force = spring_force / math.sqrt((change_y / change_x)**2 + 1)
        y_spring_force = x_spring_force * (change_y / change_x)

    def calc_spring_force(self, max_len, spring_contant):
        extension = self.get_len() - max_len
        return spring_contant * extension

    def get_len(self):
        return math.sqrt((self.coord[0][1] - self.coord[1][1])**2 + (
            self.coord[0][1] - self.coord[1][1])**2)

    def __str__(self):
        return f"id: {self.id_}, nodes: {self.node}"

class Main:
    def __init__(self):
        self.run = True

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.frame_time = 0

    def game_loop(self):
        controller.create_cloth()

        while self.run:
            self.frame_time = self.clock.tick(self.fps)

            controller.update(self.frame_time)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

        pygame.quit()

def calc():
    coord = [[1,1], [5,2]]
    spring_force = 5
    change_x = coord[0][0] - coord[1][0]
    change_y = coord[0][1] - coord[1][1]
    x_spring_force = spring_force / math.sqrt((change_y / change_x)**2 + 1)
    y_spring_force = x_spring_force * (change_y / change_x)
    print(x_spring_force)
    print(y_spring_force)

calc()

main = Main()
controller = Controller()
main.game_loop()
