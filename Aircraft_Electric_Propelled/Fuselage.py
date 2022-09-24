from __future__ import division # let 5/2 = 2.5 rather than 2
from Aerothon.scalar.units import IN, LBF, SLUG, FT, OZM, OZF
from Aerothon.scalar.units import AsUnit
from Aerothon.ACFuselage import ACFuselage
from Aerothon.DefaultMaterialsLibrary import Monokote

from Propulsion_Electric import Phoenix100 as SpeedController
from Propulsion_Electric import MotorBattery as MotorBattery

Fuselage = ACFuselage()
"""
Note im just putting some dummy weights in here. Go to the 2015 AC if you want to 
see how to start using materials to calculate your weights.
"""
###################################
# ADD SECTIONS
###################################
Fuselage.AddSection('Nose', 3*IN, -1)
Fuselage.AddSection('PyldBay', 10*IN, 1)
Fuselage.AddSection('Tail')

###################################
# SIZE MOTOR MOUNT & FIREWALL
###################################
"""
Note im just using a fixed weight for the firewall, that's fine
Things you will want to include later would be:
 StringerMat which will give you the weight of whatever attaches the FrontBulk to BackBulk


We're going to put the battery in here as it's significant weight, but you 
should model every single thing in the fuselage as a weight somewhere
so you don't mess up your CG.
"""
Fuselage.Nose.FrontBulk.Width  = 3*IN
Fuselage.Nose.FrontBulk.Height = 7*IN
Fuselage.Nose.FrontBulk.Weight = .2*LBF
Fuselage.Nose.StringerMat.AreaForceDensity = 0.001*LBF/IN**2
Fuselage.Nose.SkinMat = Monokote.copy()

# we need to put the battery in here, it's significant weight
Fuselage.Nose.AddComponent("MotorBattery"  , MotorBattery.Weight, MotorBattery.LWH , "Back"  , (0.45 , .5, .5) )
Fuselage.Nose.AddComponent("SpeedController", SpeedController.Weight, SpeedController.LWH, "Right", (0.4 , 0.0, 0.7) )
###################################
# SIZE PAYLOAD PAY
###################################
"""
Note here we're sepcifying the skin mat density because now this area is big enough
that the monokote weight matters.
"""
Fuselage.PyldBay.FrontBulk.Width  = 5*IN
Fuselage.PyldBay.FrontBulk.Height = 5*IN
Fuselage.PyldBay.BackBulk.Width   = 5*IN
Fuselage.PyldBay.BackBulk.Height  = 5*IN
Fuselage.PyldBay.StringerMat.AreaForceDensity = 0.001*LBF/IN**2
Fuselage.PyldBay.SkinMat = Monokote.copy()

# notoinal placement for payload, this basically just puts t in the payload bay
Fuselage.Payload.Width  = 4*IN
Fuselage.Payload.Length = 10*IN
Fuselage.Payload.Face = 'Bottom'

Fuselage.XcgSection = Fuselage.PyldBay
Fuselage.XcgSecFrac = 0.5

###################################
# SIZE TAIL
###################################
"""
As your in the Preliminary Design, the tail section is mostly going to be iterated
because you'll likely be placing your VTail and HTail based on volume coefficents.
THis means your tails when you run Aircraft.py may not be attached, and you can modify 
them in that file to match up for your specific volume coeffs.
"""
Fuselage.Tail.BackBulk.Width = 2.25*IN
Fuselage.Tail.BackBulk.Height = 2*IN
Fuselage.Tail.BackBulk.X = [60*IN, 0*IN, 0*IN]
Fuselage.Tail.Align = 1
Fuselage.Tail.StringerMat.AreaForceDensity = 0.001*LBF/IN**2
Fuselage.Tail.SkinMat = Monokote.copy()

# Tell it to put the htail on the backbulk
Fuselage.TailBulk = Fuselage.Tail.BackBulk

if __name__ == '__main__':
    import pylab as pyl

    print 'Nose      Weight :', AsUnit(Fuselage.Nose.Weight, 'lbf')
    print 'PyldBay   Weight :', AsUnit(Fuselage.PyldBay.Weight, 'ozf')
    print 'TailTaper Weight :', AsUnit(Fuselage.Tail.Weight, 'lbf')

    print 'Fuselage Weight    :', AsUnit(Fuselage.Weight, 'lbf')
    print 'Fuselage MOI       :', AsUnit(Fuselage.MOI(), 'slug*ft**2')
    print 'Fuselage CG        :', AsUnit(Fuselage.CG(), 'in')
    print 'Fuselage Desired CG:', AsUnit(Fuselage.AircraftCG(), 'in')

    Fuselage.Draw()
    pyl.show()