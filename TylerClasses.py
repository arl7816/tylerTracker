from dataclasses import dataclass
import numpy as np

class Data():
  def __init__(self, x, y) -> None:
    if (len(y) != len(x)):
      raise Exception("x and y must be the same")
    
    self.x = np.array(x)
    self.y = np.array(y)

  def inverseX(self) -> None:
    for i in range(len(self.x)):
      if (self.x[i] == 0): continue
      self.x[i] = 1/self.x[i]
    print(self.x)
  
  def insert(self, x, y) -> None:
    return

  def line_of_best_fit(self) -> list:
    return np.polyfit(self.x, self.y, 1)
  
  def get_max(self) -> int:
    return self.y.max()
  
  def remap(self, max=None) -> None:
    if max == None: max = self.get_max()

    for index, element in enumerate(self.y):
      self.y[index] = max / element

@dataclass
class TylerDataPoint():
  day: int
  date: str
  lateness: int 
  class_name: str
  class_time: str

  def __getitem__(self, item):
    return getattr(self, item)


class TylerData():
  entries = []

  def get_data(self, file_name) -> list:
    data = []
    with open(file_name, encoding="utf-8", mode="r") as file:
      for line in file:
        if line[0] == "*":
          continue

        print(line)
        line.strip()
        line_data = line.split(" ")

        if len(line_data) != 5:
          raise Exception("Something in", file_name, "doesnt have the correct amount of info")
      
        day = int(line_data[0])
        date = line_data[1]
        lateness = int(line_data[2])
        class_name = line_data[3]
        class_time = line_data[4]

        data_point = TylerDataPoint(day, date, lateness, class_name, class_time)
        data.append(data_point)
    return data
  
  # converts a part of the data entries into a Data class such as days vs lateness
  def convert_into_data(self, compareTo: str) -> list:
    data = []
    for entry in self.entries:
      data.append(entry[compareTo])
    return data

  def __init__(self, file_name) -> None:
    self.entries = self.get_data(file_name)