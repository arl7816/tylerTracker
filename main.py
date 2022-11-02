import matplotlib
import TylerClasses as tyclass
import tyler as tymethod
import numpy as np
import tylerprediction as typre

def main() -> None:
  data = tyclass.TylerData("tylertrack.txt")
  
  lateness = tyclass.Data((data.get_xaxis(), data.axis_into_data("lateness")))

  weekdays = [i % 5 + 1 for i in range(len(lateness.x))]
  backwards = [3,2,1,5,4]
  for index, element in enumerate(weekdays):
    weekdays[index] = backwards[element - 1]
  weekdays = tyclass.Data((data.get_xaxis(), weekdays))
  weekdays.remap(lateness.get_max())

  #late_graph = tymethod.plot((2,1,2), lateness, "blue", "lateness (in minutes)", key="lateness")

  #tymethod.set_labels("lateness", "Entry points", "lateness (in minutes)", "What aee doinng Tylaa u silly boi u `:(")

  #tymethod.plot((2,1,2), weekdays, "orange", "entry # (1-5)", key="weekdays")

  #tymethod.plot((2,1,2), tyclass.Data(lateness.line_of_best_fit()), "red", legend="Line of best fit (lateness)")
  #tymethod.plot((2,1,2), tyclass.Data(weekdays.line_of_best_fit()), "purple", legend="Line of best fit (weekdays)")

  #late_graph = tymethod.plot((2,1,2), tyclass.Data(lateness.smooth_data()), "purple")
  smooth_weekdays = tyclass.Data(weekdays.smooth_data())
  #tymethod.plot((2,1,2), smooth_weekdays, "orange")

  #late_graph.grid()
  #late_graph.legend()
  
  day_average = tyclass.Data((["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], lateness.get_averages(True, weekdays.y)[1]))

  tymethod.bar((2,2,1), day_average, color="purple", key="bar")
  tymethod.set_labels("bar", "Days of the week", "Average lateness (minutes)", "Average lateness per day")

  tymethod.bar((2,2,2), tyclass.Data(tyclass.Data(data.convert_into_data("class_name", "lateness")).get_averages(True)), "green", key="class")
  tymethod.set_labels("class", "classes" , "average lateness (minutes)", "Average lateness per class")

  #tymethod.plot((2,1,2), tyclass.Data(smooth_weekdays.derivative()), "black")

  xs = []
  r1 = []
  r_unb = []
  slope_pre = []
  slope_pre_aver = []
  der_pre = []
  entr_der_pre = []

  for i in range(5, len(lateness.x)):
    xs.append(i)
    result = typre.predict(lateness, i, True)
    r1.append(result[0])
    r_unb.append(result[1])
    slope_pre.append(result[2])
    slope_pre_aver.append(result[3])
    der_pre.append(result[4])
    entr_der_pre.append(result[5])
  
  tymethod.plot((2,1,2), tyclass.Data((xs, r1)), "red", key="error")
  tymethod.plot((2,1,2), tyclass.Data((xs, r_unb)), "blue")
  tymethod.plot((2,1,2), tyclass.Data((xs, slope_pre)), "green")
  tymethod.plot((2,1,2), tyclass.Data((xs, slope_pre_aver)), "purple")
  tymethod.plot((2,1,2), tyclass.Data((xs, der_pre)), "black")
  tymethod.plot((2,1,2), tyclass.Data((xs, entr_der_pre)), "orange")

  tymethod.subplots["error"].grid()

  tymethod.show()

  



if __name__ == "__main__":
  main()