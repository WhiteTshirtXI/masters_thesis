#!/usr/bin/python
# Copyright (C) 2013 FlowKit Ltd, Lausanne, Switzerland
# E-mail contact: contact@flowkit.com
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License, either
# version 3 of the License, or (at your option) any later version.
#
# Rewrite, extension and bugfixes by Florian Rohm, 2015

#
# 2D flow around a cylinder
#
# D2Q9 Stencil with enumeration
#
# 5   2   8
#   \ | /
# 3 - 0 - 6
#   / | \
# 4   1   7
#

from numpy import *
from matplotlib import cm, pyplot
from auxiliary.VTKWrapper import saveToVTK
from auxiliary.stream import stream
from auxiliary.collide import BGKCollide, cumulantCollide, cumulantCollide_min
from auxiliary.LBMHelpers import clamp, getMacroValues, sumPopulations, equilibrium, noslip, iLeft, iCentV, iRight, iTop, iCentH, iBot
from auxiliary.ghiaResults import *
from auxiliary.transformations.momentsFromDistributions import momentsFromDistributions
import os


###### Plot settings ############################################################

plotEveryN    = 500         # draw every plotEveryN'th cycle
skipFirstN    = 0       # do not process the first skipFirstN cycles
savePlot      = True      # save velocity norm and x velocity plot
liveUpdate    = True     # show the process of the simulation (slow)
saveVTK       = False       # save the vtk files
prefix        = 'ldc_re500_vel2'      # naming prefix for saved files
outputFolder  = './out'    # folder to save the output to
workingFolder = os.getcwd()


###### Flow definition #########################################################
maxIterations = 10000  # Total number of time iterations.
Re            = 500.0   # Reynolds number.re

# Number of Cells
nx = 100
ny = 100

# Highest index in each direction
nxl = nx-1
nyl = ny-1

# populations
q  = 9

# Velocity in lattice units.
uLB  = 0.08
nulb = uLB*ny/Re

# Relaxation parameter
omega = 1.0 / (3.*nulb+0.5)


###### Plot preparations ############################################################

# quick and dirty way to create output directory
if not os.path.isdir(outputFolder):
    try:
        os.makedirs(outputFolder)
    except OSError:
        pass

# Define the Grid for vtk output
gridX = arange(0, nx, dtype='float64')
gridY = arange(0, ny, dtype='float64')
gridZ = arange(0, 1, dtype='float64')
grid  = gridX, gridY, gridZ

# Set velocity to 0 on z-axis
velocityZ = zeros((nx, ny, 1))

# define axis for velocity plot
axisYPlot = arange(ny, 0, -1, dtype='float64')
axisYNorm = axisYPlot/(ny)

# import results of Ghia et al.
yghia = getAxis()
xghia = getRe100()


###### Setup ##################################################################

# set up the walls
leftWall    = fromfunction(lambda   x, y: x == 0,  (nx, ny))
rightWall   = fromfunction(lambda   x, y: x == nxl,  (nx, ny))
bottomWall  = fromfunction(lambda   x, y: y == nyl,  (nx, ny))

wall    = logical_or(logical_or(leftWall, rightWall), bottomWall)

# initial velocity profile
#  < -
#   -
#  - >
vel                = zeros((2, nx, ny))
vel[0, :,  0 ]     =  uLB

# initial particle distributions
feq   = equilibrium(1.0, vel)
fin   = feq.copy()
fpost = feq.copy()

# interactive mode (execute code while showing figures)
if ( liveUpdate | savePlot ):
    pyplot.ion()
    fig, ax = pyplot.subplots(1)

os.chdir(outputFolder)


###### Main time loop ##########################################################
for time in range(maxIterations):

    # Calculate macroscopic density and velocity
    (rho, u) = getMacroValues(fin)

    feq = equilibrium(rho, u)

    # Collision step.
    fpost = BGKCollide(fin, feq, omega)
    #fpost = cumulantCollide_min(fin, rho, u, omega)

    # Streaming step
    fin[0, :, :] = fpost[0, :, :]

    fin[1, 1:nxl,   :]     = fpost[1, 0:nxl-1,  :]
    fin[2,   :,   0:nyl-1] = fpost[2,   :,    1:nyl]
    fin[3, 0:nxl-1, :]     = fpost[3, 1:nxl,    :]
    fin[4,   :,   1:nyl]   = fpost[4,   :,    0:nyl-1]

    fin[5, 1:nxl,   0:nyl-1] = fpost[5, 0:nxl-1, 1:nyl]
    fin[6, 0:nxl-1, 0:nyl-1] = fpost[6, 1:nxl,   1:nyl]
    fin[7, 0:nxl-1, 1:nyl]   = fpost[7, 1:nxl,   0:nyl-1]
    fin[8, 1:nxl,   1:nyl]   = fpost[8, 0:nxl-1, 0:nyl-1]


    # Left wall: compute density from known populations
    u[:, :, 0] = vel[:, :, 0]
    rho[:, 0] = sumPopulations(fin[iCentV, 0, :])+2.*sumPopulations(fin[iTop, 0, :])

    # complete the left wall treatement wrt Yu 2002
    fin[iBot, 0, :] = - feq[iTop, 0, :] + (feq[iBot, 0, :] + fin[iTop, 0, :])
    # fin[iBot, 0, :] = fin[iTop, 0, :] + 6 * dot(c, u.transpose(1, 0, 2)) c[iBot][0] * rho*t[iBot]

    # wall boundary handling
    for i in range(q):
        fin[i, wall] = fin[noslip[i], wall]

    # Visualization
    if ( (time % plotEveryN == 0) & (liveUpdate | saveVTK | savePlot) & (time > skipFirstN) ):
        if ( liveUpdate | savePlot ):
            ax.clear()
            ax.imshow(sqrt(u[0]**2+u[1]**2).transpose(),  cmap=cm.afmhot, vmin=0., vmax=0.05)

        if ( liveUpdate ):
            pyplot.draw()
        if ( saveVTK ):
            # convert velocity and density to 3d arrays
            printVel = reshape(u, (2, nx, ny, 1))
            printRho = reshape(rho, (nx, ny, 1))

            velocity = (printVel[0, :, :, :], printVel[1, :, :, :], velocityZ)
            saveNumber = str(time/plotEveryN).zfill(4)

            saveToVTK(velocity, printRho, prefix, saveNumber, grid)
        if ( savePlot ):
            pyplot.savefig(prefix + "." + str(time/plotEveryN).zfill(4) + ".png")

os.chdir(workingFolder)
