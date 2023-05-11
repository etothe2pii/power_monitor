from jtop import jtop
import time
import subprocess as sb
from threading import Thread

class power_monitor:
    
    def __init__(self, interval):
        self.data = [["Time","Total_Cur","Total_Avg","GPU_Cur","GPU_Avg","CPU_Cur,CPU_Avg"]]
        self.interval = interval
        self.stop = False
        self.start_time = 0
        self.thread = None

    def start_power_monitor(self):
        self.stop = False
        self.start_time = time.time()
        self.thread = Thread(target=self.monitor_power)

        self.thread.start()

    def stop_power_monitor(self):
        self.stop = True
        self.thread.join()

    def print_data(self, output_file):
        with open(output_file, "w") as file:
            for d in self.data:
                for i in range(len(d)):
                    file.write(str(d[i]))

                    if i < len(d) - 1:
                        file.write(",")
                file.write("\n")

    def monitor_power(self):
        with jtop(interval = self.interval) as jetson:
            while not self.stop and jetson.ok():
                new_data = []
                new_data.append(time.time() - self.start_time)
                new_data.append(jetson.power[0]["cur"])
                new_data.append(jetson.power[0]["avg"])
                new_data.append(jetson.power[1]["GPU"]["cur"])
                new_data.append(jetson.power[1]["GPU"]["avg"])
                new_data.append(jetson.power[1]["CPU"]["cur"])
                new_data.append(jetson.power[1]["CPU"]["avg"])
                self.data.append(new_data)

    def monitor_function(self, function, iterations = 100, output_file = "data.csv"):
        self.start_power_monitor()
        for i in range(iterations):
            function()
        
        self.stop_power_monitor()

        self.print_data(output_file)




