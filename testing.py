from TylerClasses import Data
from tyler import *
from random import random
from math import e, pow, log

def f(n: int) -> int:
  return (n * n * n) + 3 * n - 6

def base_test(n: float, coes: list):
  return pow(n, 2) * coes[0] + n * coes[1] + coes[2]

def base_test_d_d0(x: float, y: float, coes: list) -> float:
  return -2 * (y - coes[0] * (x * x) - coes[1] * x - coes[2]) * (x * x)

def base_test_d_d1(x: float, y: float, coes: list) -> float:
  return -2 * (y - coes[0] * (x * x) - coes[1] * x - coes[2]) * x

def base_test_d_d2(x: float, y: float, coes: list) -> float:
  return -2 * (y - coes[0] * (x * x) - coes[1] * x - coes[2])

def ln_test(n: float, coes: list) -> float:
  if n == 0:
    n = 0.00001
  return coes[0] + coes[1] * log(coes[2] * n)

def ln_test_d0(x: float, y: float , coes: list) -> float:
  if x == 0:
    x = 0.00001
  return -2 * (y - coes[0] - coes[1] * log(coes[2] * x))

def ln_test_d1(x: float, y: float, coes: list) -> float:
  if x == 0:
    x = 0.00001
  return -2 * log(coes[2] * x) * (y - coes[0] - coes[1] * log(coes[2] * x))

def ln_test_d2(x: float, y: float, coes: list) -> float:
  if x == 0:
    x = 0.00001
  return -2 * coes[1] / coes[2] * (y - coes[0] - coes[1] * log(coes[2] * x))

def expo_func(n: float, coes: list):
  return coes[0] + coes[1] * pow(e, n * coes[2])

def expo_d0(x: float, y: float, coes: list) -> float:
  return -2 * (y - expo_func(x, coes))

def expo_d1(x: float, y: float, coes: list) -> float:
  return -2 * (y - expo_func(x, coes)) * pow(e, x * coes[2])

def expo_d2(x: float, y: float, coes: list) -> float:
  return -2 * (y - expo_func(x, coes)) * coes[1] * coes[2] * pow(e, coes[2] * x)

def nudge():
  return random() * 100

def sigmoid_pos(x: float) -> float:
  return 1 / (1 + pow(e, -x + pow(e, 2)))

def standard_error_average(data: Data, predictions: Data, percent = False):
  sigma = 0
  length = len(data.y)
  for index in range(length):
    sigma += pow(data.y[index] - predictions.y[index], 2)

  if percent:
    return sigmoid_pos(sigma / length) * 100
  return sigma / length

def use_function(coes: list, x: float) -> float:
  n = len(coes)
  sigma = 0
  for i in range(n):
    sigma += coes[i] * pow(x, i)
  return sigma

def generate_function_v1(dataset: Data, partials: list, coes: list, alpha = .5, iterations = 100_000, print_me=False) -> list:
  def gradient(dataset: Data, partial: object, coes: list) -> float:
    sigma = 0
    n = len(dataset.x)
    for index in range(n):
      sigma += partial(dataset.x[index], dataset.y[index], coes)
    return sigma / n

  for _ in range(iterations):
    for i in range(len(coes)):
      coes[i] = coes[i] - alpha * gradient(dataset, partials[i], coes)
    if print_me:
      print("error is now at", standard_error_average(dataset, Data((dataset.x, [base_test(x, coes) for x in x_test]))))
  return coes
      

x_test = [n for n in range (0,100, 3)]
y = [f(n) + nudge() for n in x_test]

y2 = [f(n) for n in x_test]

data = Data((x_test, y))
best_fit = Data(data.line_of_best_fit())
perfect = Data((x_test, y2))

constants = generate_function_v1(data, [base_test_d_d0, base_test_d_d1, base_test_d_d2], [1,1,1], .00000001, print_me=False)
print("Quad constants =", constants)
y3 = [base_test(x, constants) for x in x_test]
test = Data((x_test, y3))

ln_constants = generate_function_v1(data, [ln_test_d0, ln_test_d1, ln_test_d2], [1,1,1], 0.000000000001, 200_000)
print("ln constants =", ln_constants)
y4 = [ln_test(x, constants) for x in x_test]
ln_data = Data((x_test, y4))

"""expo_constants = generate_function_v1(data, [expo_d0, expo_d1, expo_d2], [1,1,1], .0000000000001, 500_000 , print_me=False)
print("expo constants =", expo_constants)
y5 = [expo_func(x, constants) for x in x_test]
expo_data = Data((x_test, y5))"""

pl = scatter((1,1,1), data, "blue", marker="o", legend="test_cases")
pl2 = plot((1,1,1), best_fit, "green", legend="best fit " + str(round(standard_error_average(data, best_fit))))
pl3 = plot((1,1,1), perfect, "red", "perfect " + str(round(standard_error_average(data, perfect))))
pl4 = plot((1,1,1), test, "purple", "quad " + str(round(standard_error_average(data, test))))
pl5 = plot((1,1,1), ln_data, "pink", "ln " + str(round(standard_error_average(data, ln_data))))
#pl6 = plot((1,1,1), expo_data, "yellow", "ln " + str(round(standard_error_average(data, expo_data))))

pl.legend()
pl.grid()

show()
