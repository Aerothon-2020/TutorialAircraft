from __future__ import division
import numpy as npy
import pylab as pyl

from Aerothon.scalar.units import IN, LBF, PSFC, SEC, ARCDEG, FT, OZF, RPM, HP, inHg, GRAM, gacc, W, K, V, mAh, OHM, A, MM
from Aerothon.scalar.units import AsUnit
from Aerothon.ACPropulsion import ACPropulsion

from Aerothon.ACPropeller import ACPropeller
from Aerothon.AeroUtil import STDCorrection

from Aerothon.ACMotor import ACBattery

from Aerothon.ACMotor import ACMotor

"""
I'm just importing the 2015 Propulsion all in one file for a bit of simplicity just as a starting point
You should go look at the 2015 or 2022 directory structures to enable your trade studies.
"""

####################################
# SET PROP PROPERTIES
####################################
Prop = ACPropeller()
Prop.name       = 'APC 20x8E'
Prop.D          = 20*IN
Prop.Thickness  = 0.5*IN

Prop.Pitch      = 8*IN
Prop.dAlpha     = 3.3*ARCDEG
Prop.Solidity   = 0.0126

Prop.AlphaStall = 20*ARCDEG
Prop.AlphaZeroCL = 0*ARCDEG
"""
When you start taking test data, you will modify these 3 items below to match your propeller data.
"""
Prop.CLSlope    = .078/ARCDEG  #- 2D airfoil lift slope
Prop.CDCurve    = 2.2          #- 2D curvature of the airfoil drag bucket
Prop.CDp        = .02          #- Parasitic drag

Prop.Weight     = 115*GRAM*gacc

Prop.ThrustUnit = LBF
Prop.ThrustUnitName = 'lbf'
Prop.PowerUnit = W
Prop.PowerUnitName = 'watt'
Prop.MaxTipSpeed = None

###################################
# BATTERY PROPERTIES
###################################
# Turnicy 6Cell 3000
MainBattery = ACBattery()
MainBattery.Voltage = 22.2*V
MainBattery.Cells = 6
MainBattery.Capacity = 3000*mAh
MainBattery.C_Rating = 25
MainBattery.Weight = .915*LBF
MainBattery.LWH = (1.375*IN,1.875*IN,6.0*IN) #inaccurate dimensions


###################################
# MOTOR PROPERTIES
###################################
Motor  = ACMotor()
Motor.name = 'Hacker_A50_14L'
Motor.Battery = MainBattery
#Matched data
Motor.Ri = .12*OHM
Motor.Io = .5*A
Motor.Kv  = 355*RPM/V
Motor.Vmax = 23.5*V
Motor.Imax = 55*A
Motor.ThrustUnit = LBF
Motor.ThrustUnitName = 'lbf'
Motor.xRm =  100000
Motor.Pz  = 0.0
Motor.Weight = 445*GRAM*gacc
Motor.LenDi = [46.8*MM, 59.98*MM]

###################################
# COMBINED PROPERTIES
###################################
Propulsion = ACPropulsion(Prop,Motor)
Propulsion.Alt  = 0*FT
Propulsion.Vmax =70*FT/SEC
Propulsion.nV   = 20

