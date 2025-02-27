from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

def gaussMethod(eq1, eq2):
    A, B, C = eq1
    A1, B1, C1 = eq2

    # Проверка на совпадающие линии
    if A1 * B == A * B1 and A1 * C == A * C1:
        return None, "Бесконечно много решений"

    # Остальная часть метода Гаусса
    if A != 0:
        factor = A1 / A
        A1 -= factor * A
        B1 -= factor * B
        C1 -= factor * C

    if A1 == 0 and B1 == 0:
        if C1 == 0:
            return None, "Бесконечно много решений"
        else:
            return None, "Нет решений"

    if B1 == 0:
        return None, "Ошибка: Деление на 0 невозможно (B1 = 0)."

    Y = C1 / B1
    X = (C - B * Y) / A

    return (round(X, 2), round(Y, 2)), None


def plot_equations(eq1, eq2, solution):
    A, B, C = eq1
    A1, B1, C1 = eq2

    x = np.linspace(-10, 10, 400)

    # Проверка на вертикальные линии для предотвращения деления на 0
    if B != 0:
        y1 = (C - A * x) / B
    else:
        y1 = None

    if B1 != 0:
        y2 = (C1 - A1 * x) / B1
    else:
        y2 = None

    plt.figure()

    # Условие для проверки совместимых линий
    if y1 is not None:
        plt.plot(x, y1, label=f'{A}x + {B}y = {C}', color='blue')
    else:
        plt.axvline(x=C / A, color='blue', label=f'{A}x + {B}y = {C}')  # Вертикальная линия, если B == 0

    if y2 is not None:
        plt.plot(x, y2, label=f'{A1}x + {B1}y = {C1}', color='green')
    else:
        plt.axvline(x=C1 / A1, color='green', label=f'{A1}x + {B1}y = {C1}')  # Вертикальная линия, если B1 == 0

    if solution is not None and isinstance(solution, tuple):
        # Отображение одной точки решения
        plt.plot(solution[0], solution[1], 'ro', label=f'Решение: ({solution[0]:.2f}, {solution[1]:.2f})')
    elif isinstance(solution, str) and solution == "Бесконечно много решений":
        # Условие совпадающих линий
        if y1 is not None:
            plt.plot(x, y1, 'r--', label='Совпадающие линии')
        else:
            plt.axvline(x=C / A, color='red', linestyle='--', label='Совпадающие линии')

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.title('График системы линейных уравнений')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return image_base64


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    try:
        function1 = request.form["row1"]
        function2 = request.form["row2"]

        # Проверка правильного формата (разделения через запятую)
        if not ("," in function1 and "," in function2):
            return render_template("result.html", data_format_error=True, image_base64=None)

        eq1 = tuple(map(float, function1.split(",")))
        eq2 = tuple(map(float, function2.split(",")))

        result, error = gaussMethod(eq1, eq2)

        if error:
            solution_type = error
            result = None
        else:
            solution_type = "Одно решение"

        # Генерация графика независимо от результата
        image_base64 = plot_equations(eq1, eq2, result if result else solution_type)

        return render_template("result.html", result=result, solution_type=solution_type, image_base64=image_base64)

    except Exception as e:
        return render_template("result.html", error=f"Ошибка: {str(e)}", image_base64=None)



if __name__ == "__main__":
    app.run(debug=True)

