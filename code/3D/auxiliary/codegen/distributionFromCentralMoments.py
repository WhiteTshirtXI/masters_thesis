#!/usr/bin/python

for b in range(3):
    for c in range(3):
        print \
        "\
    k_1_{0}{1} =  k_0{0}{1}*(1 - ux**2)  - k_1{0}{1}*2*ux       - k_2{0}{1}        \n\
    k_0_{0}{1} = (k_0{0}{1}*(ux**2 - ux) + k_1{0}{1}*(2*ux - 1) + k_2{0}{1}) * 0.5 \n\
    k_2_{0}{1} = (k_0{0}{1}*(ux**2 + ux) + k_1{0}{1}*(2*ux + 1) + k_2{0}{1}) * 0.5".format(b,c)

for i in range(3):
    for c in range(3):
        print \
        "\
    k_{0}1_{1} =  k_{0}_0{1}*(1 - uy**2)  - k_{0}_1{1}*2*uy       - k_{0}_2{1}        \n\
    k_{0}0_{1} = (k_{0}_0{1}*(uy**2 - uy) + k_{0}_1{1}*(2*uy - 1) + k_{0}_2{1}) * 0.5 \n\
    k_{0}2_{1} = (k_{0}_0{1}*(uy**2 + uy) + k_{0}_1{1}*(2*uy + 1) + k_{0}_2{1}) * 0.5".format(i,c)

for i in range(3):
    for j in range(3):
        print \
        "\
    f[{0}, {1}, 1] =  k_{0}{1}_0*(1 - uy**2)  - k_{0}{1}_1*2*uy       - k_{0}{1}_2        \n\
    f[{0}, {1}, 0] = (k_{0}{1}_0*(uy**2 - uy) + k_{0}{1}_1*(2*uy - 1) + k_{0}{1}_2) * 0.5 \n\
    f[{0}, {1}, 2] = (k_{0}{1}_0*(uy**2 + uy) + k_{0}{1}_1*(2*uy + 1) + k_{0}{1}_2) * 0.5".format(i,j)
