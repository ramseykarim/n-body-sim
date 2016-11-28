import numpy as np
import planet
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import gc
import scipy.constants as cst
import pyfits as pf

plt.rcParams['agg.path.chunksize'] = 10000



class SolarSystem:
    def __init__(self, dt = 1 * 86400.):
        self.planets = []  # List of Planet objects
        self.populate()
        self.dt = dt

        plotnumb = int(1.3e+8/dt)

        loop_count = 0
        loop_cap = 10000 * 365

        for i, p in enumerate(self.planets):
            if p.name == "Sun":
                solar_index = i
        print "SOLAR INDEX: ", solar_index
        while loop_count < loop_cap:
            if loop_count % 50 == 0:
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
            print '------'
            print p.name
            #print "POSITION", p.position
            '''
            ax.plot(p.history[:, 0], p.history[:, 1],
                    marker='o', linestyle='None',
                    # linestyle='-' if not p.name == 'Sun' else 'None',
                    # marker='None' if not p.name == 'Sun' else 'o',
                    zs=p.history[:, 2])
            '''
            ax.plot(p.history[:plotnumb, 0], p.history[:plotnumb, 1],
                    marker='.', linestyle='None', color = 'b',
                    # linestyle='-' if not p.name == 'Sun' else 'None',
                    # marker='None' if not p.name == 'Sun' else 'o',
                    zs=p.history[:plotnumb, 2])
            ax.plot(p.history[-plotnumb:, 0], p.history[-plotnumb:, 1],
                    marker='.', linestyle='None', color = 'g',
                    # linestyle='-' if not p.name == 'Sun' else 'None',
                    # marker='None' if not p.name == 'Sun' else 'o',
                    zs=p.history[-plotnumb:, 2])
            avg_dist_init = np.median( np.sqrt( np.sum(p.history[:plotnumb, :]**2., axis = 1) ) )
            print 'Avg initial distance in AU from Sun:', avg_dist_init
            avg_dist_final = np.median( np.sqrt( np.sum(p.history[-plotnumb:, :]**2., axis = 1) ) )
            print 'Avg final distance in AU from Sun:', avg_dist_final
            print 'Change in avg distance from Sun:', (avg_dist_final - avg_dist_init)
            #if p.name != 'Sun':
            #   avg_dist, useless = planet.distance(self.planets[solar_index], p)
            #   print 'distance in AU from Sun', avg_dist/cst.au
            #print p.mass

            outputfilename = 'dt' + str(int(dt/86400.)) + '_total' + str(int(loop_cap/365.)) + p.name + '.fits'
            hdu = pf.PrimaryHDU(p.history)
            hdulist = pf.HDUList([hdu])
            hdulist.writeto(outputfilename ,clobber=True)

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
