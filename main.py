import math
from sympy import symbols, expand, simplify, Eq, solve

x = symbols('x')

x_list_val = [1.2, 1.3, 1.4, 1.6, 1.8]
y_list_val = [2.1, 2.0, 1.9, 2.5, 2.7]



def newton(x_value):
    dy1 = []
    dy2 = []
    dy3 = []
    dy4 = []
    dyy = [y_list_val, dy1, dy2, dy3, dy4]

    for i in range(0, len(y_list_val) - 1):
        for j in range(0, len(y_list_val) - i - 1):
            dyy[i + 1].append((dyy[i][j + 1] - dyy[i][j]) / (x_list_val[j + i + 1] - x_list_val[j]))
    #Максимальна довжина списку значень

    max_length = max(len(x_list_val), len(y_list_val), len(dy1), len(dy2), len(dy3),
                     len(dy4))
    print("Значення кінцевих різниць функції")
    print("{:<8} | {:<10} | {:<10} | {:<10} | {:<10} | {:<10} ".format("x", "y", "dy1", "dy2", "dy3", "dy4", ))
    print("_____________________________________________________________________________________")

    for i in range(max_length):
        x_val = "{:<8.4f}".format(x_list_val[i]) if i < len(x_list_val) else "         "
        y_val = "{:<10.4f}".format(y_list_val[i]) if i < len(y_list_val) else "         "
        dy1_val = "{:<10.4f}".format(dy1[i]) if i < len(dy1) else "          "
        dy2_val = "{:<10.4f}".format(dy2[i]) if i < len(dy2) else "          "
        dy3_val = "{:<10.4f}".format(dy3[i]) if i < len(dy3) else "          "
        dy4_val = "{:<10.4f}".format(dy4[i]) if i < len(dy4) else "          "
        print("{} | {} | {} | {} | {} | {}".format(x_val, y_val, dy1_val, dy2_val, dy3_val, dy4_val))

    print("\n... Перша інтерполяційна формула Ньютона ...")
    eq1 = y_list_val[0]
    for i in range(0,len(dy1)):
        subeq = dyy[i+1][0]
        for j in range(0, i + 1):
            subeq *= (x - x_list_val[j])
        eq1 = eq1 + subeq

    print(f"\nПоліном: {eq1}")
    simp_eq1 = simplify(expand(eq1))
    print("\nРозкрита формула:")
    print(simp_eq1)

    print(f"Підставляємо значення х3 у отриманий поліном, отримаємо: {eq1.subs([(x, x_list_val[3])])}\n")
    print(f"Підставляємо значення {x_value} у отриманий поліном, отримаємо: {eq1.subs([(x, x_value)])}\n")

    print("\n... Друга інтерполяційна формула Ньютона ...")

    eq2 = y_list_val[len(y_list_val) - 1]
    for i in range(0, len(dy1)):
        subeq = dyy[i + 1][len(dyy[i + 1]) - 1]
        for j in range(0, i + 1):
            subeq *= (x - x_list_val[len(x_list_val) - 1 - j])
        eq2 = eq2 + subeq

    print(f"Поліном: {eq2}")
    simp_eq2 = simplify(expand(eq2))
    print("\nРозкрита формула:")
    print(simp_eq2)

    print(f"Підставляємо значення х3 у отриманий поліном, отримаємо: {eq2.subs([(x, x_list_val[3])])}\n")
    print(f"Підставляємо значення {x_value} у отриманий поліном, отримаємо: {eq2.subs([(x, x_value)])}\n")
