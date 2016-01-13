from numpy import *
from equilibrium import equilibrium
from transformation.transformations import cumulantsFromDistribution, distributionFromCumulants

def BGKCollide(fin, rho, u, omega):
    feq = equilibrium(rho, u)
    return fin - omega * (fin - feq)

def cumulantCollide(f, rho, u, omega):
    omega2  = 1
    omega3  = 1
    omega4  = 1
    omega5  = 1
    omega6  = 1
    omega7  = 1
    omega8  = 1
    omega9  = 1
    omega10 = 1

    rhoInv = 1./rho
    ux = u[0]
    uy = u[1]
    uz = u[2]

    ( C_000, C_001, C_002, C_010, C_011, C_012, C_020, C_021, C_022,
      C_100, C_101, C_102, C_110, C_111, C_112, C_120, C_121, C_122,
      C_200, C_201, C_202, C_210, C_211, C_212, C_220, C_221, C_222) = cumulantsFromDistribution(rhoInv, u, f)

    CS_000 = C_000
    CS_100 = C_100
    CS_010 = C_010
    CS_001 = C_001

    CS_110 = (1-omega)*C_110
    CS_101 = (1-omega)*C_101
    CS_011 = (1-omega)*C_011

    # (C_000 =) k_000 in the paper, not sure, why he wrote k
    Dxux = - 0.5*omega*rhoInv*(2*C_200 - C_020 - C_002) - 0.5*1*rhoInv*(C_200 + C_020 + C_002 - C_000)
    Dyuy = Dxux + 1.5*omega*rhoInv*(C_200 - C_020)
    Dzuz = Dxux + 1.5*omega*rhoInv*(C_200 - C_002)

    CS_200__m__CS020 = (1 - omega)*(C_200 - C_020) - 3*rho*(1 - 0.5*omega)*(Dxux*ux**2 - Dyuy*uy**2)
    CS_200__m__CS002 = (1 - omega)*(C_200 - C_002) - 3*rho*(1 - 0.5*omega)*(Dxux*ux**2 - Dzuz*uz**2)
    CS_200__p__CS020__p__CS_002 = omega2*C_000 + (1-omega2)*(C_200 + C_020 + C_002) \
                                  - 3*rho*(1 - 0.5*omega2)*(Dxux*ux**2 + Dyuy*uy**2 + Dzuz*uz**2)

    CS_200 = (CS_200__m__CS020 + CS_200__m__CS002 + CS_200__p__CS020__p__CS_002)/3.
    CS_020 = CS_200 - CS_200__m__CS020
    CS_002 = CS_200 - CS_200__m__CS002


    CS_120__p__CS_102 = (1 - omega3)*(C_120 + C_102)
    CS_210__p__CS_012 = (1 - omega3)*(C_210 + C_012)
    CS_201__p__CS_021 = (1 - omega3)*(C_201 + C_021)
    CS_120__m__CS_102 = (1 - omega4)*(C_120 - C_102)
    CS_210__m__CS_012 = (1 - omega4)*(C_210 - C_012)
    CS_201__m__CS_021 = (1 - omega4)*(C_201 - C_021)

    CS_120 = 0.5*(CS_120__p__CS_102 + CS_120__m__CS_102)
    CS_102 = 0.5*(CS_120__p__CS_102 - CS_120__m__CS_102)
    CS_012 = 0.5*(CS_210__p__CS_012 - CS_210__m__CS_012)
    CS_210 = 0.5*(CS_210__p__CS_012 + CS_210__m__CS_012)
    CS_201 = 0.5*(CS_201__p__CS_021 + CS_201__m__CS_021)
    CS_021 = 0.5*(CS_201__p__CS_021 - CS_201__m__CS_021)

    C_111 = (1 - omega5) * C_111


    CS_220__m__2CS_202__p__CS_022 = (1 - omega6)*(C_220 - 2*C_202 + C_022)
    CS_220__p__CS_202__m__2CS_022 = (1 - omega6)*(C_220 + C_202 - 2*C_022)
    CS_220__p__CS_202__p__CS_022  = (1 - omega7)*(C_220 + C_202 + C_022)

    CS_220 = (CS_220__m__2CS_202__p__CS_022 + CS_220__p__CS_202__m__2CS_022 + CS_220__p__CS_202__p__CS_022)/3.
    CS_202 = (CS_220__p__CS_202__p__CS_022 - CS_220__m__2CS_202__p__CS_022)/3.
    CS_022 = (CS_220__p__CS_202__p__CS_022 - CS_220__p__CS_202__m__2CS_022)/3.

    CS_211 = (1 - omega8 )* C_211
    CS_121 = (1 - omega8 )* C_121
    CS_112 = (1 - omega8 )* C_112
    CS_221 = (1 - omega9 )* C_221
    CS_212 = (1 - omega9 )* C_212
    CS_122 = (1 - omega9 )* C_122
    CS_222 = (1 - omega10 )* C_222

    return distributionFromCumulants(rhoInv, u, C_000, C_001, C_002, C_010, C_011, C_012, C_020, C_021, C_022,
                                                C_100, C_101, C_102, C_110, C_111, C_112, C_120, C_121, C_122,
                                                C_200, C_201, C_202, C_210, C_211, C_212, C_220, C_221, C_222)
