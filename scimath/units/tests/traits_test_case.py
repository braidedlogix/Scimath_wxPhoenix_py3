#-----------------------------------------------------------------------------
#
#  Copyright (c) 2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Greg Rogers
#
#-----------------------------------------------------------------------------

from unittest import TestCase

from traits.api import HasTraits, TraitError

from scimath.units.api import dimensionless, FamilyNameTrait, UnitsTrait, \
    unit_parser


class UnitsNonStrict(HasTraits):
    units = UnitsTrait


class UnitsStrict(HasTraits):
    units = UnitsTrait(is_strict=True)


class UnitsStrictNotNone(HasTraits):
    units = UnitsTrait('ft', is_strict=True, allow_none=False)


class UnitsStrictWithFamily(HasTraits):
    units = UnitsTrait(
        is_strict=True, allow_none=True, family_trait='family_name')
    family_name = FamilyNameTrait('unknown', allow_none=False)


class FamilyNameNonStrict(HasTraits):
    family_name = FamilyNameTrait


class FamilyNameStrict(HasTraits):
    family_name = FamilyNameTrait(is_strict=True)


class FamilyNameStrictNotNone(HasTraits):
    family_name = FamilyNameTrait('unknown', is_strict=True, allow_none=False)


class FamilyNameWithUnitsLinkage(HasTraits):
    """ units and family_name are always compatible. family_name is the master
    and must be changed first if you want to change both.
    """
    family_name = FamilyNameTrait(
        'length', is_strict=True, allow_none=False, units_trait='units')
    units = UnitsTrait(
        'm', is_strict=True, allow_none=False, family_trait='family_name')

    def __init__(self, **traits):
        """ Create a new FamilyNameWithUnitsLinkage. """

        # HasTraits.__init__ will assign attributes from **traits in an abitrary
        # order (its a dictionary).  However, this class defines a relationship
        # between units and family_name and therefore must make sure the
        # assignments are done in the proper order.
        if 'units' in traits and 'family_name' in traits:
            units = traits.pop('units')
            family_name = traits.pop('family_name')

        else:
            units = family_name = None

        super(FamilyNameWithUnitsLinkage, self).__init__(**traits)

        if units is not None:
            self.family_name = family_name
            self.units = units

        return


