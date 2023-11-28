from mpmath import iv
import numpy as np
from singleton import LinguisticVariables
from tnorm import Tnorm
import pandas as pd
from consequent import Urgency
from tconorm import Tconorm
import matplotlib.pyplot as plt
from defuzzifier import Defuzzifier

    
class SingletonFuzzySet:
    Temperature = LinguisticVariables.Temperature()
    Age = LinguisticVariables.Age()
    HeadAche = LinguisticVariables.HeadAche()
    firing_strengths = None
    Tnorm = Tnorm()
    Urgency = Urgency()
    Tconorm = Tconorm()
    final_set = None
    Defuzzifier = Defuzzifier()
    
    
    def __init__(self, temperature:list, headache:list,age:list):
        self.Temperature.set_input(temperature)
        self.Age.set_input(age)
        self.HeadAche.set_input(headache)

    def get_input_plots(self):
        self.Temperature.plot()
        self.Age.plot()
        self.HeadAche.plot()

    def calculate_firing_strengths(self):
        self.firing_strengths = {
            "temperature": self.Temperature.calculate_term_firing_strength(),
            "headache": self.HeadAche.calculate_term_firing_strength(),
            "age": self.Age.calculate_term_firing_strength()
        }


    def process_ruleset(self, tnorm = 'min'):
        df = pd.read_csv("rules.csv")
        
        #Iterate our rule sets
        rule_tnorm_outputs = []


        for i,row in df.iterrows():
            tnorm_input = []
            row = row.fillna('NaN')

            if row["temperature"]  != 'NaN' and self.firing_strengths["temperature"] is not None:
                #Get the rule value for temperature for eg. temperature is low
                temperature_value:str = row["temperature"]
                #Get the firing strength for temperature
                temperature_firing_strength:dict = self.firing_strengths["temperature"]
                #Check if rule value has an or condition represented by ^
                if '^' in temperature_value:
                    #If or condition, eg. LOW ^ MODERATE, we take max(LOW,MODERATE)
                    temperature_value = temperature_value.split('^')
                    firing_strengths = []
                    for val in temperature_value:
                        firing_strengths.append(temperature_firing_strength.get(val))

                    tnorm_input.append(max(firing_strengths))
                else:
                    #Since no OR condition, continue as normal
                    tnorm_input.append(temperature_firing_strength.get(temperature_value))
            if row["headache"]  != 'NaN' and self.firing_strengths["headache"] is not None:
                #Same as above
                headache_value:str = row["headache"]
                headache_firing_strength:dict = self.firing_strengths["headache"]
                if '^' in headache_value:
                    headache_value = headache_value.split('^')
                    firing_strengths = []
                    for val in headache_value:
                        firing_strengths.append(headache_firing_strength.get(val))
                    tnorm_input.append(max(firing_strengths))
                else:
                    tnorm_input.append(headache_firing_strength.get(headache_value))
            if row["age"]  != 'NaN' and self.firing_strengths["age"] is not None:
                age_value:str = row["age"]
                age_firing_strength:dict = self.firing_strengths["age"]
                if '^' in age_value:
                    age_value = age_value.split('^')
                    firing_strengths = []
                    for val in age_value:
                        firing_strengths.append(age_firing_strength.get(val))
                    tnorm_input.append(max(firing_strengths))
                else:
                    tnorm_input.append(age_firing_strength.get(age_value))


            final_firing = self.Tnorm.apply(input=tnorm_input,tnorm=tnorm)

            rule_tnorm_outputs.append((final_firing,row['urgency']))



        fuzzified_area = []
        for row in rule_tnorm_outputs:
            fuzzified_area.append(self.Urgency.generate_output_set(row[0],row[1]))


        final_set = self.Tconorm.apply(input=fuzzified_area, tconorm='max')
        self.final_set = dict(sorted(final_set.items()))



    def plot_fuzzified_output(self):
        if self.final_set is None:
            return
        
        x = np.array(list(self.final_set.keys()))
        y = np.array(list(self.final_set.values()))
       
        plt.plot(x, y, label='Result', color='black')
        plt.show()

    def defuzzyfy(self,defuzzifier):
        return self.Defuzzifier.apply(self.final_set,defuzzifier=defuzzifier)

        


        
        
# if __name__ == '__main__':
#     SingletonFuzzySet = SingletonFuzzySet(temperature=35.5,age=75.5,headache=5.5)
#     SingletonFuzzySet.get_input_plots()
#     SingletonFuzzySet.calculate_firing_strengths()
#     #print(NonSingletonFuzzySet.firing_strengths)
#     SingletonFuzzySet.process_ruleset(tnorm='hamacher')
#     SingletonFuzzySet.plot_fuzzified_output()
#     print(SingletonFuzzySet.defuzzyfy(defuzzifier='centroid'))
#     print(SingletonFuzzySet.final_set)

        
        
        
        
        