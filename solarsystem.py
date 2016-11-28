import numpy as np
import planet
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import gc


plt.rcParams['agg.path.chunksize'] = 10000


class SolarSystem:
    def __init__(self, dt=50 * 86400.):
        self.planets = []  # List of Planet objects
        self.populate()
        self.dt = dt

        loop_count = 0
        loop_cap = 5000 * 360
        for i, p in enumerate(self.planets):
            if p.name == "Sun":
                solar_index = i
        print "SOLAR INDEX: ", solar_index
        while loop_count < loop_cap:
            if loop_count % 10 == 0:
                sys.stdout.write("%.2f percent \r" % ((loop_count + 10) * 100. / loop_cap))
                sys.stdout.flush()
            self.run_simulation()
            solar_pos = self.planets[solar_index].position
            if loop_count % 100 == 0:
                for p in self.planets:
                    p.record(solar_pos)
                gc.collect()
            loop_count += 1
        print "\n"
        print "Pinned to %s" % self.planets[solar_index].name
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for p in self.planets:
            print p.name
            print "POSITION", p.position
            ax.plot(p.history[:, 0], p.history[:, 1],
                    marker='o', linestyle='None',
                    # linestyle='-' if not p.name == 'Sun' else 'None',
                    # marker='None' if not p.name == 'Sun' else 'o',
                    zs=p.history[:, 2])
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
