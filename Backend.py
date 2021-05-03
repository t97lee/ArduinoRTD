from pyfirmata import Arduino, util
import time
from jupyterplot import ProgressPlot

board = Arduino('#PORT')
it = util.Iterator(board)
it.start()
vol = board.get_pin("a:0:i")

#variables for calculating the temperature
voltage_source = 5
R_known = 1000 #Value of the known resistor 
alpha = 0.00385 #temperature coefficient 
temp_ref = -5 #temperature reference
R_ref = 1000 #resistance of RTD (part no. F2222-1000-A-100)
                                                                            
pp = ProgressPlot()

while True:
    voltages = vol.read() * 5 #scales voltage to 5V
    
    R_rtd = (R_known) * (voltage_source - voltages)/voltages #eq. 1-8 to find R of RTD
    
    temps = temp_ref + (R_rtd / R_ref - 1) / alpha #eq. 3-3 to solve for T (temperature)
    
    pp.update(temps) #updates the graph with temperatures over time, 
    
    time.sleep(60) #frequency of data collection

pp.finalize()
       
#NOTES: 
#y-axis on the plot is temperature (in °C), x-axis is time (in minutes)
