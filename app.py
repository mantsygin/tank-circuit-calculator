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
            form_data = request.form.to_dict()

            shape = form_data.get('core_shape')
            mu_r = float(form_data.get('mu_r', 0))
            capacitance_nf = float(form_data.get('capacitance', 0))
            wire_diameter = float(form_data.get('wire_diameter', 0))
            wire_resistivity = float(form_data.get('wire_resistivity', 0))
            insulation = float(form_data.get('insulation', 0))

            if capacitance_nf <= 0:
                raise ValueError("Ёмкость должна быть больше нуля.")
            if wire_diameter <= 0:
                raise ValueError("Диаметр провода должен быть больше нуля.")
            if wire_resistivity <= 0:
                raise ValueError("Удельное сопротивление провода должно быть больше нуля.")
            if mu_r <= 0:
                raise ValueError("Магнитная проницаемость должна быть больше нуля.")
            if insulation < 0:
                raise ValueError("Толщина изоляции не может быть отрицательной.")

            capacitor = Capacitor(capacitance_farad=capacitance_nf * 1e-9)

            if shape == 'toroidal':
                outer_d = float(form_data.get('outer_diameter', 0))
                inner_d = float(form_data.get('inner_diameter', 0))
                height = float(form_data.get('height', 0))

                if outer_d <= inner_d:
                    raise ValueError("Внешний диаметр тора должен быть больше внутреннего.")
                if height <= 0:
                    raise ValueError("Высота тора должна быть больше нуля.")

                core = Core.toroidal(mu_r, outer_d, inner_d, height)

            elif shape == 'cylindrical':
                diameter = float(form_data.get('diameter', 0))
                length = float(form_data.get('length', 0))

                if diameter <= 0 or length <= 0:
                    raise ValueError("Диаметр и длина цилиндра должны быть больше нуля.")

                core = Core.cylindrical(mu_r, diameter, length)

            elif shape == 'custom':
                cross_section = float(form_data.get('cross_section', 0))
                magnetic_length = float(form_data.get('magnetic_length', 0))

                if cross_section <= 0 or magnetic_length <= 0:
                    raise ValueError("Площадь сечения и длина магнитного пути должны быть больше нуля.")

                core = Core.custom(mu_r, cross_section, magnetic_length)
            else:
                raise ValueError("Неизвестная форма сердечника.")

            wire = Wire(wire_diameter, wire_resistivity, insulation, core)

            if wire.coil_number <= 0:
                raise ValueError("Провод с такой изоляцией слишком толстый для этого сердечника (не помещается ни одного витка).")

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

        except ValueError as e:
            results = {'error': f"Ошибка в данных: {str(e)}"}

        except ZeroDivisionError:
            results = {'error': "Ошибка расчёта: деление на ноль. Проверьте введённые параметры."}

        except Exception as e:
            results = {'error': f"Непредвиденная ошибка: {str(e)}"}

    return render_template('index.html', results=results, form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True)
