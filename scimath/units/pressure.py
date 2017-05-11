#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2003  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from .SI import pascal, kilo, mega, giga
from scimath.units.force import lbf
from scimath.units.length import inch
from scimath.units.unit import unit
#
# Definitions of common pressure units
#
# Data taken from
#     Appendix F of Halliday, Resnick, Walker, "Fundamentals of Physics",
#         fourth edition, John Willey and Sons, 1993
#
#     The NIST Reference on Constants, Units and Uncertainty,
#         http://physics.nist.gov/cuu
#

# aliases

Pa = pascal
Pa.label = 'Pa'

kPa = kilo * pascal
kPa.label = 'kPa'

MPa = mega * pascal
MPa.label = 'MPa'
mpa = MPa
Mpa = MPa
MPA = MPa

GPa = giga * pascal
GPa.label = 'GPa'
gpa = GPa
Gpa = GPa
GPA = GPa

# others

bar = 1e5 * pascal
bar.label = 'bar'
bars = bar

kilobar = kilo * bar
kilobar.label = 'kbar'
kbar = kilobar
kbars = kbar

millibar = 100 * pascal

torr = 133.3 * pascal
atmosphere = 101325 * pascal

atm = atmosphere

pounds_per_square_inch = lbf / inch**2
pounds_per_square_inch.label = 'psi'
psi = pounds_per_square_inch
apsi = psi
psig = unit(psi.value, psi.derivation, 14.6959494)

inHg = 3386.389 * pascal
inHg.label = 'inHg'

# version
__id__ = "$Id: pressure.py,v 1.1.1.1 2003/07/02 21:39:14 aivazis Exp $"

#
# End of file
