import numpy as np
import scipy.constants as cst

PLANET_DICT = {'Sun': (2.e30, np.array([0., 0., 0.]), np.array([0., 0., 0.])),
               'Earth': (6.e24, np.array([1.5e11, 0, 0]), np.array([0., 3.e4, 0])),
               'Jupiter': (2.e27, np.array([(5.2 * 1.5e11), 0., 0.]), np.array([0., 1.3e4, 0.])),
               'Test': (1.e29, np.array([(3.2 * 1.5e11), 0., 0.]), np.array([0., 2.3e4, 0.])),
               'Pluto?': (6.e23, np.array([(40. * 1.5e11), 0., 0.]), np.array([0., 4.e3, 0.])),
               }


class Planet:
    def __init__(self, name, (mass, position, velocity)):
        self.name = name  # String
        self.mass = mass  # Float
        self.position = position  # Numpy ndarray
        self.velocity = velocity  # Numpy ndarray
        self.forces = {}  # {'Mars': False, 'Earth': ndarray}
        self.init_forces()
        self.history = [[], []]

    def calculate_all_interactions(self, planet_list):
        for planet in planet_list:
            if planet.name != self.name:
                self.forces[planet.name] = self.calculate_interaction(planet)

    def calculate_interaction(self, other_planet):
        if isinstance(other_planet.forces[self.name], bool):
            d, direction = distance(self, other_planet)
            gravity_force = cst.G * self.mass * other_planet.mass / (d ** 2.)
            gravity_vector = direction * gravity_force
            return gravity_vector
        else:
        	return -1. * other_planet.forces[self.name]

    def get_acceleration(self, other_planet_name):
        force = self.forces[other_planet_name]
        acceleration = force / self.mass
        return acceleration

    def update(self, dt):
        accelerations = np.zeros([0, 3])
        for planet in self.forces:
            if planet == self.name:
                continue
            a = self.get_acceleration(planet)
            accelerations = np.concatenate([accelerations, [a]])
        net_acceleration = np.sum(accelerations, axis=0)
        dv = net_acceleration * dt
        self.velocity += dv
        self.position += self.velocity * dt
        # print self.name
        # print 'acceleration', net_acceleration
        # print 'velocity', self.velocity
        # print 'position', self.position
        # useless = raw_input()

    def init_forces(self):
        for name in PLANET_DICT:
            self.forces[name] = False

    def reset_forces(self):
        self.init_forces()

    def record(self, offset):
        diff = self.position - offset
        self.history[0].append(diff[0])
        self.history[1].append(diff[1])


def distance(planet1, planet2):
    assert isinstance(planet1, Planet)
    assert isinstance(planet2, Planet)
    x1 = planet1.position
    x2 = planet2.position
    direction = x2 - x1
    d = np.sqrt(np.sum(direction ** 2.))
    unit_vector = direction / d
    return d, unit_vector
