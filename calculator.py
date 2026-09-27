import math


class Constants:
    def __init__(self, name, symbol, value, unit):
        self.name = name
        self.symbol = symbol
        self.value = value
        self.unit = unit


mu_0 = Constants("Permeability of free space", "μ₀", 4 * math.pi * 10 ** (-7), "H/m")


class Capacitor:
    def __init__(self, capacitance_farad):
        self.capacitance = capacitance_farad


class Core:
    def __init__(self, shape, mu_r, dim_1_mm, dim_2_mm, dim_3_mm=None):
        self.shape = shape.lower()
        self.mu_r = mu_r

        if self.shape in ['toroidal', 'tor']:
            self.outer_diameter = dim_1_mm / 1000
            self.inner_diameter = dim_2_mm / 1000
            self.height = dim_3_mm / 1000
        elif self.shape in ['cylindrical', 'cylinder']:
            self.diameter = dim_1_mm / 1000
            self.length = dim_2_mm / 1000
        elif self.shape in ['customized', 'custom']:
            self.cross_section = dim_1_mm / 1000
            self.magnetic_length = dim_2_mm / 1000
        else:
            raise ValueError(f"Incorrect core shape: {self.shape}")

    @classmethod
    def toroidal(cls, mu_r, outer_diameter_mm, inner_diameter_mm, height_mm):
        return cls('toroidal', mu_r, outer_diameter_mm, inner_diameter_mm, height_mm)

    @classmethod
    def cylindrical(cls, mu_r, diameter_mm, length_mm):
        return cls('cylinder', mu_r, diameter_mm, length_mm)

    @classmethod
    def custom(cls, mu_r, cross_section_mm, magnetic_length_mm):
        return cls('custom', mu_r, cross_section_mm, magnetic_length_mm)

    @property
    def core_cross_sectional_area(self):
        if self.shape in ['toroidal', 'tor']:
            return ((self.outer_diameter - self.inner_diameter) / 2) * self.height
        if self.shape in ['cylindrical', 'cylinder']:
            return math.pi * (self.diameter ** 2) / 4
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
        self.wire_diameter = wire_diameter_mm / 1000
        self.wire_resistivity = wire_resistivity_microohm_cm * (10 ** (-8))
        self.wire_insulation_thickness = insulation_thickness_mm / 1000
        self.core = core

    @property
    def wire_diameter_with_insulation(self):
        return self.wire_diameter + 2 * self.wire_insulation_thickness

    @property
    def wire_cross_sectional_area(self):
        return math.pi * ((self.wire_diameter ** 2) / 4)

    @property
    def coil_number(self):
        if self.core.shape in ['toroidal', 'tor']:
            return int(self.core.inner_diameter * math.pi / self.wire_diameter_with_insulation) - 1
        elif self.core.shape in ['cylindrical', 'cylinder']:
            return int(self.core.length / self.wire_diameter_with_insulation) - 1
        elif self.core.shape in ['customized', 'custom']:
            return int(self.core.magnetic_length / self.wire_diameter_with_insulation) - 1

    @property
    def wire_length(self):
        if self.core.shape in ['toroidal', 'tor']:
            return self.coil_number * math.pi * ((self.core.outer_diameter + self.core.inner_diameter) / 2)
        elif self.core.shape in ['cylindrical', 'cylinder']:
            return self.coil_number * math.pi * self.core.diameter
        elif self.core.shape in ['customized', 'custom']:
            return self.coil_number * self.core.magnetic_length

    @property
    def resistance(self):
        return self.wire_resistivity * (self.wire_length / self.wire_cross_sectional_area)


def inductance(core, wire):
    return (mu_0.value * core.mu_r * wire.coil_number ** 2 * core.core_cross_sectional_area)\
           / core.core_magnetic_path_length


def frequency(capacitor, L):
    return 1 / (2 * math.pi * math.sqrt(L * capacitor.capacitance))


def oscillation_period(capacitor, L):
    return 2 * math.pi * math.sqrt(L * capacitor.capacitance)


def critical_resistance(L, C):
    return 2 * math.sqrt(L / C)


def quality_factor(R, L, C):
    return (1 / R) * math.sqrt(L / C)


def analyze_circuit(core, wire, capacitor):
    L = inductance(core, wire)
    C = capacitor.capacitance
    R = wire.resistance
    f = frequency(capacitor, L)
    T = oscillation_period(capacitor, L)
    Q = quality_factor(R, L, C)
    R_cr = critical_resistance(L, C)

    if R > R_cr:
        mode = f"Aperiodic mode (R > R_cr): R = {R:.6f} Ohm, R_cr = {R_cr:.6f} Ohm"
    elif R < R_cr:
        mode = f"Oscillatory mode (R < R_cr): R = {R:.6f} Ohm, R_cr = {R_cr:.6f} Ohm"
    else:
        mode = f"Critical mode (R = R_cr): R = {R:.6f} Ohm, R_cr = {R_cr:.6f} Ohm"

    print("\n DESIGN PARAMETERS:")
    print(f"  Core: {core.shape}, μ = {core.mu_r}")
    if core.shape in ['toroidal', 'tor']:
        print(f"    Outer diameter: {core.outer_diameter * 1000:.1f} mm")
        print(f"    Inner diameter: {core.inner_diameter * 1000:.1f} mm")
        print(f"    Height: {core.height * 1000:.1f} mm")
    print(f"  Wire: diameter {wire.wire_diameter * 1000:.2f} mm")
    print(f"  Number of turns: {wire.coil_number}")
    print(f"  Wire length: {wire.wire_length * 1000:.2f} mm")

    print("\n ELECTRICAL PARAMETERS:")
    print(f"  Inductance L = {L * 1e6:.3f} µH")
    print(f"  Capacitance C = {C * 1e9:.3f} nF")
    print(f"  Resistance R = {R:.6f} Ohm")
    print(f"  Frequency f = {f / 1000:.3f} kHz")
    print(f"  Period T = {T * 1e6:.3f} µs")

    print("\n OPERATING MODE:")
    print(f"  {mode}")

    print("\n QUALITY FACTOR:")
    print(f"  Q = {Q:.2f}")