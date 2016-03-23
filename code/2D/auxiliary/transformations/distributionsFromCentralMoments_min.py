from numpy import *

def distributionsFromCentralMoments_min (u, c_00, c_11, c_20, c_02, c_22):
    ux = u[0, :, :]
    uy = u[1, :, :]
    (nx,ny) = ux.shape
    f = zeros((3,3,nx,ny))
    c_0_0 = (c_00*(ux**2 - ux)  + c_20) * 0.5
    c_1_0 =  c_00*(1 - ux**2)   - c_20
    c_2_0 = (c_00*(ux**2 + ux)  + c_20) * 0.5
    c_0_1 = ( c_11*(2*ux - 1) ) * 0.5
    c_1_1 =  - c_11*2*ux
    c_2_1 = ( c_11*(2*ux + 1) ) * 0.5
    c_0_2 = (c_02*(ux**2 - ux) + c_22) * 0.5
    c_1_2 =  c_02*(1 - ux**2)  - c_22
    c_2_2 = (c_02*(ux**2 + ux) + c_22) * 0.5
    f[0, 0] = (c_0_0*(uy**2 - uy) + c_0_1*(2*uy - 1) + c_0_2) * 0.5
    f[0, 1] =  c_0_0*(1 - uy**2)  - c_0_1*2*uy       - c_0_2
    f[0, 2] = (c_0_0*(uy**2 + uy) + c_0_1*(2*uy + 1) + c_0_2) * 0.5
    f[1, 0] = (c_1_0*(uy**2 - uy) + c_1_1*(2*uy - 1) + c_1_2) * 0.5
    f[1, 1] =  c_1_0*(1 - uy**2)  - c_1_1*2*uy       - c_1_2
    f[1, 2] = (c_1_0*(uy**2 + uy) + c_1_1*(2*uy + 1) + c_1_2) * 0.5
    f[2, 0] = (c_2_0*(uy**2 - uy) + c_2_1*(2*uy - 1) + c_2_2) * 0.5
    f[2, 1] =  c_2_0*(1 - uy**2)  - c_2_1*2*uy       - c_2_2
    f[2, 2] = (c_2_0*(uy**2 + uy) + c_2_1*(2*uy + 1) + c_2_2) * 0.5

    return array((f[1,1], f[2,1], f[1,2], f[0,1], f[1,0], f[2,2], f[0,2], f[0,0], f[2,0]))
