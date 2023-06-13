# Cloth Sim

class Controller:
    def __init__(self):
        self.num_nodes = [10, 10] # [amt_horizontal, amt_vertical]
        self.nodes = [] # will be: 2d array - width = amt_horizontal, height = amt_vertical
        self.connections = [] # will be: 2d array - width = amt_horizontal, height = 2*amt_vertical - 1

        self.str_max_len = 5 # float

        self.grav_field_strength = 9.8 # float
        self.wind_force = [0, 0] # [x_force, y_force]

    def create_cloth(self):
        pass

class Node:
    def __init__(self, id_, coords, connections, grav):
        self.id = id_ # int
        self.conn = connections # [id, id, id, id]

        self.coord = coords # [x, y]
        self.const_force = [0, -grav] # [x_force, y_force]
        self.accel = [0, 0] # [x_accel, y_accel]

class Connection:
    def __init__(self, id_, coords, nodes):
        self.id = id_ # int
        self.node = nodes # [id, id]

        self.coord = coords # [[fr_x, fr_y], [end_x, end_y]]
        self.force = [0, 0] # [x_force, y_force]

    def update(self, max_len):
        pass

    def check_len(self, max_len):
        if math.sqrt((self.coord[0][1] - self.coord[1][1])**2 + (self.coord[0][1] - self.coord[1][1])**2) <= max_len:
            return True

        return False
