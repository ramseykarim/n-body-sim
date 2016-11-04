import numpy as np
import planet
import matplotlib.pyplot as plt
import sys


class SolarSystem:
    def __init__(self, dt=15 * 86400.):
        self.planets = []  # List of Planet objects
        self.populate()
        self.dt = dt

        loop_count = 0
        loop_cap = 15*360
        for i, p in enumerate(self.planets):
            if p.name == "Sun":
                solar_index = i
        print "SOLAR INDEX: ", solar_index
        while loop_count < loop_cap:
            if loop_count % 10 == 0:
                sys.stdout.write("%.2f\r" % ((loop_count + 10)*100./loop_cap))
                sys.stdout.flush()
            self.run_simulation()
            # x = []
            # y = []
            solar_pos = self.planets[solar_index].position
            # for p in self.planets:
            #     if p.name == 'Pluto?':
            #         continue
            #     x.append((p.position - solar_pos)[0])
            #     y.append((p.position - solar_pos)[1])
            for p in self.planets:
                p.record(solar_pos)
            # plt.plot(x, y, '.')
            loop_count += 1
        print ""
        print "Pinned to %s" % self.planets[solar_index].name
        for p in self.planets:
            plt.plot(p.history[0], p.history[1])
        plt.legend([p.name for p in self.planets])
        plt.show()

    def populate(self):
        for planet_name in planet.PLANET_DICT:
            planet_temp = planet.Planet(planet_name, planet.PLANET_DICT[planet_name])
            self.planets.append(planet_temp)

    def run_simulation(self):
        for p in self.planets:
            p.reset_forces()
        for p in self.planets:
            p.calculate_all_interactions(self.planets)
            p.update(self.dt)

SolarSystem()
