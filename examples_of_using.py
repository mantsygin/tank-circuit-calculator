# This file demonstrates how to use the calculator with different cores, wires, and capacitors.
# The code below shows which parameters to enter and in what order.
# Feel free to modify the parameters for your own needs.

# Import the file "calculator.py":
from calculator import Core, Wire, Capacitor, analyze_circuit

# Specify the characteristics of your core, wire and capacitor:

# For the toroidal core:
core_1 = Core.toroidal(mu_r=2500,
                       outer_diameter_mm=60,
                       inner_diameter_mm=40,
                       height_mm=10)

# For the cylindrical core:
core_2 = Core.cylindrical(mu_r=1000,
                          diameter_mm=10,
                          length_mm=50)

# For the custom core:
core_3 = Core.custom(mu_r=2000,
                     cross_section_mm=65,
                     magnetic_length_mm=120)

# Wire characteristics are specified this way:
wire_1 = Wire(wire_diameter_mm=0.3,
              wire_resistivity_microohm_cm=1.72,
              insulation_thickness_mm=0.05,
              core=core_1)

# More wires:
wire_2 = Wire(wire_diameter_mm=0.5,
              wire_resistivity_microohm_cm=2.65,
              insulation_thickness_mm=0.1,
              core=core_2)
wire_3 = Wire(wire_diameter_mm=0.2,
              wire_resistivity_microohm_cm=1.59,
              insulation_thickness_mm=0.03,
              core=core_3)

# Define a capacitor by its capacitance:
capacitor_1 = Capacitor(capacitance_farad=5e-9)

# More capacitors:
capacitor_2 = Capacitor(capacitance_farad=4e-8)
capacitor_3 = Capacitor(capacitance_farad=8e-7)

# Pass the core, wire, and capacitor to analyze:
analyze_circuit(core_1, wire_1, capacitor_1)

# Any combination works:
analyze_circuit(core_2, wire_3, capacitor_2)

# Or:
analyze_circuit(core_3, wire_2, capacitor_1)