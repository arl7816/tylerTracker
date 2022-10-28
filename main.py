from TylerClasses import *
from tyler import *

def main() -> None:
  data = TylerData("tylertrack.txt")
  data.convert_into_data("lateness")

  # is in minutes
  lateness = [
    30,
    30,
    30,
    90,
    90,
    37,
    4,
    6,
    8,
    55,
    -2,
    4,
    55,
    -2
  ]
  days = [i for i in range(len(lateness))]
  
  weekdays = [i % 5 + 1 for i in range(len(lateness))]

  backwards = [3,2,1,5,4]
  for index, element in enumerate(weekdays):
    weekdays[index] = backwards[element - 1]
  
  
  lateness_data = Data(days, lateness)
  weekdays_data = Data(days, weekdays)
  weekdays_data.remap(lateness_data.get_max())

  print(data.convert_into_data("lateness"))
  print(lateness)

  graph(lateness_data, weekdays_data)



if __name__ == "__main__":
  main()