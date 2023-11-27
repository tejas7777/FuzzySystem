from mpmath import iv
import numpy as np
from nonsingleton import LinguisticVariables as NSLinguisticVariables
from tnorm import Tnorm
import pandas as pd
from consequent import Urgency
from tconorm import Tconorm
import matplotlib.pyplot as plt

    
class NonSingletonFuzzySet:
    Temperature = NSLinguisticVariables.Temperature()
    Age = NSLinguisticVariables.Age()
    HeadAche = NSLinguisticVariables.HeadAche()
    firing_strengths = None
    Tnorm = Tnorm()
    Urgency = Urgency()
    Tconorm = Tconorm()
    final_set = None
    
    
    def __init__(self, temperature:list, headache:list,age:list):
        self.Temperature.set_input_interval(temperature)
        self.Age.set_input_interval(age)
        self.HeadAche.set_input_interval(headache)

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

        print('RULES FIRINGS:\n', self.firing_strengths)

        for i,row in df.iterrows():
            tnorm_input = []
            row = row.fillna('NaN')

            if row["temperature"]  != 'NaN' and self.firing_strengths["temperature"] is not None:
                tnorm_input.append(self.firing_strengths["temperature"].get(row["temperature"]))
            if row["headache"]  != 'NaN' and self.firing_strengths["headache"] is not None:
                tnorm_input.append(self.firing_strengths["headache"].get(row["headache"]))
            if row["age"] != 'NaN' and self.firing_strengths["age"] is not None:
                tnorm_input.append(self.firing_strengths["age"].get(row['age']))


            final_firing = self.Tnorm.apply(input=tnorm_input,tnorm=tnorm)

            rule_tnorm_outputs.append((final_firing,row['urgency']))

        print(rule_tnorm_outputs)


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

    def defuzzyfy(self):
        if self.final_set is None:
            return
        
        x = list(self.final_set.keys())
        y = list(self.final_set.values())

        nominator_sum = 0
        denominator_sum = 0

        for i in range(len(x)):
            nominator_sum = nominator_sum + x[i]*y[i]
            denominator_sum = denominator_sum + y[i]

        if nominator_sum == 0 or denominator_sum == 0:
            return 0

        return nominator_sum/denominator_sum

        


        
        
if __name__ == '__main__':
    NonSingletonFuzzySet = NonSingletonFuzzySet(temperature=[35,36],age=[70,80],headache=[5,6])
    NonSingletonFuzzySet.get_input_plots()
    NonSingletonFuzzySet.calculate_firing_strengths()
    #print(NonSingletonFuzzySet.firing_strengths)
    NonSingletonFuzzySet.process_ruleset(tnorm='bounded_difference')
    NonSingletonFuzzySet.plot_fuzzified_output()
    print(NonSingletonFuzzySet.defuzzyfy())

        
        
        
        
        