from flask import Flask, render_template, request
from calculator import Core, Wire, Capacitor, inductance, frequency, oscillation_period, critical_resistance, \
    quality_factor

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    form_data = {}

    if request.method == 'POST':
        try:
            form_data['core_shape'] = request.form.get('core_shape')
            form_data['mu_r'] = request.form.get('mu_r')
            form_data['capacitance'] = request.form.get('capacitance')
            form_data['wire_diameter'] = request.form.get('wire_diameter')
            form_data['wire_resistivity'] = request.form.get('wire_resistivity')
            form_data['insulation'] = request.form.get('insulation')

            form_data['outer_diameter'] = request.form.get('outer_diameter')
            form_data['inner_diameter'] = request.form.get('inner_diameter')
            form_data['height'] = request.form.get('height')
            form_data['diameter'] = request.form.get('diameter')
            form_data['length'] = request.form.get('length')
            form_data['cross_section'] = request.form.get('cross_section')
            form_data['magnetic_length'] = request.form.get('magnetic_length')

            shape = form_data['core_shape']
            mu_r = float(form_data['mu_r'])
            capacitance_nf = float(form_data['capacitance'])
            wire_diameter = float(form_data['wire_diameter'])
            wire_resistivity = float(form_data['wire_resistivity'])
            insulation = float(form_data['insulation'])

            capacitor = Capacitor(capacitance_farad=capacitance_nf * 1e-9)

            if shape == 'toroidal':
                core = Core.toroidal(mu_r,
                                     float(form_data['outer_diameter']),
                                     float(form_data['inner_diameter']),
                                     float(form_data['height']))
            elif shape == 'cylindrical':
                core = Core.cylindrical(mu_r,
                                        float(form_data['diameter']),
                                        float(form_data['length']))
            elif shape == 'custom':
                core = Core.custom(mu_r,
                                   float(form_data['cross_section']),
                                   float(form_data['magnetic_length']))

            wire = Wire(wire_diameter, wire_resistivity, insulation, core)

            L = inductance(core, wire)
            C = capacitor.capacitance
            R = wire.resistance
            f = frequency(capacitor, L)
            T = oscillation_period(capacitor, L)
            Q = quality_factor(R, L, C)
            R_cr = critical_resistance(L, C)

            if R > R_cr:
                mode = "Aperiodic"
            elif R < R_cr:
                mode = "Oscillatory"
            else:
                mode = "Critical"

            results = {
                'frequency': f"{f:.3f}",
                'period': f"{T:.6f}",
                'wavelength': f"{3e8 / f:.3f}",
                'quarter_wavelength': f"{3e8 / f / 4:.3f}",
                'mode': mode,
                'resistance': f"{R:.6f}",
                'critical_resistance': f"{R_cr:.6f}",
                'quality_factor': f"{Q:.2f}"
            }

        except Exception as e:
            results = {'error': str(e)}

    return render_template('index.html', results=results, form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True)
