import math
import numpy as np
from system import systems
import matplotlib.pyplot as plt


#todo пофиксить функцию с логарифмом, и расчет системы уравнений
def eq1(x):
    return -0.38*x**3-3.42*x**2+2.51*x+8.75

def eq2(x):
    return math.log(x**2 + 1) - x

def eq3(x):
    return 2.74*x**3-1.93*x**2-15.28*x-3.72

def eq4(x):
    return x**3+4.81*x**2-17.37*x+5.38

def deq1(x):
    return -1.14*x**2-6.84*x+2.51

def ddeq1(x):
    return -2.28*x-6.84

def deq2(x):
    return (2*x/(x**2+1))-1

def ddeq2(x):
    return ((-2*x**2+2)/(x**2+1)**2)

def deq3(x):
    return 8.22*x**2-3.86*x-15.28

def ddeq3(x):
    return 16.44*x-3.86

def deq4(x):
    return 3*x**2+9.62*x-17.37

def ddeq4(x):
    return 6*x+9.62

eqs = [eq1, eq2, eq3, eq4]
deqs = [deq1, deq2, deq3, deq4]
ddeqs = [ddeq1, ddeq2, ddeq3, ddeq4]

#метод хорд, метод ньютона, метод простой итерации
def main():
    while True:
        choice = int(input("решение нелинейных уравнений (1), решение систем линейных уравнений (2), выход (3): "))

        if choice == 3:
            break
        if choice == 2:
            systems()
        elif choice == 1:
            print("выберите уравнение: ")
            print("1. -0.38x**3-3.42x**2+2.51x+8.75")
            print("2. ln(x**2 + 1) -x")
            print("3. 2.74x**3-1.93x**2-15.28x-3.72")
            print("4. x**3+4.81x**2-17.37x+5.38")
            # выбор варианта
            choice = int(input())

            if choice == 1:
                draw(eq1, -10, 10)
            elif choice == 2:
                draw(eq2, -10, 10)
            elif choice == 3:
                draw(eq3, -10, 10)
            elif choice == 4:
                draw(eq4, -10, 10)

            print("выберите метод: ")
            print("1. метод хорд")
            print("2. метод Ньютона")
            print("3. метод простой итерации")
            method = int(input())

            while True:
                choice1 = input("откуда вы хотите ввести границы интервала и погрешность? 1. с файла 2. с клавиатуры ")
                if choice1 == "1":
                    inf = read_from_file()
                    break
                elif choice1 == "2":
                    inf = read_from_keyboard()
                    break
                else:
                    print("Неверный ввод")

            if method == 1:
                hord(eqs[choice-1], inf[0], inf[1], inf[2], deqs[choice-1])
            elif method == 2:
                newton(eqs[choice-1], inf[0], inf[1], inf[2], deqs[choice -1], ddeqs[choice-1])
            elif method == 3:
                iteration(eqs[choice-1], inf[0], inf[1], inf[2], deqs[choice-1])


def read_from_file():
    filename = input("введите имя файла: ")
    with open(filename) as f:
        left = float(f.readline().strip())
        right = float(f.readline().strip())
        eps = float(f.readline().strip())
        if left > right:
            left, right = right, left
    return [left, right, eps]


def read_from_keyboard():
    while True:
        left = float(input("введите левую границу интервала: "))
        right = float(input("введите правую границу интервала: "))
        eps = float(input("введите погрешность: "))
        if left > right:
            left, right = right, left
        return [left, right, eps]

def hord(f, a, b, eps, df):
    if f(a)*f(b) >0 and not((df(a) > 0 and df(b) > 0) or (df(a) < 0 and df(b) < 0)):
        print("на этом отрезке либо нет корней, либо их больше одного")
        return

    n = 1
    draw(f, a, b)

    while True:
        x = a - (a - b) * f(a) / (f(a) - f(b))
        print(f"x: {x}, f(X): {f(x)}, {abs(b-a)}")

        if abs(f(x)) < eps or abs(b - a) < eps:
            break

        if f(a) * f(x) < 0:
            b = x
        else:
            a = x

        n += 1
    print(f"корень: {x}, значение функции: {f(x)}, число итераций {n}")

def newton(f, a, b, eps, df, ddf):
    if f(a)*ddf(a) > 0:
        x0 = a
    elif f(b)*ddf(b) > 0:
        x0 = b
    else:
        x0 = (a+b)/2
    draw(f, a, b)

    if f(a)*f(b) > 0 and not((df(a) > 0 and df(b) > 0) or (df(a) < 0 and df(b) < 0)):
        print("на этом отрезке либо нет корней, либо их больше одного")
        return

    #достаточное но не необходимое, может сойдется, а может нет
    elif df(x0)*ddf(x0) > 0:
        print("условие сходимости метода не выполняется, ")
        print("хотите продолжить? [y/n]")
        answer = input().strip().lower()
        if answer != "y":
            return

    n = 0
    while True:
        x = x0 - f(x0)/df(x0)
        n+=1
        if abs(x - x0) <= eps and abs(f(x0)) <= eps:
            break
        x0 = x
        print(f"x0: {x0}, f(X): {f(x)}")

    print(f"корень: {x0}, значение функции: {f(x0)}, число итераций {n}")


def iteration(f, a, b, eps, df):
    if f(a)*f(b) >= 0 and not((df(a) > 0 and df(b) > 0) or (df(a) < 0 and df(b) < 0)):
        print("на промежутке либо нет корней, либо их несколько")
        return

    draw(f, a, b)

    lambda1 = -1 / max(abs(df(a)), abs(df(b)))
    if df(a) < 0 and df(b) < 0:
        lambda1 = 1 / max(abs(df(a)), abs(df(b)))

    print(f"выбрали такую лямбду: {lambda1}")

    def phi(x):
        return x + lambda1*f(x)

    def dfphi(x):
        return 1+ lambda1*df(x)

    if max(abs(dfphi(a)), abs(dfphi(b))) >= 1:
        print("условие сходимости не выполнено. последовательность может не сойтись или найти другой корень.")
        print("Хотите продолжить? [y/n]")
        answer = input().strip().lower()
        if answer != "y":
            return

    x0 = (a+b)/2
    print(f"начальное приближение: {x0}")

    n = 0
    while n < 100:
        x1 = phi(x0)
        print(f"x0: {x0}, x1: {x1}, |x1 - x0|:  {abs(x1 - x0)}")

        if abs(x1 - x0) < eps and abs(f(x1)) < eps:
            print(f"корень: {x1}, значение функции в корне: {f(x1)}, число итераций: {n} ")
            return x1

        x0 = x1
        n += 1

    print("Достигнут лимит итераций, последовательность не сошлась.")
    return None

def draw(f, a, b):
    x = np.linspace(a, b, 100)
    y = [f(xi) for xi in x]

    plt.figure(facecolor="black", figsize=(10, 6))  # Черный фон и размер графика
    plt.plot(x, y, label='Функция', color="pink", linewidth=2)

    plt.axhline(0, color='white', linewidth=0.5, linestyle='--')
    plt.axvline(0, color='white', linewidth=0.5, linestyle='--')

    plt.grid(True, linestyle='--', linewidth=0.5, color="black", alpha=0.7)

    plt.title("График функции", color="white", fontsize=14, pad=20)
    plt.xlabel("Ось X", color="white", fontsize=12)
    plt.ylabel("Ось Y", color="white", fontsize=12)

    plt.legend(loc='upper right', fontsize=12, facecolor='black', edgecolor='white', labelcolor='white')

    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')


    for spine in plt.gca().spines.values():
        spine.set_color('white')

    plt.legend()
    plt.show()

main()
