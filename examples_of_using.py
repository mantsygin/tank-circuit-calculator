# Examples of using tank-circuit-calculator.
# This file demonstrates how to use the calculator with different cores, wires, and capacitors.
# Feel free to modify the parameters for your own needs.

# First, you have to import the file "calculator.py".
from calculator import *
# Then you have to specify the characteristics of your core, wire and capacitor.

# For the toroidal core:
core_1 = Core.toroidal(2500, 60, 40, 10)

# For the cylindrical core:
core_2 = Core.cylindrical(1000, 10, 50)

# For the custom core:
core_3 = Core.custom(2000, 15, 65)

# Wire characteristics are specified this way:
wire_1 = Wire(0.3, 1.72, 0.05, core_1)
# You should also specify which core you use with this wire.

# You may also work with many wires:
wire_2 = Wire(0.5, 2.65, 0.1, core_2)
wire_3 = Wire(0.2, 1.59, 0.03, core_3)

# When it comes to write down your capacitor characteristics, you only have to indicate its capacitance.
# Here's how to do it:
capacitor_1 = Capacitor(5 * 10**(-9))

# You may also work with many capacitors:
capacitor_2 = Capacitor(4 * 10**(-8))
capacitor_3 = Capacitor(8 * 10**(-7))

# When you need to learn your LC-circuit characteristics, you just have to type this:
analyze_circuit(core_1, wire_1, capacitor_1)
# You need to specify what core, wire, and capacitor you use.

# You may use any combination:
analyze_circuit(core_2, wire_3, capacitor_2)

# Or:
analyze_circuit(core_3, wire_2, capacitor_1)