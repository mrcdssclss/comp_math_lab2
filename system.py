import autograd.numpy as np
from numdifftools import Jacobian
import matplotlib.pyplot as plt

def f1(x, y):
    return np.array([
        np.cos(y) + x - 1.5,
        2*y - np.sin(x - 0.5) - 1
    ])

def f2(x, y):
    return np.array([
        np.sin(y - 1) + x - 1.3,
        y - np.sin(x+1) - 0.8
    ])

def f1_phi(x, y):
    return np.array([
        1.5 - np.cos(y),
        (1-np.sin(x- 0.5))/2
    ])

def f2_phi(x, y):
    return np.array([
        1.3 - np.sin(y-1),
        0.8 + np.sin(x+1)
    ])

#метод простой итерации
def systems():
    print("выберите систему")
    print("1.")
    print("cos(y) + x = 1.5")
    print("2y - sin(x - 0.5) = 1")
    print("-----------------------------")
    print("2.")
    print("sin(y-1) + x = 1.3")
    print("y - sin(x+1) = 0.8")
    choice = int(input())
    if choice == 1:
        draw(f1)
    elif choice == 2:
        draw(f2)

    while True:
        choice1 = input("откуда вы хотите ввести начальное приближение и погрешность? 1. с файла 2. с клавиатуры ")
        if choice1 == "1":
            inf = read_from_file()
            break
        elif choice1 == "2":
            inf = read_from_keyboard()
            break
        else:
            print("Неверный ввод")

    if choice == 1:
        siteration(f1_phi, inf[0], inf[1], inf[2], f1)
    elif choice == 2:
        siteration(f2_phi, inf[0], inf[1], inf[2], f2)

def read_from_file():
    filename = input("введите имя файла: ")
    with open(filename) as f:
        xborder = float(f.readline().strip())
        yborder = float(f.readline().strip())
        eps = float(f.readline().strip())
    return [xborder, yborder, eps]


def read_from_keyboard():
    while True:
        xborder = float(input("введите приближение по x: "))
        yborder = float(input("введите приближение по y: "))
        eps = float(input("введите погрешность: "))
        return [xborder, yborder, eps]


def check(phi, xborder, yborder):
    if phi(xborder, yborder) is None:
        print("на этом интервале невозможно корректно решить систему")
        return

    j_matrix = Jacobian(lambda var: phi(var[0], var[1]))
    j = j_matrix([xborder, yborder])
    print(j)

    q = max(sum(abs(j)))
    if q < 1:
        return q
    else:
        print("Метод может не сойтись.")
        return False

def siteration(phi, xborder, yborder, eps, f):
    n = 0
    check(phi, xborder, yborder)

    for i in range(1000):
        n+=1
        x1, x2 = phi(xborder, yborder)[0], phi(xborder, yborder)[1]

        print(f"n: {n}, x: {x1}, y: {x2}, x1 - xborder: {x1 - xborder}, y - yborder: {x2 - yborder}")


        max_dif = max(abs(x1 - xborder), abs(x2 - yborder))
        if max_dif < eps or (abs(f(x1, x2)[0]) < eps and abs(f(x1, x2)[1]) < eps):
            print("Результат: ", f"x: {x1}, y: {x2}")
            print(f(x1, x2))
            return x1, x2

        xborder, yborder = x1, x2

    print("превышено количество итераций, корень не найден")


def draw(system):
    x = np.linspace(-2, 2, 400)
    y = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, y)

    Z1 = np.array([system(x_, y_)[0] for x_, y_ in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)
    Z2 = np.array([system(x_, y_)[1] for x_, y_ in zip(np.ravel(X), np.ravel(Y))]).reshape(X.shape)

    plt.contour(X, Y, Z1, levels=[0], colors='r', linewidths=2, linestyles='solid')
    plt.contour(X, Y, Z2, levels=[0], colors='b', linewidths=2, linestyles='solid')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('График системы уравнений')
    plt.grid(True)
    plt.show()


