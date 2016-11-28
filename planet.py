import numpy as np
import scipy.constants as cst

PLANET_DICT = {
    'Sun': (1.988544E30, np.array([0., 0., 0.]), np.array([0., 0., 0.])),
    'Jupiter': (1.89813E27, np.array([-5.399632, -7.643480E-1, 1.239975E-1]), np.array([9.684588E-4, -7.121879E-3, 7.927815E-6])),
}


def prepare_test():
    test_mass = 1E2
    test_position = (PLANET_DICT['Jupiter'][1] * ((1. / 3.) ** (2. / 3.)))
    test_velocity = PLANET_DICT['Jupiter'][2] * ((1. / 3.) ** (- 1. / 3.))
    
    PLANET_DICT['Test'] = (test_mass, test_position, test_velocity)
    #PLANET_DICT.pop('Jupiter')


prepare_test()


class Planet:
    def __init__(self, name, (mass, position, velocity)):
        self.name = name  # String
        self.mass = mass  # Float
        self.position = position * cst.au  # Numpy ndarray
        self.velocity = velocity * cst.au / (60. * 60. * 24.)  # Numpy ndarray
        self.forces = {}  # {'Mars': False, 'Earth': ndarray}
        self.init_forces()
        self.history = np.array([]).reshape([0, 3])

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
        diff = (self.position - offset) / cst.au
        self.history = np.concatenate([self.history, [diff]], axis=0)


def distance(planet1, planet2):
    assert isinstance(planet1, Planet)
    assert isinstance(planet2, Planet)
    x1 = planet1.position
    x2 = planet2.position
    direction = x2 - x1
    d = np.sqrt(np.sum(direction ** 2.))
    unit_vector = direction / d
    return d, unit_vector
