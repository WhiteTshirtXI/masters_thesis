#!/usr/bin/python
# 2D Lattice Boltzmann Code
# Copyright (C) 2016  Florian Rohm
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# 6   2   5
#   \ | /
# 3 - 0 - 1
#   / | \
# 7   4   8

# 0,2   1,2   2,2
#   \    |   /
# 0,1   1,1   2,1
#   /    |   \
# 0,0   1,0   2,0

import os
import sys

filename = os.path.dirname(os.path.realpath(__file__)) + "/../transformations/centralMomentsFromDistributions.py"
fileObject = open(filename , "w")

orig_stdout = sys.stdout
sys.stdout = fileObject

print "#Automatically generated, do not change\n"
print "from numpy import *"
print ""
print "def centralMomentsFromDistributions (u, fin):"
print "    ux = u[0, :, :]"
print "    uy = u[1, :, :]"
print "    (nx,ny) = ux.shape"
print "    f = zeros((3,3,nx,ny))"
print ""
print "    f[1,1] = fin[0]"
print "    f[2,1] = fin[1]"
print "    f[1,2] = fin[2]"
print "    f[0,1] = fin[3]"
print "    f[1,0] = fin[4]"
print "    f[2,2] = fin[5]"
print "    f[0,2] = fin[6]"
print "    f[0,0] = fin[7]"
print "    f[2,0] = fin[8]"

for i in range(3):
    print \
    "\
    c_{0}_0 = f[{0},0]              + f[{0},1]           + f[{0},2]          \n\
    c_{0}_1 = f[{0},0]*(-1 - uy)    - f[{0},1]*uy        + f[{0},2]*(1 - uy) \n\
    c_{0}_2 = f[{0},0]*(-1 - uy)**2 + f[{0},1]*uy**2     + f[{0},2]*(1 - uy)**2".format(i)

for b in range(3):
    print \
    "\
    c_0{0} = c_0_{0}              + c_1_{0}           + c_2_{0}          \n\
    c_1{0} = c_0_{0}*(-1 - ux)    - c_1_{0}*ux        + c_2_{0}*(1 - ux) \n\
    c_2{0} = c_0_{0}*(-1 - ux)**2 + c_1_{0}*ux**2     + c_2_{0}*(1 - ux)**2".format(b)

print ""
print "    return (c_00, c_10, c_01, c_11, c_20, c_02, c_21, c_12, c_22)"

sys.stdout = orig_stdout
fileObject.close()
