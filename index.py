from mpmath import iv
import numpy as np
from nonsingleton import LinguisticVariables
from tnorm import Tnorm
import pandas as pd

    
class NonSingletonFuzzySet:
    Temperature = LinguisticVariables.Temperature()
    Age = LinguisticVariables.Age()
    HeadAche = None
    firing_strengths = None
    Tnorm = Tnorm()
    
    
    def __init__(self, temperature:list, headache:list,age:list):
        self.Temperature.set_input_interval(temperature)
        self.Age.set_input_interval(age)

    def get_input_plots(self):
        self.Temperature.plot()
        self.Age.plot()

    def calculate_firing_strengths(self):
        self.firing_strengths = {
            "temperature": self.Temperature.calculate_term_firing_strength(),
            "headache": None,
            "age": self.Age.calculate_term_firing_strength()
        }


    def process_ruleset(self):
        df = pd.read_csv("rules.csv")
        
        #Iterate our rule sets
        rule_tnorm_outputs = []

        for i,row in df.iterrows():
            tnorm_input = []
            if row["temperature"] is not None and self.firing_strengths["temperature"] is not None:
                tnorm_input.append(self.firing_strengths["temperature"].get(row["temperature"]))
            if row["headache"] != None and self.firing_strengths["headache"] is not None:
                tnorm_input.append(self.firing_strengths["headache"].get(row["headache"]))
            if row["age"] is not None and self.firing_strengths["age"] is not None:
                tnorm_input.append(self.firing_strengths["age"].get(row['age']))

            
            final_firing = self.Tnorm.tnorm_min(input=tnorm_input)

            rule_tnorm_outputs.append(final_firing)

            print(rule_tnorm_outputs)
            
            


        
        
        
        
if __name__ == '__main__':
    NonSingletonFuzzySet = NonSingletonFuzzySet(temperature=[35,36],age=[30,40],headache=[])
    NonSingletonFuzzySet.get_input_plots()
    NonSingletonFuzzySet.calculate_firing_strengths()
    #print(NonSingletonFuzzySet.firing_strengths)
    NonSingletonFuzzySet.process_ruleset()

        
        
        
        
        