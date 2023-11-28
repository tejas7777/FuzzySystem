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
        plt.plot(self.input_x, self.input_mf, linestyle='--', color='red', label='I')


        plt.grid(True)
        plt.legend()

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
         
        x_values = X
        mu_A_values = np.array([self.low_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
 
    def calculate_normal_firing_strength(self):
        normal_x = list(self.normal.keys())
        X = np.intersect1d( self.input_x, np.linspace(normal_x[0], normal_x[-1], int((normal_x[-1] - normal_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        x_values = X
        mu_A_values = np.array([self.normal_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0
        
        return integral_sSH/integral_mu_I

        
        
    def calculate_high_firing_strength(self):
        high_x = list(self.high.keys())
        X = np.intersect1d( self.input_x, np.linspace(high_x[0], high_x[-1], int((high_x[-1] - high_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        x_values = X
        mu_A_values = np.array([self.high_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
        
        
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
    adult = {30:0,45:1,60:0}
    old = {50:0,60:1,130:1}
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
        plt.plot(x, y, label='Pediatric')
        
        #Plot young adult
        x = np.array(list(self.young_adult.keys()))
        y = np.array(list(self.young_adult.values()))  
        plt.plot(x, y, label='Young Adult')
        
        #Plot adult
        x = np.array(list(self.adult.keys()))
        y = np.array(list(self.adult.values()))
        
        plt.plot(x, y, label='Adult')
        
        #Plot High
        x = np.array(list(self.old.keys()))
        y = np.array(list(self.old.values()))
        
        plt.plot(x, y, label='Old')

        #Plot input
        plt.plot(self.input_x, self.input_mf, linestyle='--', color='red', label='I')

        plt.grid(True)
        plt.legend()
        
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
        
        
    def adult_mf(self, value):
        x = list(self.adult.keys())

        if value < x[0] or value > x[2]:
            return 0

        if value == x[1]:
            return 1
        
        if value < x[1]:
            return (value - x[0]) / (x[1] - x[0])
        
        return (x[2] - value) / (x[2] - x[1])
    
    def old_mf(self, value):
        x = list(self.old.keys())

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
        
        x_values = X
        mu_A_values = np.array([self.pediatric_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
 
    def calculate_young_adult_mf_firing_strength(self):
        young_adult_x = list(self.young_adult.keys())
        X = np.intersect1d( self.input_x, np.linspace( young_adult_x[0],  young_adult_x[-1], int(( young_adult_x[-1] -  young_adult_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0

        
        x_values = X
        mu_A_values = np.array([self.young_adult_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I

        
        
    def calculate_adult_mf_firing_strength(self):
        adult_x = list(self.adult.keys())
        X = np.intersect1d( self.input_x, np.linspace(adult_x[0], adult_x[-1], int((adult_x[-1] - adult_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        x_values = X
        mu_A_values = np.array([self.adult_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
        
    def calculate_old_mf_firing_strength(self):
        old_x = list(self.old.keys())
        X = np.intersect1d( self.input_x, np.linspace(old_x[0], old_x[-1], int((old_x[-1] - old_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        print(X)
        
        x_values = X
        mu_A_values = np.array([self.old_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        print(integral_sSH,integral_sSH)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
    
    def calculate_term_firing_strength(self):
        if self.input_mf is None:
            return None
        
        return {"pediatric":self.calculate_pediatric_mf_firing_strength(), "young_adult": self.calculate_young_adult_mf_firing_strength(),"adult": self.calculate_adult_mf_firing_strength(), "old": self.calculate_old_mf_firing_strength()}
        
    
class HeadAche:
    low = {0:1,3:1,6:0}
    moderate = {2:0,5:1,8:0}
    high = {4:0,7:1,10:1}
    input_mf = None
    input_x = None
    
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
        plt.plot(self.input_x, self.input_mf, linestyle='--', color='red', label = 'I')

        plt.xlabel('Headache')
        plt.ylabel('μ(x)')
        

        plt.grid(True)
        plt.legend()
        
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
        
        if(value == x[1]):
            return 1
        
        if value < x[1]:
            return (value - x[0])/(x[1] - x[0])

        return (x[2] - value) / (x[2] - x[1])
        
        
    
    def high_mf(self,value):
        x = list(self.high.keys())
        if(value < x[0]):
            return 0
        
        if(value > x[1]):
            return 1
        
        return (value - x[0])/(x[1] - x[0])
    

    def get_pdf_value(self,x):
        if self.input_mf is None:
            return 0
        if x <= self.input_x.min() or x >= self.input_x.max():
            return 0
                
        return self.input_mf[np.abs(self.input_x - x).argmin()]
            
    def set_input_interval(self,interval):
        np_interval = np.array(interval)
        mu = np_interval.mean()
        sigma = 0.25
        self.input_x = np.linspace(interval[0], interval[1], int((interval[1] - interval[0]) / 0.1) + 1)
        
        pdf = np.exp(-0.5 * ((self.input_x - mu) / sigma) ** 2)

        # Scale the PDF
        pdf /= pdf.max()
        self.input_mf = pdf

    def calculate_low_firing_strength(self):
        low_x = list(self.low.keys())
        X = np.intersect1d( self.input_x, np.linspace(low_x[0], low_x[2], int((low_x[2] - low_x[0]) / 0.1) + 1))
         
        x_values = X
        mu_A_values = np.array([self.low_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
 
    def calculate_moderate_firing_strength(self):
        moderate_x = list(self.moderate.keys())
        X = np.intersect1d( self.input_x, np.linspace(moderate_x[0], moderate_x[-1], int((moderate_x[-1] - moderate_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        x_values = X
        mu_A_values = np.array([self.moderate_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0
        
        return integral_sSH/integral_mu_I

        
        
    def calculate_high_firing_strength(self):
        high_x = list(self.high.keys())
        X = np.intersect1d( self.input_x, np.linspace(high_x[0], high_x[-1], int((high_x[-1] - high_x[0]) / 0.1) + 1))
        
        if len(X) == 0:
            return 0
        
        x_values = X
        mu_A_values = np.array([self.high_mf(x) for x in x_values])
        mu_I_values = np.array([self.get_pdf_value(x) for x in x_values])

        # Calculate the integrals using the trapezoidal rule
        integral_sSH = np.trapz(np.minimum(mu_A_values, mu_I_values), x=x_values)
        integral_mu_I = np.trapz(mu_I_values, x=x_values)

        if integral_sSH == 0 or integral_mu_I == 0:
            return 0

        return integral_sSH/integral_mu_I
        
        
    def calculate_mf(self,value):
        return [self.low_mf(value),self.normal_mf(value),self.high_mf(value)]
    
    
    def calculate_term_firing_strength(self):
        if self.input_mf is None:
            return None
        
        return {"low": self.calculate_low_firing_strength(), "moderate":self.calculate_moderate_firing_strength(), "high": self.calculate_high_firing_strength()}
