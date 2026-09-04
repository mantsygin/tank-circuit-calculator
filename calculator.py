import math


class Capacitor:
    def __init__(self, capacitance_farad):
        self.capacitance = capacitance_farad


class Core:
    def __init__(self, shape, mu_r, dim_1, dim_2, dim_3=None):
        self.shape = shape.lower()
        self.mu_r = mu_r

        if shape in ['toroidal', 'tor']:
            self.outer_diameter = dim_1
            self.inner_diameter = dim_2
            self.height = dim_3
        elif shape in ['cylindrical', 'cylinder']:
            self.diameter = dim_1
            self.length = dim_2
        elif shape in ['customized', 'custom']:
            self.cross_section = dim_1
            self.magnetic_length = dim_2

    @property
    def core_cross_sectional_area(self):
        if self.shape in ['toroidal', 'tor']:
            return ((self.outer_diameter - self.inner_diameter) / 2) * self.height
        if self.shape in ['cylindrical', 'cylinder']:
            return math.pi*((self.diameter**2)/4)
        if self.shape in ['customized', 'custom']:
            return self.cross_section

    @property
    def core_magnetic_path_length(self):
        if self.shape in ['toroidal', 'tor']:
            return math.pi * (self.outer_diameter + self.inner_diameter) / 2
        if self.shape in ['cylindrical', 'cylinder']:
            return self.length
        if self.shape in ['customized', 'custom']:
            return self.magnetic_length


class Wire:
    def __init__(self, wire_diameter_mm, wire_resistivity_microohm_cm, insulation_thickness_mm, core):
        self.wire_diameter = wire_diameter_mm/1000
        self.wire_resistivity = wire_resistivity_microohm_cm * (10**(-8))
        self.wire_insulation_thickness = insulation_thickness_mm/1000
        self.core = core

    @property
    def wire_diameter_with_insulation(self):
        return self.wire_diameter + 2 * self.wire_insulation_thickness

    @property
    def wire_cross_sectional_area(self):
        return math.pi * ((self.wire_diameter**2)/4)

    @property
    def coil_number(self):
        if self.core.shape in ['toroidal', 'tor']:
            return int(self.core.inner_diameter * math.pi/self.wire_diameter_with_insulation) - 1
        elif self.core.shape in ['cylindrical', 'cylinder']:
            return int(self.core.length/self.wire_diameter_with_insulation) - 1
        elif self.core.shape in ['customized', 'custom']:
            return int(self.core.magnetic_length/self.wire_diameter_with_insulation) - 1

    @property
    def wire_length(self):
        if self.core.shape in ['toroidal', 'tor']:
            return self.coil_number * math.pi * ((self.core.outer_diameter + self.core.inner_diameter)/2)
        elif self.core.shape in ['cylindrical', 'cylinder']:
            return self.coil_number * math.pi * self.core.diameter
        elif self.core.shape in ['customized', 'custom']:
            return self.coil_number * self.core.magnetic_length

    @property
    def resistance(self):
        return self.wire_resistivity * (self.wire_length/self.wire_cross_sectional_area)


def inductance(core, wire):
    return (4 * math.pi * 10**(-7) * core.mu_r * wire.coil_number**2 * core.core_cross_sectional_area)/core.core_magnetic_path_length


def oscillation_period(capacitor, L):
    return 2 * math.pi * math.sqrt(L * capacitor.capacitance)


def frequency(capacitor, L):
    return 1/(2 * math.pi * math.sqrt(L * capacitor.capacitance))