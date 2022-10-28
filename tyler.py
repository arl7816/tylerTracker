from matplotlib import pyplot as plt
from TylerClasses import *
  
def graph(lateness: Data, weekdays: Data):
  plt.plot(lateness.x, lateness.y, label="lateness", marker="o")

  plt.title("Tyler, what you doin silly boi???!!!! :`(")
  plt.ylabel("Lateness in minutes (m)")
  plt.xlabel("Days")

  plt.plot(weekdays.x, weekdays.y, label="weekdays (1-5)", marker="o")

  plt.grid()
  plt.legend()

  plt.show()


def plot():
  pass

def show():
  plt.show()