from dataclasses import dataclass
import numpy as np
from scipy.interpolate import make_interp_spline

class Data():
  """[summary]
  class used to keep track of two sets of data and manipulate them

  Raises:
    Exception: tuple must provie two arrays in the form of tuple
    Exception: both the x and y axis must have the same number of element
  """
  x = np.array([])
  y = np.array([])

  def __init__(self, data: tuple) -> None:
    """[summary]
    The constructor of the Data class

    Args:
      data (tuple): both the x and y axis of the initial data

    Raises:
      Exception: tuple must provie two arrays in the form of tuple
      Exception: both the x and y axis must have the same number of element
    """
    if len(data) != 2: raise Exception("the data must consist of two arrays")
    if len(data[0]) != len(data[1]):  raise Exception("x and y must be the same")
    self.x = np.array(data[0])
    self.y = np.array(data[1])

  def inverseX(self) -> None:
    """[summary]
      transforms each element of the xaxis into the reciprocal the element
    
    Returns:
      None
    """
    for i in range(len(self.x)):
      if (self.x[i] == 0): continue
      self.x[i] = 1/self.x[i]
  
  def insert(self, x, y, index=0) -> None:
    """[summary] not yet implemented

    Args:
        x (_type_): _description_
        y (_type_): _description_
        index (int, optional): _description_. Defaults to 0.
    """
    return

  def line_of_best_fit(self) -> list:
    """[summary] Gets the line of best fit for your data

    Preconditions:
      both x and y values are integers or floats

    Returns:
        list: an numpy array
    """
    a, b = np.polyfit(self.x, self.y, 1)

    return (self.x, a*self.x+b)

  def smooth_data(self, smoothness = 500) -> tuple:
    """[summary] Smooths out the data thats gets displayed

    Args:
      smoothness (int, optional): The amount of data points generated between x values (linear line is 50). Defaults to 500.

    Raises:
      Exception: smoothness of the line is less than 0

    Returns:
        tuple: your new data points, in the form of (x axis, y axis)
    """

    if (smoothness < 0):
      raise Exception("Smoothness of the data must be above or equal to 0")

    X_Y_Spline = make_interp_spline(self.x, self.y)
 
    # Returns evenly spaced numbers
    # over a specified interval.
    X_ = np.linspace(self.x.min(), self.x.max(), smoothness)
    Y_ = X_Y_Spline(X_)

    return (X_, Y_)

  def derivative(self) -> tuple:
    """[summary] get the derivative of any line (recommend smoothing out data points first, for very linear plots)

    Returns:
        tuple (list[int], list[int]): returns a tuple of arrays representing the x and y coordinates of the derivative
    """
    
    x = self.x
    y = self.y
    der = np.diff(y) / np.diff(x)
    x2 = (x[:-1] + x[1:]) / 2
    return (x2, der)
  

  def get_max(self) -> int:
    """[summary] Gets the max element from the y axis

    Returns:
        int: the max element within the y axis
    """
    return self.y.max()
  

  def remap(self, max = None) -> None:
    """[summary] stretches each of the data points on the y axis, so that the data fits more nicely between 
    a maximum number and 0

    Args:
      max (int, optional): The highest number the y should stretch to. Defaults to the max value of the object.

    Returns:
      None
    """
    if max == None: max = self.get_max()

    for index, element in enumerate(self.y):
      self.y[index] = max / element


  def get_averages(self, sort=False, x=None, y=None) -> tuple:
    """[summary] Gets the averages for every x value that repeats

    Args:
      sort (bool, optional): determines whether or not to sort the average x axis. Defaults to False
      x (list, optional): the x axis to get averages for. Defaults to the objects x axis
      y (list, optional): the y axis to get averages for. Defaults to the objects y axis 

    Returns:
        tuple(list, list): the x axis and the y axis representing the average of the given x element
    """
    averages = dict()
    xaxis = []
    yaxis = []
    if type(x) == type(None): x = self.x
    if type(y) == type(None): y = self.y

    for index in range(len(x)):
      if x[index] not in averages:
        averages[x[index]] = {
          "value": 0,
          "amount": 0
        }
      averages[x[index]]["value"] += y[index]
      averages[x[index]]["amount"] += 1
    
    for key in averages.keys():
      xaxis.append(key)
    
    if sort:
      xaxis.sort()

    for key in xaxis:
      yaxis.append(averages[key]["value"] / averages[key]["amount"])

    return xaxis, yaxis
    

@dataclass # decorater
class TylerDataPoint():
  """[summary] a dataclass that represents a event in tylers history of lateness
  
  Attributes: 
    days (int): the day of the week (1=Monday, 5=Friday)
    date (str): the date of the occurance (##/##/####)
    lateness (int): the time of his lateness (x -> R)
    class_name (str): the name of his class
    class_time (str): the time the class starts in military time (##:##)
  """
  day: int
  date: str
  lateness: int 
  class_name: str
  class_time: str

  def __getitem__(self, item: str):
    """[summary] Is used to get a attribute using the syntax, TylerDataPoint["attribute"]

    Args:
      item (str): the attribute in question

    Returns:
      Any: the desired attribute
    """
    return getattr(self, item)


class TylerData():
  """[summary] Holds a collection of TylerDataPoints based on a given file of data
  """
  entries = []

  def get_xaxis(self) -> list:
    """[summary] gets the x axis for the data entries.

    Returns:
      list: a list of numbers between 0 and (length of entries)-1
    """
    return [i for i in range(len(self.entries))]

  def get_data(self, file_name: str) -> list:
    """[summary] converts the data within a text file to a list of TylerDataPoints

    Preconditions:
      1. the filename is in the same directory
      2. the data points are seperated by 1 space
      3. the data points are given in the following order:
        Day (monday=1) | date | lateness | class | class-time

    Args:
        file_name (str): the file name of tylers lateness

    Raises:
        Exception: throws error if something in the text file doesnt match the 3rd pre-condition

    Returns:
        list: of TylerDataPoints
    """
    data = []
    with open(file_name, encoding="utf-8", mode="r") as file:
      for line in file:
        if line[0] == "*":
          continue

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
  def axis_into_data(self, compareTo: str) -> list:
    """[summary] converts a part of the data entries into a list

    Args:
        compareTo (str): The thing you want converted into a list

    Returns:
        list: a list of data points
    """
    data = []
    for entry in self.entries:
      data.append(entry[compareTo])
    return data

  def convert_into_data(self, xaxis: str, yaxis: str) -> tuple:
    """[summary] converts two parts of the data into a x and y axis

    Args:
        xaxis (str): the thing you want converted into your x axis
        yaxis (str): the thing you want converted into your y axis

    Returns:
        tuple(list, list): the x and y data points
    """
    x = []
    y = []
    for entry in self.entries:
      x.append(entry[xaxis])
      y.append(entry[yaxis])
    return (x, y)


  def __init__(self, file_name: str) -> None:
    """[summary] the constructor

    Args:
        file_name (str): the file name you want converted into data points
    """
    self.entries = self.get_data(file_name)