class TraitsTestCase(TestCase):
    def test_units_trait(self):
        obj = UnitsNonStrict(units='km')
        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'km')

        obj.units = 'm/sec**2'
        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'm/sec**2')

        obj.units = 'invalid'
        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'invalid')
        self.assertEqual(obj.units.derivation, dimensionless.derivation)

        units = unit_parser.parse_unit('g/cc')
        self.assertFalse(units is None)
        self.assertEqual(units.label, 'g/cc')
        self.assertNotEqual(units.derivation, dimensionless.derivation)

        obj.units = units
        self.assertTrue(obj.units is units)

        return

    def test_units_not_none(self):
        obj = UnitsStrictNotNone(units='km')
        self.assertRaises(TraitError, setattr, obj, 'units', None)

        try:
            obj = UnitsStrictNotNone(units=None)
            self.fail('Constructor did not raise TraitError with units=None')
        except TraitError:
            pass
        return

    def test_strict_units_trait(self):
        obj = UnitsStrict(units='km')
        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'km')

        obj.units = 'm/sec**2'
        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'm/sec**2')
        self.assertEqual(obj.units.derivation, (1, 0, -2, 0, 0, 0, 0))

        self.assertRaises(TraitError, setattr, obj, 'units', 'invalid')

        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'm/sec**2')
        self.assertEqual(obj.units.derivation, (1, 0, -2, 0, 0, 0, 0))

        units = unit_parser.parse_unit('g/cc')
        self.assertFalse(units is None)
        self.assertEqual(units.label, 'g/cc')
        self.assertNotEqual(units.derivation, dimensionless.derivation)

        obj.units = units
        self.assertTrue(obj.units is units)

        return

    def test_units_strict_with_family(self):
        obj = UnitsStrictWithFamily()
        self.assertEqual(obj.family_name, 'unknown')

        # anything is compatible with 'unknonw'
        obj.units = 'km/sec'

        obj.family_name = 'pvelocity'

        obj.family_name = 'distance'
        obj.units = 'km'

        self.assertRaises(TraitError, setattr, obj, 'units', 'g/cc')

        return

    def test_family_name_trait(self):
        obj = FamilyNameNonStrict(family_name='distance')
        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'distance')

        obj.family_name = 'time'
        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'time')

        obj.family_name = 'unknown to unit_manager'
        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'unknown to unit_manager')

        obj = FamilyNameNonStrict()
        self.assertFalse(obj is None)
        self.assertTrue(obj.family_name is None)

        return

    def test_family_name_strict_trait(self):
        obj = FamilyNameStrict(family_name='distance')
        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'distance')

        obj.family_name = 'time'
        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'time')

        self.assertRaises(TraitError, setattr, obj, 'family_name',
                          'unknown to unit_manager')
        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'time')

        obj = FamilyNameNonStrict()
        self.assertFalse(obj is None)
        self.assertTrue(obj.family_name is None)

        return

    def test_family_not_none(self):
        obj = FamilyNameStrictNotNone(family_name='length')
        self.assertRaises(TraitError, setattr, obj, 'family_name', None)

        try:
            obj = FamilyNameStrictNotNone(family_name=None)
            self.fail(
                'Constructor did not raise TraitError with family_name=None')
        except TraitError:
            pass
        return

    def test_family_with_units_defaults(self):
        obj = FamilyNameWithUnitsLinkage()

        self.assertFalse(obj is None)
        self.assertEqual(obj.family_name, 'length')
        self.assertEqual(obj.units.label, 'm')

        return

    def test_family_with_units_family_change_with_compatible_units(self):

        # family changing should not cause units change if units are
        # compatible with the family.
        obj = FamilyNameWithUnitsLinkage()

        obj.family_name = 'distance'
        self.assertEqual(obj.family_name, 'distance')
        self.assertEqual(obj.units.label, 'm')

        obj.units = 'ft'
        self.assertEqual(obj.family_name, 'distance')
        self.assertEqual(obj.units.label, 'ft')

        obj.family_name = 'length'
        self.assertEqual(obj.family_name, 'length')
        self.assertEqual(obj.units.label, 'ft')

        return

    def test_family_with_units_family_change_causes_units_change(self):

        # family change with incompatible units should reset units to default
        # units for that family as defined by the unit_manager.
        obj = FamilyNameWithUnitsLinkage()

        obj.family_name = 'time'
        self.assertEqual(obj.family_name, 'time')
        self.assertEqual(obj.units.label, 'msec')

        return

    def test_family_with_units_units_change_compatible(self):

        # Should be able to change units within a family without
        # exception.
        obj = FamilyNameWithUnitsLinkage()

        obj.units = 'ft'
        self.assertEqual(obj.family_name, 'length')
        self.assertEqual(obj.units.label, 'ft')

        obj.units = 'in'
        self.assertEqual(obj.family_name, 'length')
        self.assertEqual(obj.units.label, 'in')

        obj.units = 'cm'
        self.assertEqual(obj.family_name, 'length')
        self.assertEqual(obj.units.label, 'cm')

    def test_family_with_units_units_change_not_compatible(self):

        # Can't change units to value incompatible with the family without
        # changing the family first.
        obj = FamilyNameWithUnitsLinkage()

        self.assertRaises(TraitError, setattr, obj, 'units', 'hours')

        obj.family_name = 'time'
        self.assertEqual(obj.family_name, 'time')
        self.assertEqual(obj.units.label, 'msec')

        obj.units = 'hour'
        self.assertEqual(obj.family_name, 'time')
        self.assertEqual(obj.units.label, 'hour')

        return

    def _units_changed(self, obj, name, old, new):
        #print "_units_changed name: '%s' old: '%s' new: '%s'" \
        #    % ( name, old, new )
        self.event_change_log.append((name, old, new))

    def test_units_events(self):
        self.event_change_log = []

        obj = UnitsNonStrict(units='km')
        self.assertFalse(obj is None)
        self.assertEqual(obj.units.label, 'km')

        obj.on_trait_change(self._units_changed)

        obj.units = 'ft'
        self.assertEqual(len(self.event_change_log), 1)
        self.assertEqual(self.event_change_log[0][0], 'units')
        self.assertEqual(obj.units.label, 'ft')

        obj.units = 'feet'
        self.assertEqual(len(self.event_change_log), 2)
        self.assertEqual(self.event_change_log[1][0], 'units')
        self.assertEqual(obj.units.label, 'feet')

    def ui_family_with_units(self):
        obj = FamilyNameWithUnitsLinkage()
        obj.configure_traits(kind='modal')
        print('\n')
        obj.print_traits()

        return


### EOF
