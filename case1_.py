
import numpy as np
import matplotlib.pyplot as plt

class Temperature:
    universe = np.round(np.arange(35,42.1,0.1),1)
    low = {30:1, 34:1, 35:0}
    normal = {34.5:0,35:1,36:1,37.5:0}
    high = {36:0,38:1,40:1}
    
    def plot(self, val):
        #Plot low
        x = np.array(list(self.low.keys()))
        y = np.array(list(self.low.values()))
        
        plt.plot(x, y, label='Low')
        
        #Plot normal
        x = np.array(list(self.normal.keys()))
        y = np.array(list(self.normal.values()))
        
        plt.plot(x, y, label='Normal')
        
        #Plot High
        x = np.array(list(self.high.keys()))
        y = np.array(list(self.high.values()))
        
        plt.plot(x, y, label='High')
        
        #Plot value
        plt.axvline(x=val, color = 'black', linestyle='--')
        
        #show
        plt.show()
        
        
    def low_mf(self,value):
        x = list(self.low.keys())
        
        if value < x[1]:
            return 1
        
        if value > x[2]:
            return 0
        
        return (x[2]-value)/(x[2]-x[1])
    
    
    def high_mf(self,value):
        x = list(self.high.keys())
        
        if(value < x[0]):
            return 0
        if(value > x[1]):
            return 1
        
        return (value-x[0])/(x[1]-x[0])
    
    def normal_mf(self,value):
        x = list(self.normal.keys())
        
        if(value >= x[1] and value <= x[2]):
            return 1
        if(value <= x[0]):
            return 0
        if(value >= x[3]):
            return 0
        if(value > x[0] and value < x[1]):
            return (value - x[0])/(x[1]-x[0])
        if(value > x[2] and value < x[3]):
            return (x[3]-value) / (x[3]-x[2])
        
    def calculate_mf(self,value):
        return [self.low_mf(value),self.normal_mf(value),self.high_mf(value)]
    
    
        
class HeadAche :
    low = {0:1,2:1,4:0}
    moderate = {3:0,4:1,7:1}
    high = {6:0,8:1,10:1}
    
    def plot(self, val):
        
        #Plot low
        x = np.array(list(self.low.keys()))
        y = np.array(list(self.low.values()))
        
        plt.plot(x, y, label='Low')
        
        #Plot moderate
        x = np.array(list(self.moderate.keys()))
        y = np.array(list(self.moderate.values()))
        
        plt.plot(x, y, label='Moderate')
        
        #Plot High
        x = np.array(list(self.high.keys()))
        y = np.array(list(self.high.values()))
        
        plt.plot(x, y, label='High')
        
        #Plot value
        plt.axvline(x=val, color = 'black', linestyle='--')
        
        #show
        plt.show()
        
    def low_mf(self,value):
        x = list(self.low.keys())
        if(value <= x[1]):
            return 1
        
        if(value > x[2]):
            return 0
        
        return (x[2]- value)/(x[2]-x[1])
    
    
    def moderate_mf(self,value):
        x = list(self.moderate.keys())
        if(value < x[0]):
            return 0
        
        if(value > x[2]):
            return 0
        
        if(value > x[1] and value < x[2]):
            return 1
        
        return (value - x[0])/(x[1] - x[0])
    
    
    def high_mf(self,value):
        x = list(self.high.keys())
        if(value < x[0]):
            return 0
        
        if(value > x[1]):
            return 1
        
        return (value - x[0])/(x[1] - x[0])
        
 
        
