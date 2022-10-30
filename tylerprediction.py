import numpy
import TylerClasses as tyclasses
from random import randint as ran

T_DATA = tyclasses.TylerData("tylertrack.txt")

def random_prediction(yo=0, y=120) -> int:
  return ran(yo, y)

def random_prediction_unbalanced() -> int:
  chance = ran(0,100)
  if chance <= 40:
    return ran(0,10)
  elif chance <= 70:
    return ran(11,25)
  elif chance <= 85:
    return ran(26, 50)
  elif chance <= 95:
    return ran(51, 60)
  elif chance <= 100:
    return ran(60,120)

def slope_prediction(data: tyclasses.Data, x: int) -> int:
  xn1 = data.x[x-1]
  xn2 = data.x[x-2]
  
  deltaY = data.y[xn1] - data.y[xn2]
  deltaX = xn1 - xn2
  slope = deltaY/deltaX

  yn1 = data.y[xn1]

  y = slope*(deltaX) + yn1
  return y

def slope_prediction_average(data: tyclasses.Data, x: int) -> int:
  average_slope = 0
  tempx = x 
  while tempx >= 2 and len(data.x) >= 2:
    xn1 = data.x[tempx-1]
    xn2 = data.x[tempx-2]

    deltaY = data.y[xn1] - data.y[xn2]
    deltaX = xn1 - xn2
    slope = deltaY/deltaX

    average_slope += slope
    tempx -= 1
  average_slope /= x

  xn1 = data.x[x-1]
  xn2 = data.x[x-2]
  
  deltaX = xn1 - xn2

  yn1 = data.y[xn1]

  y = average_slope*(deltaX) + yn1
  return y

def der_prediction(data: tyclasses.Data, x: int) -> int:
  x -= 1
  new_data = tyclasses.Data(tyclasses.Data((data.x, data.y)).derivative())

  m = new_data.y[x]
  yo = data.y[x]
  deltaX = (x+1) - x

  return m*deltaX+yo # y coor

def entry_prediction(data: tyclasses.Data, x: int) -> int:
  print(x)

  def form_entries(data: tyclasses.Data, x: int) -> tyclasses.Data:
    weekdays = [i % 5 + 1 for i in range(x)]
    backwards = [3,2,1,5,4]
    for index, element in enumerate(weekdays):
      weekdays[index] = backwards[element - 1]
    
    temp_data = [i for i in range(x)]

    print(len(temp_data))
    print(len(weekdays))
    weekdays = tyclasses.Data((temp_data, weekdays))
    weekdays.remap(data.get_max())
    print("Weekdays:", len(weekdays.y))
    return weekdays
  
  entries = tyclasses.Data(form_entries(data, x).smooth_data())
  print("len:", len(entries.y))
  entries = tyclasses.Data(entries.derivative())

  m = entries.y[x]
  yo = data.y[x-1]

  xn1 = x-1

  y = m(x - xn1) + yo
  return y


def predict_future():
  pass

def predict(data: tyclasses.TylerData, x, expected=False):
  x -= 1
  def get_error(e: int, a: int) -> int:
    return round(abs(e-a)/e * 100)

  def format_error(e: int,a: int) -> str:
    return "{actual: " + str(e) + " Precent Error: " + str(get_error(e, a)) + "%}"

  random = random_prediction()
  random_unbal = random_prediction_unbalanced()
  slope_pred = slope_prediction(data, x)
  slope_pred_aver = slope_prediction_average(data, x)
  der_pre = der_prediction(data, x)
  #entr_der_pre = entry_prediction(data, x)

  y = None
  if expected:
    y = data.y[x]

  if not expected:
    print("Doing a random guess: (x,l(x)) = (" + str(x) + "," + str(random) + ")")
    print("Doing a unbalanced guess: (x, l(x) = (" + str(x) + "," + str(random_unbal) + ")")
    print("Doing a slope prediction: (x,l(x) = (" + str(x) + "," + str(slope_pred) + ")")
    print("Doing a average slope prediction: (x,l(x) = (" + str(x) + "," + str(slope_pred_aver) + ")")
    print("Doing a derivative prediction: (x, l(x)) = (" + str(x) + "," + str(der_pre) + ")")
    print("Doing a entry derivative prediction: (x,l(x)) = (" + str(x) + "," + str(entr_der_pre) + ")")
  else:
    print("Doing a random guess: (x,l(x)) = (" + str(x) + "," + str(random) + ") " + format_error(y, random))
    print("Doing a unbalanced guess: (x, l(x) = (" + str(x) + "," + str(random_unbal) + ") " + format_error(y, random_unbal))
    print("Doing a slope prediction: (x,l(x) = (" + str(x) + "," + str(slope_pred) + ") " + format_error(y, slope_pred))
    print("Doing a average slope prediction: (x,l(x) = (" + str(x) + "," + str(slope_pred_aver) + ") " + format_error(y, slope_pred_aver))
    print("Doing a derivative prediction: (x, l(x)) = (" + str(x) + "," + str(der_pre) + ")" + format_error(y, der_pre))
    #print("Doing a entry derivative prediction: (x,l(x)) = (" + str(x) + "," + str(entr_der_pre) + ")" + format_error(y, entr_der_pre))
