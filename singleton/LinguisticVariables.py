from mpmath import iv
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import warnings

warnings.simplefilter("ignore", integrate.IntegrationWarning)
    

class Temperature:
    universe = np.round(np.arange(35,42.1,0.1),1)
    low = {30:1, 34:1, 35:0}
    normal = {34.5:0,35:1,36:1,37.5:0}
    high = {36:0,38:1,40:1}
    input_x = None
    
    def set_input(self,input):
        self.input_x = input
        
    
    def plot(self):
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
        
        #Plot input
        plt.axvline(self.input_x, linestyle='--', color='red', label='input')


        plt.grid(True)
        plt.xlabel('Temperature')
        plt.ylabel('μ(x)')
        plt.legend()
        
        plt.show()
        
        
    def low_mf(self):
        x = list(self.low.keys())
        value = self.input_x
        
        if value < x[1]:
            return 1
        
        if value > x[2]:
            return 0
        
        return (x[2]-value)/(x[2]-x[1])
    
    
    def high_mf(self):
        x = list(self.high.keys())

        value = self.input_x
        
        if(value < x[0]):
            return 0
        if(value > x[1]):
            return 1
        
        return (value-x[0])/(x[1]-x[0])
    
    def normal_mf(self):
        x = list(self.normal.keys())

        value = self.input_x
        
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
        
    
    def calculate_term_firing_strength(self):        
        return {"low": self.low_mf(), "normal":self.normal_mf(), "high": self.high_mf()}
    
    
class Age:
    universe = np.round(np.arange(0,130.1,0.1),1)
    pediatric = {0:1, 10:1, 18:0}
    young_adult = {15:0, 25:1, 35:0}
    adult = {30:0,45:1,60:0}
    old = {50:0,60:1,130:1}
    input_x = None

    def set_input(self,input):
        self.input_x = input

    def plot(self):

        #Plot pediatric
        x = np.array(list(self.pediatric.keys()))
        y = np.array(list(self.pediatric.values()))
        plt.plot(x, y, label='Pediatric')
        
        #Plot young adult
        x = np.array(list(self.young_adult.keys()))
        y = np.array(list(self.young_adult.values()))  
        plt.plot(x, y, label='Young Adult')
        
        #Plot Adult
        x = np.array(list(self.adult.keys()))
        y = np.array(list(self.adult.values()))
        
        plt.plot(x, y, label='Adult')
        
        #Plot High
        x = np.array(list(self.old.keys()))
        y = np.array(list(self.old.values()))
        
        plt.plot(x, y, label='Old')

        #Plot input
        plt.axvline(self.input_x, linestyle='--', color='red', label='input')

        plt.grid(True)
        plt.legend()
        plt.xlabel('Age')
        plt.ylabel('μ(x)')
        
        #show
        plt.show()


    def pediatric_mf(self):
        x = list(self.pediatric.keys())
        value = self.input_x
        
        if value < x[1]:
            return 1
        
        if value > x[2]:
            return 0
        
        return (x[2]-value)/(x[2]-x[1])
    
    def young_adult_mf(self):
        x = list(self.young_adult.keys())

        value = self.input_x

        if value < x[0] or value > x[2]:
            return 0

        if value == x[1]:
            return 1
        
        if value < x[1]:
            return (value - x[0]) / (x[1] - x[0])
        
        return (x[2] - value) / (x[2] - x[1])
        
        
    def adult_mf(self):
        x = list(self.adult.keys())

        value = self.input_x

        if value < x[0] or value > x[2]:
            return 0

        if value == x[1]:
            return 1
        
        if value < x[1]:
            return (value - x[0]) / (x[1] - x[0])
        
        return (x[2] - value) / (x[2] - x[1])
    
    def old_mf(self):
        x = list(self.old.keys())
        value = self.input_x

        if value < x[0] or value > x[2]:
            return 0

        if value > x[1]:
            return 1
        
        return (value - x[0]) / (x[1] - x[0])
        
    
    def calculate_term_firing_strength(self):        
        return {"pediatric":self.pediatric_mf(), "young_adult": self.young_adult_mf(),"adult": self.adult_mf(), "old": self.old_mf()}
        
    
class HeadAche:
    low = {0:1,3:1,6:0}
    moderate = {2:0,5:1,8:0}
    high = {4:0,7:1,10:1}
    input_x = None

    def set_input(self,input):
        self.input_x = input
    
    def plot(self):
        
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

        #Plot input
        plt.axvline(self.input_x, linestyle='--', color='red', label='input')

        plt.grid(True)
        plt.legend()
        
        #show
        plt.show()
        
    def low_mf(self):
        x = list(self.low.keys())
        value = self.input_x
        if(value <= x[1]):
            return 1
        
        if(value > x[2]):
            return 0
        
        return (x[2]- value)/(x[2]-x[1])
    
    
    def moderate_mf(self):
        x = list(self.moderate.keys())
        value = self.input_x
        if(value < x[0]):
            return 0
        
        if(value > x[2]):
            return 0
        
        if(value == x[1]):
            return 1
        
        if value < x[1]:
            return (value - x[0])/(x[1] - x[0])

        return (x[2] - value) / (x[2] - x[1])
        
        
    
    def high_mf(self):
        x = list(self.high.keys())
        value = self.input_x
        if(value < x[0]):
            return 0
        
        if(value > x[1]):
            return 1
        
        return (value - x[0])/(x[1] - x[0])
            
    def calculate_term_firing_strength(self):        
        return {"low": self.low_mf(), "moderate":self.moderate_mf(), "high": self.high_mf()}
