from matplotlib import pyplot as plt
from TylerClasses import *

subplots = dict()

def graph(lateness: Data, weekdays: Data):
  plt.plot(lateness.x, lateness.y, label="lateness", marker="o")

  plt.title("Tyler, what you doin silly boi???!!!! :`(")
  plt.ylabel("Lateness in minutes (m)")
  plt.xlabel("Days")

  plt.plot(weekdays.x, weekdays.y, label="weekdays (1-5)", marker="o")

  plt.grid()
  plt.legend()

  plt.show()


def plot(trt: tuple, data: Data, color, legend="", marker="o", key=None):
  if key == None:
    key = trt

  sub = plt.subplot(trt[0], trt[1], trt[2])
  subplots[key] = sub

  sub.plot(data.x, data.y, label=legend, color=color)
  return sub

def bar(trt: tuple, data: Data, color, legend="", marker="o", key=None):
  if key == None:
    key = trt

  sub = plt.subplot(trt[0], trt[1], trt[2])
  subplots[key] = sub

  sub.bar(data.x, data.y, label=legend, color=color)
  return sub

def set_labels(key: str, xlabel: str, ylabel: str, title: str):
  subplots[key].set_title(title)
  subplots[key].set_xlabel(xlabel)
  subplots[key].set_ylabel(ylabel)

def show():
  plt.show()