# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:05:12 2022

@author: gunes
"""
import naca12_incremental as structural_solver
import numpy as np
from math import pi
#Structural and geometric parameters of the 2D wing.
m = 12.4
I = 0.065
Kh = 28444
Ka = 70.5
b = 0.5
xa = 0.03
a=-0.5
parameters = np.array([m, I, Kh, Ka, b, xa,a])
#Run steady
# steady_cmd = "pls run steady"
# subprocess.run(steady_cmd)
#Initial guesses and assumed normalized deflection. Angular rotation DOF is
#normalized to "Def" and phase of this DOF is taken as zero.
deflection = 0.01*pi/180
V=50;
xi = np.array([[b*(1+a)*np.sin(deflection)*np.cos(-54*pi/180)], [b*(1+a)*np.sin(deflection)*np.sin(-54*pi/180)], [np.sqrt(Ka/I)], [-0.5]])
#Define "errcriteria" and "itcriteria" as error criteria and iteration criteria
#respectively.
errcriteria = 1e-3
itcriteria = 5
#Newton solver takes inputs initial guesses,  error criteria,  iteration criteria
#,  deflection and structural parameters and gives roots,  maximum error in a
#variable and iteration number.
roots, maxerr, iterationnumber = structural_solver.NewtonNumeric(xi, errcriteria, itcriteria, deflection, V, parameters)
