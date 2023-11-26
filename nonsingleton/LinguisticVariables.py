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
    input_mf = None
    input_x = None
    
    
    def get_pdf_value(self,x):
        if self.input_mf is None:
            return 0
        if x <= self.input_x.min() or x >= self.input_x.max():
            return 0
        
        return self.input_mf[np.abs(self.input_x - x).argmin()]
    
    def set_input_interval(self,interval):
        np_interval = np.array(interval)
        mu = np_interval.mean()
        sigma = 0.2
        self.input_x = np.linspace(interval[0], interval[1], int((interval[1] - interval[0]) / 0.1) + 1)
        #pdf = norm.pdf(self.input_x, mu, sigma)
        #pdf /= pdf.max()
        
        pdf = np.exp(-0.5 * ((self.input_x - mu) / sigma) ** 2)

        # Scale the PDF
        pdf /= pdf.max()
        self.input_mf = pdf
        
    
    def plot(self):
        #Plot low
        x = np.array(list(self.low.keys()))
        y = np.array(list(self.low.values()))
        
        plt.plot(x, y, label='Low', color='black')
        
        #Plot normal
        x = np.array(list(self.normal.keys()))
        y = np.array(list(self.normal.values()))
        
        plt.plot(x, y, label='Normal', color='black')
        
        #Plot High
        x = np.array(list(self.high.keys()))
        y = np.array(list(self.high.values()))
        
        plt.plot(x, y, label='High', color='black')
        
        #Plot input
        plt.plot(self.input_x, self.input_mf, linestyle='--', color='red')


        plt.grid(True)
        plt.xlabel('Temperature')
        plt.ylabel('μ(x)')
        
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
        
        
    def calculate_low_firing_strength(self):
        low_x = list(self.low.keys())
        X = np.intersect1d( self.input_x, np.linspace(low_x[0], low_x[2], int((low_x[2] - low_x[0]) / 0.1) + 1))
        
        
        integrand1 = lambda x: min(self.low_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value
        
        result1, error1 = integrate.quad(integrand1, X.min(), X.max())
        result2, error2 = integrate.quad(integrand2, X.min(), X.max())
        
        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2
 
    def calculate_normal_firing_strength(self):
        normal_x = list(self.normal.keys())
        X = np.intersect1d( self.input_x, np.linspace(normal_x[0], normal_x[-1], int((normal_x[-1] - normal_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        integrand1 = lambda x: min(self.normal_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value
        
        result1, error1 = integrate.quad(integrand1, X.min(), X.max())
        result2, error2 = integrate.quad(integrand2, X.min(), X.max())
        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2

        
        
    def calculate_high_firing_strength(self):
        high_x = list(self.high.keys())
        X = np.intersect1d( self.input_x, np.linspace(high_x[0], high_x[-1], int((high_x[-1] - high_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        integrand1 = lambda x: min(self.high_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value
        
        result1, error1 = integrate.quad(integrand1, X.min(), X.max())
        result2, error2 = integrate.quad(integrand2, X.min(), X.max())

        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2
        
        
        
        
    def calculate_mf(self,value):
        return [self.low_mf(value),self.normal_mf(value),self.high_mf(value)]
    
    
    def calculate_term_firing_strength(self):
        if self.input_mf is None:
            return None
        
        return {"low": self.calculate_low_firing_strength(), "normal":self.calculate_normal_firing_strength(), "high": self.calculate_high_firing_strength()}
    
    
class Age:
    universe = np.round(np.arange(0,130.1,0.1),1)
    pediatric = {0:1, 10:1, 18:0}
    young_adult = {15:0, 25:1, 35:0}
    middle_aged = {30:0,45:1,60:0}
    old = {50:0,60:1,130:1}


    def get_pdf_value(self,x):
        if self.input_mf is None:
            return 0
        if x <= self.input_x.min() or x >= self.input_x.max():
            return 0
                
        return self.input_mf[np.abs(self.input_x - x).argmin()]
            
    def set_input_interval(self,interval):
        np_interval = np.array(interval)
        mu = np_interval.mean()
        sigma = 2
        self.input_x = np.linspace(interval[0], interval[1], int((interval[1] - interval[0]) / 0.1) + 1)
        
        pdf = np.exp(-0.5 * ((self.input_x - mu) / sigma) ** 2)

        # Scale the PDF
        pdf /= pdf.max()
        self.input_mf = pdf

    def plot(self):

        #Plot pediatric
        x = np.array(list(self.pediatric.keys()))
        y = np.array(list(self.pediatric.values()))
        plt.plot(x, y, label='Pediatric', color='black')
        
        #Plot young adult
        x = np.array(list(self.young_adult.keys()))
        y = np.array(list(self.young_adult.values()))  
        plt.plot(x, y, label='Young Adult', color='black')
        
        #Plot middle_aged
        x = np.array(list(self.middle_aged.keys()))
        y = np.array(list(self.middle_aged.values()))
        
        plt.plot(x, y, label='Adult', color='black')
        
        #Plot High
        x = np.array(list(self.old.keys()))
        y = np.array(list(self.old.values()))
        
        plt.plot(x, y, label='Old', color='black')

        #Plot input
        plt.plot(self.input_x, self.input_mf, linestyle='--', color='red')

        plt.grid(True)
        
        plt.xlabel('Age')
        plt.ylabel('μ(x)')
        
        #show
        plt.show()


    def pediatric_mf(self, value):
        x = list(self.pediatric.keys())
        
        if value < x[1]:
            return 1
        
        if value > x[2]:
            return 0
        
        return (x[2]-value)/(x[2]-x[1])
    
    def young_adult_mf(self, value):
        x = list(self.young_adult.keys())

        if value < x[0] or value > x[2]:
            return 0

        if value == x[1]:
            return 1
        
        if value < x[1]:
            return (value - x[0]) / (x[1] - x[0])
        
        return (x[2] - value) / (x[2] - x[1])
        
        
    def middle_aged_mf(self, value):
        x = list(self.middle_aged.keys())

        if value < x[0] or value > x[2]:
            return 0

        if value == x[1]:
            return 1
        
        if value < x[1]:
            return (value - x[0]) / (x[1] - x[0])
        
        return (x[2] - value) / (x[2] - x[1])
    
    def old_mf(self, value):
        x = list(self.middle_aged.keys())

        if value < x[0] or value > x[2]:
            return 0

        if value > x[1]:
            return 1
        
        return (value - x[0]) / (x[1] - x[0])
    
    def calculate_pediatric_mf_firing_strength(self):
        pediatric_x = list(self.pediatric.keys())
        X = np.intersect1d( self.input_x, np.linspace(pediatric_x[0], pediatric_x[2], int((pediatric_x[2] - pediatric_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        integrand1 = lambda x: min(self.pediatric_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value
        
        result1 = integrate.quad(integrand1, X.min(), X.max())
        result2= integrate.quad(integrand2, X.min(), X.max())
        
        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2
 
    def calculate_young_adult_mf_firing_strength(self):
        young_adult_x = list(self.young_adult.keys())
        X = np.intersect1d( self.input_x, np.linspace( young_adult_x[0],  young_adult_x[-1], int(( young_adult_x[-1] -  young_adult_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0

        
        integrand1 = lambda x: min(self.young_adult_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value

        result1, error1 = integrate.quad(integrand1, X.min(), X.max())
        result2, error1 = integrate.quad(integrand2, X.min(), X.max())

        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2

        
        
    def calculate_middle_aged_mf_firing_strength(self):
        middle_aged_x = list(self.middle_aged.keys())
        X = np.intersect1d( self.input_x, np.linspace(middle_aged_x[0], middle_aged_x[-1], int((middle_aged_x[-1] - middle_aged_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        integrand1 = lambda x: min(self.middle_aged_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value
    
        
        result1, error1 = integrate.quad(integrand1, X.min(), X.max())
        result2, error2 = integrate.quad(integrand2, X.min(), X.max())

        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2
        
    def calculate_old_mf_firing_strength(self):
        old_x = list(self.old.keys())
        X = np.intersect1d( self.input_x, np.linspace(old_x[0], old_x[-1], int((old_x[-1] - old_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        integrand1 = lambda x: min(self.old_mf(x), self.get_pdf_value(x))
        integrand2 = self.get_pdf_value
    
        
        result1, error1 = integrate.quad(integrand1, X.min(), X.max())
        result2, error2 = integrate.quad(integrand2, X.min(), X.max())

        if result1 == 0 or result2 == 0:
            return 0
        
        return result1/result2
    
    def calculate_term_firing_strength(self):
        if self.input_mf is None:
            return None
        
        return {"pediatric":self.calculate_pediatric_mf_firing_strength(), "young_adult": self.calculate_young_adult_mf_firing_strength(),"middle_aged": self.calculate_middle_aged_mf_firing_strength(), "old": self.calculate_old_mf_firing_strength()}
        


