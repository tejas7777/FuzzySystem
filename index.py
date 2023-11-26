from mpmath import iv
import numpy as np
from nonsingleton import LinguisticVariables

    
class IntervalFuzzySet:
    temperature_universe = np.round(np.arange(35,42.1,0.1),1)
    headache_universe = np.arange(0,11,1)
    age_universe = np.arange(0,131,1)
    
    Temperature = LinguisticVariables.Temperature()
    
    
    def __init__(self, temperature:list, headache:list,age:list):
        self.temperature = temperature
        self.headache = headache
        self.age = age
        
        
        
        
if __name__ == '__main__':
    TemperatureVariable = LinguisticVariables.Temperature()
    TemperatureVariable.set_input_interval([35,37
                                            ])
    TemperatureVariable.plot()
    print(TemperatureVariable.calculate_term_firing_strength())
        
        
        
        
        