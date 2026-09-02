import math


class Capacitor:
    def __init__(self, capacitance_farad):
        self.capacitance = capacitance_farad


class Wire:
    def __init__(self, wire_length_cm, wire_diameter_mm, wire_resistivity_microohm_cm):
        self.wire_length = wire_length_cm/100
        self.wire_diameter = wire_diameter_mm/1000
        self.wire_resistivity = wire_resistivity_microohm_cm*(10**(-8))

    @property
    def wire_cross_sectional_area(self):
        return math.pi*((self.wire_diameter**2)/4)

    @property
    def resistance(self):
        return (self.wire_resistivity*self.wire_length)/self.wire_cross_sectional_area


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