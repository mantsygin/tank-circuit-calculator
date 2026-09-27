from calculator import inductance, frequency, oscillation_period, critical_resistance, quality_factor


def analyze_circuit_web(core, wire, capacitor):
    L = inductance(core, wire)
    C = capacitor.capacitance
    R = wire.resistance
    f = frequency(capacitor, L)
    T = oscillation_period(capacitor, L)
    Q = quality_factor(R, L, C)
    R_cr = critical_resistance(L, C)

    if R > R_cr:
        mode = "Aperiodic (R > R_cr)"
    elif R < R_cr:
        mode = "Oscillatory (R < R_cr)"
    else:
        mode = "Critical (R = R_cr)"

    result = {
        "core_shape": core.shape,
        "mu_r": core.mu_r,
        "wire_diameter_mm": wire.wire_diameter * 1000,
        "coil_number": wire.coil_number,
        "wire_length_mm": wire.wire_length * 1000,
        "L_uH": L * 1e6,
        "C_nF": C * 1e9,
        "R_Ohm": R,
        "f_kHz": f / 1000,
        "T_us": T * 1e6,
        "mode": mode,
        "Q": Q,
        "R_cr_Ohm": R_cr
    }

    if core.shape in ['toroidal', 'tor']:
        result["outer_diameter_mm"] = core.outer_diameter * 1000
        result["inner_diameter_mm"] = core.inner_diameter * 1000
        result["height_mm"] = core.height * 1000
    elif core.shape in ['cylindrical', 'cylinder']:
        result["diameter_mm"] = core.diameter * 1000
        result["length_mm"] = core.length * 1000
    elif core.shape in ['customized', 'custom']:
        result["cross_section_mm"] = core.cross_section * 1000
        result["magnetic_length_mm"] = core.magnetic_length * 1000

    return result
