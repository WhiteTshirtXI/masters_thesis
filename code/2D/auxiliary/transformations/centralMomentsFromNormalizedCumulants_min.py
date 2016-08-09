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

def centralMomentsFromNormalizedCumulants_min (rho, K_11, K_20, K_02):
    # Transformation to central moments
    c_22 = 2*K_11*K_11/rho + K_20*K_02/rho

    return (rho, K_11, K_20, K_02, c_22)