if __name__=='__main__':
    ###########################
    # PROPELLER DATA AND PLOTS
    ##########################
    #
    # These are corrected for standard day
    #
    # Second set of data taken - concern about first set since taken at night
    STD = STDCorrection(30.00 * inHg, (22 + 273.15) * K)
    STD2 = STDCorrection(29.63 * inHg, (21.1 + 273.15) * K)
    STD3 = STDCorrection(30.10 * inHg, (12.7 + 273.15) * K)
    Prop.ThrustData = [(5520 * RPM, 176 * OZF * STD),
                       (5040 * RPM, 139 * OZF * STD),
                       (4590 * RPM, 116 * OZF * STD),
                       (4110 * RPM, 91 * OZF * STD),
                       (3540 * RPM, 66 * OZF * STD),
                       (5862 * RPM,
                        187 * OZF * STD2)]  # this point taken after initial points on Hacker A50. Used to verify good data.

    Arm = 19.5 * IN * STD
    Arm3 = 19.5 * IN * STD3  # Took torque data in closet with known prop to observe difference between temp
    Prop.TorqueData = [(5490 * RPM, (8.3 * Arm * OZF)),
                       (5000 * RPM, (6.8 * Arm * OZF)),
                       (4560 * RPM, (5.5 * Arm * OZF)),
                       (4000 * RPM, (4.3 * Arm * OZF)),
                       (3525 * RPM, (3.4 * Arm * OZF)),
                       # begin 2nd taking of torque data in closet
                       (5690 * RPM, (9.5 * Arm3 * OZF)),
                       (5018 * RPM, (7.1 * Arm3 * OZF)),
                       (4525 * RPM, (5.7 * Arm3 * OZF)),
                       (4118 * RPM, (4.8 * Arm3 * OZF))]
    print " D     : ", AsUnit(Prop.D, 'in')
    print " Pitch : ", AsUnit(Prop.Pitch, 'in')

    Vmax = 50
    h = 0 * FT
    N = npy.linspace(1000, 6800, 5) * RPM

    Alpha = npy.linspace(-25, 25, 41) * ARCDEG
    Vi = npy.linspace(0, Vmax, 30) * FT / SEC

    #Prop.CoefPlot(Alpha, fig=1)
    Prop.PTPlot(N, Vi, h, 'V', fig=2)

    #
    #    N = npy.linspace(0, 13000,31)*RPM
    #    Vi = npy.linspace(0,Vmax,5)*FT/SEC
    #
    #    Prop.PTPlot(N,Vi,h,'N', fig = 3)
    Prop.PlotTestData(fig=3)

    N = 6024 * RPM
    print
    print "Static Thrust   : ", AsUnit(Prop.T(N, 0 * FT / SEC, h), 'lbf')
    print "Measured Thrust : ", AsUnit(max(npy.array(Prop.ThrustData)[:, 1]), 'lbf')
    N = 6410 * RPM
    print
    print "Static Torque   : ", AsUnit(Prop.P(N, 0 * FT / SEC, h) / N, 'in*ozf')
    print "Measured Torque : ", AsUnit(max(npy.array(Prop.TorqueData)[:, 1]), 'in*ozf')

    ###########################
    # MOTOR DATA AND PLOTS
    ##########################
    # This data has been corrected for standard day
    STD_motor = STDCorrection(29.9 * inHg, (23.9 + 273.15) * K)
    STD2_motor = STDCorrection(30.32 * inHg, (5 + 273.15) * K)  # 1/14/2015
    Arm_motor = 19.5 * IN
    #            RPM,        Torque                               Current   Voltage
    TestData = [(6210 * RPM, (7.5 * Arm_motor * OZF) * STD_motor, 34.8 * A, 23.0 * V),
                (5910 * RPM, (8.7 * Arm_motor * OZF) * STD_motor, 39.0 * A, 21.9 * V),
                (5610 * RPM, (9.9 * Arm_motor * OZF) * STD_motor, 44.2 * A, 21.5 * V),
                (5640 * RPM, (9.3 * Arm_motor * OZF) * STD_motor, 40.5 * A, 21.4 * V),
                (5640 * RPM, (11.9 * Arm_motor * OZF) * STD_motor, 48.2 * A, 21.5 * V),
                (6034 * RPM, (8.9 * Arm_motor * OZF) * STD_motor, 35.8 * A, 22.06 * V),
                (5802 * RPM, (11.1 * Arm_motor * OZF) * STD_motor, 45.2 * A, 21.9 * V)]  # this is actual test data from a test stand

    Motor.TestData = TestData

    print "V to Motor : ", AsUnit(Motor.Vmotor(Ib=3.75 * A), 'V')
    print "Efficiency : ", Motor.Efficiency(Ib=3.75 * A)
    print "Max efficiency : ", Motor.Effmax()
    print "Max efficiency current : ", AsUnit(Motor.I_Effmax(), 'A')
    print "Max efficiency RPM : ", AsUnit(Motor.N_Effmax(), 'rpm')

    Motor.PlotTestData(fig=4)

    ###########################
    # SYSTEM DATA AND PLOTS
    ##########################

    Propulsion_VMAX = 70
    Vi = npy.linspace(0,Vmax,30)*FT/SEC
    Vprop = npy.linspace(0,Vmax,5)*FT/SEC
    Prop_Ni = npy.linspace(1000,7000,30)*RPM
    Propulsion.PlotMatched(Vi, Prop_Ni, Vprop, fig=5)

    Propulsion.Draw(fig=6)

    pyl.show()