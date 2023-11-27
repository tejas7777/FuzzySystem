from mpmath import iv
import numpy as np
from nonsingleton import LinguisticVariables
from tnorm import Tnorm
import pandas as pd
import matplotlib.pyplot as plt

class Urgency:
    universe = np.arange(0,101,1)
    low = {0:1,25:1, 50:0}
    moderate = {25:0,50:1, 75:0}
    high = {50:0,75:1,100:1}

    def plot(self):
        #Plot low
        x = np.array(list(self.low.keys()))
        y = np.array(list(self.low.values()))
        
        plt.plot(x, y, label='Low', color='black')
        
        #Plot normal
        x = np.array(list(self.moderate.keys()))
        y = np.array(list(self.moderate.values()))
        
        plt.plot(x, y, label='Moderate', color='black')
        
        #Plot High
        x = np.array(list(self.high.keys()))
        y = np.array(list(self.high.values()))
        
        plt.plot(x, y, label='High', color='black')
        
        #Plot input
        #plt.plot(self.input_x, self.input_mf, linestyle='--', color='red')

        plt.grid(True)
        plt.xlabel('Urgency')
        plt.ylabel('μ(x)')
        
        plt.show()

    def low_mf(self,value):
        x = list(self.low.keys())
        
        if value < x[1]:
            return 1
        
        if value > x[2]:
            return 0
        
        return (x[2]-value)/(x[2]-x[1])
    

    def moderate_mf(self,value):
        x = list(self.moderate.keys())
        
        if(value <= x[0] or value >= x[2]):
            return 0

        if(value == x[1]):
            return 1
        
        if(value < x[1]):
            return (value-x[0])/(x[1]-x[0])
        
        return (x[2] - value)/(x[2]-x[1])
        
    

    def high_mf(self,value):
        x = list(self.high.keys())
        
        if(value < x[0]):
            return 0
        if(value > x[1]):
            return 1
        
        return (value-x[0])/(x[1]-x[0])


    def  generate_output_set(self,mf,term):
        input_range = None
        callable_function = None

        if term == 'low':
            x = list(self.low.keys())
            input_range = [x[0],x[-1]]
            callable_function = self.low_mf

        if term == 'moderate':
            x = list(self.moderate.keys())
            input_range = [x[0],x[-1]]
            callable_function = self.moderate_mf

        if term == 'high':
            x = list(self.high.keys())
            input_range = [x[0],x[-1]]
            callable_function = self.high_mf

        output_set = []

        for xi in range(input_range[0], input_range[-1]+1):
            output_set.append((min(mf,callable_function(xi)), xi))
            #output_set[xi] = min(mf, callable_function(xi))

        return output_set
    


