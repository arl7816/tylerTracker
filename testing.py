from TylerClasses import Data
from tyler import *
from random import random
from math import e, pow, log, sqrt
from math_funcs import *

def nudge():
  return random() * 2

def sigmoid_pos(x: float) -> float:
  return 1 / (1 + pow(e, -x + pow(e, 2)))

def standard_error_average(data: Data, predictions: Data, percent = False):
  sigma = 0
  length = len(data.y)
  for index in range(length):
    sigma += pow(data.y[index] - predictions.y[index], 2)

  if percent:
    return sigmoid_pos(sigma / length) * 100
  return sqrt(sigma / length)

def use_function(coes: list, x: float) -> float:
  n = len(coes)
  sigma = 0
  for i in range(n):
    sigma += coes[i] * pow(x, i)
  return sigma

def generate_function_v1(dataset: Data, model: object ,partials: list, coes: list, alpha = .1, iterations = 100_000, print_me=False) -> list:
  def gradient(dataset: Data, model: object, partial: object, coes: list) -> float:
    sigma = 0
    n = len(dataset.x)
    for index in range(n):
      sigma += partial(dataset.x[index], dataset.y[index], coes)

    return sigma / n

  for _ in range(iterations):
    for i in range(len(coes)):
      coes[i] = coes[i] - alpha * gradient(dataset, model, partials[i], coes)
    if print_me:
      print("error is now at", standard_error_average(dataset, Data((dataset.x, [base_test(x, coes) for x in x_test]))))
  return coes
    

def generate_function_v2(dataset: Data, model: object ,partials: list, coes: list, alpha = .1, iterations = 100_000, print_me=False) -> list:
  def gradient(dataset: Data, model: object, partial: object, coes: list) -> float:
    sigma = 0
    demo_sigma = 0
    n = len(dataset.x)
    for index in range(n):
      sigma += partial(dataset.x[index], dataset.y[index], coes)
      demo_sigma += pow(dataset.y[index] - model(dataset.x[index], coes), 2)

    return sigma / (2 * sqrt(demo_sigma * n))

  for _ in range(iterations):
    for i in range(len(coes)):
      coes[i] = coes[i] - alpha * gradient(dataset, model, partials[i], coes)
    if print_me:
      print("error is now at", standard_error_average(dataset, Data((dataset.x, [base_test(x, coes) for x in x_test]))))
  return coes

x_test = [n for n in range (1,100, 3)]
y = [f(n) + nudge() for n in x_test]

y2 = [f(n) for n in x_test]

data = Data((x_test, y))
best_fit = Data(data.line_of_best_fit())
perfect = Data((x_test, y2))

constants = generate_function_v1(data, base_test, [base_test_d_d0, base_test_d_d1, base_test_d_d2], [1,1,1], .000000001, print_me=False, iterations=10_000)
print("Quad constants =", constants)
y3 = [base_test(x, constants) for x in x_test]
test = Data((x_test, y3))

ln_constants = generate_function_v1(data, ln_test, [ln_test_d0, ln_test_d1, ln_test_d2], [1,1,1], 0.00011, 10_000)
print("ln constants =", ln_constants)
y4 = [ln_test(x, constants) for x in x_test]
ln_data = Data((x_test, y4))

"""expo_constants = generate_function_v1(data, expo_func,  [expo_d0, expo_d1, expo_d2], [1,1,1], .000000000000000000000001, 100_000 , print_me=False)
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
