from mpmath import iv
import numpy as np
import matplotlib.pyplot as plt


class Tnorm:

    def apply(self, input, tnorm):
        if tnorm == 'min':
            return self.tnorm_min(input)
        if tnorm == 'algebric':
            return self.algebric(input=input)
        if tnorm == 'bounded_difference':
            return self.bounded_deference(input)
        if tnorm == 'hamacher':
            return self.hamacher(rule_strengths=input)
             
             
             

    def tnorm_min(self,input:list):
        return min(input)
    
    def algebric(self,input):
        result = 1.0
        for rule_strength in input:
            result *= rule_strength
        return result
    
    def bounded_deference(self,rule_strengths):
        fs_sum = sum(rule_strengths)

        n = 0.1 #Tuning parameter
         # Step 2: Calculate the difference term
        difference_term = n * (len(rule_strengths) - 1)

        # Step 3: Apply the bounded difference t-norm
        return min(1, max(0, fs_sum - difference_term))


    
    def hamacher(self,rule_strengths):
        lambda_param = 0.5
        numerator = 1.0
        denominator = lambda_param + (1 - lambda_param)

        for rule_strength in rule_strengths:
            numerator *= rule_strength
            denominator += rule_strength - rule_strength * numerator

        return numerator / denominator

    
