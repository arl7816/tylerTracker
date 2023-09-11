from math import log, pow, e, sin, cos

def f(n: int) -> int:
  return log(2 * n) + 3 * n

def base_test(n: float, coes: list):
  return pow(n, 2) * coes[0] + n * coes[1] + coes[2]

def base_test_d_d0(x: float, y: float, coes: list) -> float:
  return -2 * (y - coes[0] * (x * x) - coes[1] * x - coes[2]) * (x * x)

def base_test_d_d1(x: float, y: float, coes: list) -> float:
  return -2 * (y - coes[0] * (x * x) - coes[1] * x - coes[2]) * x

def base_test_d_d2(x: float, y: float, coes: list) -> float:
  return -2 * (y - coes[0] * (x * x) - coes[1] * x - coes[2])

def ln_test(n: float, coes: list) -> float:
  if n <= 0:
    n = 0.00001
  if coes[2] <= 0:
    coes[2] = 0.00001
  return coes[0] + coes[1] * log(coes[2] * n)

def ln_test_d0(x: float, y: float , coes: list) -> float:
  if x <= 0:
    x = 0.00001
  if coes[2] <= 0:
    coes[2] = 0.00001
  #print("x:", x, "y:", y, "coes:", coes)
  return -2 * (y - coes[0] - coes[1] * log(coes[2] * x))

def ln_test_d1(x: float, y: float, coes: list) -> float:
  if x <= 0:
    x = 0.00001
  if coes[2] <= 0:
    coes[2] = 0.00001
  return -2 * log(coes[2] * x) * (y - coes[0] - coes[1] * log(coes[2] * x))

def ln_test_d2(x: float, y: float, coes: list) -> float:
  if x <= 0:
    x = 0.00001
  if coes[2] <= 0:
    coes[2] = 0.00001
  return -2 * coes[1] / coes[2] * (y - coes[0] - coes[1] * log(coes[2] * x))

def expo_func(n: float, coes: list):
  return coes[0] + coes[1] * pow(e, n * coes[2])

def expo_d0(x: float, y: float, coes: list) -> float:
  return -2 * (y - expo_func(x, coes))

def expo_d1(x: float, y: float, coes: list) -> float:
  return -2 * (y - expo_func(x, coes)) * pow(e, x * coes[2])

def expo_d2(x: float, y: float, coes: list) -> float:
  return -2 * (y - expo_func(x, coes)) * coes[1] * coes[2] * pow(e, coes[2] * x)

def trig_test(n : float, coes: list) -> float:
  return coes[0] + coes[1] * sin(coes[2] * n) + coes[3] * cos(coes[4] * n)

def trig_d0(x: float, y: float, coes: list) -> float:
  return -2 * (y - trig_test(x, coes))

def trig_d1(x: float, y: float, coes: list) -> float:
  return 2 * (y - trig_test(x, coes)) * sin(coes[2] * x)

def trig_d2(x: float, y: float, coes: list) -> float:
  return 2 * (y - trig_test(x, coes)) * coes[1] * x * cos(coes[2] * x)

def trig_d3(x: float, y: float, coes: list) -> float:
  return 2 * (y - trig_test(x, coes)) * cos(coes[4] * x)

def trig_d4(x: float, y: float, coes: list) -> float:
  return -2 * (y - trig_test(x, coes)) * coes[3] * x * sin(coes[4] * x)