def spline(x_val):
    c0, c1, c2, c3, c4 = symbols('c0, c1, c2, c3, c4')

    c0 = 0
    c4 = 0

    a_list = []
    b_list = []
    c_list = [c0, c1, c2, c3, c4]
    d_list = []
    h_list = []

    for i in range(len(y_list_val) - 1):
        a_list.append(y_list_val[i + 1])

    print(f"Знайдені коефіцієнти a = {a_list}\n")

    for i in range(len(x_list_val) - 1):
        h_list.append(x_list_val[i + 1] - x_list_val[i])

    print(f"Знайдені коефіцієнти h = {h_list}\n")

    equations = []

    for i in range(3):
        eq = ((h_list[i] * c_list[i] + 2 * (h_list[i] + h_list[i + 1]) * c_list[i + 1] + h_list[i + 1] * c_list[i + 2])
               - 6 * ((y_list_val[i + 2] - y_list_val[i + 1]) / (h_list[i + 1]) - (y_list_val[i + 1] - y_list_val[i])
                      / (h_list[i])))
        equations.append(Eq(eq, 0))
        print(f"Знайдене рівняння {i} ітерації для знаходження коефіцієнтів с1, с2 та с3:\n"
              f"{eq}")

    solutions = solve(equations, (c1, c2, c3))
    print(f"Корені: \n"
          f"c1 = {solutions[c1]}, c2 = {solutions[c2]}, c3 = {solutions[c3]}\n")

    c_list[1] = solutions[c1]
    c_list[2] = solutions[c2]
    c_list[3] = solutions[c3]

    for i in range(4):
        d_list.append((c_list[i + 1] - c_list[i])/h_list[i])
        b_list.append((h_list[i] / 2) * c_list[i + 1] - ((h_list[i]**2) / 6) * d_list[i] +
                      (y_list_val[i + 1] - y_list_val[i]) / h_list[i])
    print(f"Знайдені коефіцієнти d: {d_list}\n")
    print(f"Знайдені коефіцієнти b:{b_list}\n")

    print("Отримані рівняння:")
    spline_func_list = []
    simp_spline_func_list = []

    for i in range(4):
        spline_func = (a_list[i] + b_list[i] * (x - x_list_val[i + 1]) + c_list[i + 1] *
                       ((x - x_list_val[i + 1]) ** 2 / 2) * d_list[i] * ((x -x_list_val[i + 1]) ** 3 / 6))
        spline_func_list.append(spline_func)

        simp_spline_func = simplify(spline_func)
        simp_spline_func_list.append(simp_spline_func)

        print(f"S{i + 1}(x) = {simp_spline_func}")

    print(f"\nПеревірка отриманих рівнянь:")
    for i in range(4):
        func = simp_spline_func_list[i]
        print(f"S{i + 1}({x_list_val[i]}) = {func.subs([(x, x_list_val[i])])}")
        print(f"S{i + 1}({x_list_val[i + 1]}) = {func.subs([(x, x_list_val[i + 1])])}")

    func_number = 0
    for i, value in enumerate(x_list_val):
        if x_list_val[i] <= x_val < x_list_val[i + 1]:
            print(f"\nЧисло {x_val} знаходиться між елементами з індексами {i} та {i + 1}\n")
            func_number = i + 1
    if func_number == 1:
        func = simp_spline_func_list[0]
        print(f"Підставляємо задане значення 'x' у першу ф-цію \nS1({x_val}) = {func.subs([(x,x_val)])}")
    elif func_number == 2:
        func = simp_spline_func_list[1]
        print(f"Підставляємо задане значення 'x' у першу ф-цію \nS2({x_val}) = {func.subs([(x,x_val)])}")
    elif func_number == 3:
        func = simp_spline_func_list[2]
        print(f"Підставляємо задане значення 'x' у першу ф-цію \nS3({x_val}) = {func.subs([(x,x_val)])}")
    elif func_number == 4:
        func = simp_spline_func_list[3]
        print(f"Підставляємо задане значення 'x' у першу ф-цію \nS4({x_val}) = {func.subs([(x,x_val)])}")

def main():
    print("Комп'ютерний практикум №5 \nВаріант №11 \nВиконав студент групи ПБ-21 \nРозумняк Руслан\n")

    x_val = 1.25
    print("___Метод Ньютона___\n")
    newton(x_val)
    print("___Метод кубічних сплайнів___\n")
    spline(x_val)

if __name__ == "__main__":
    main()