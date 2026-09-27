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
                       height_mm=15)

# Wire characteristics are specified this way:
wire_1 = Wire(wire_diameter_mm=0.5,
              wire_resistivity_microohm_cm=1.72,
              insulation_thickness_mm=0.03,
              core=core_1)

# Define a capacitor by its capacitance:
capacitor_1 = Capacitor(capacitance_farad=2.3e-6)

analyze_circuit(core_1, wire_1, capacitor_1)
