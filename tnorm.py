from mpmath import iv
import numpy as np
import matplotlib.pyplot as plt


class Tnorm:

    def apply(self, input, tnorm):
        if tnorm == 'min':
            return self.tnorm_min(input)
        if tnorm == 'einstein':
            return self.einstein_t_norm(input=input)
        if tnorm == 'bounded_difference':
            return self.bounded_deference(input)
        if tnorm == 'hamacher':
            return self.hamacher(rule_strengths=input)
             
             
             

    def tnorm_min(self,input:list):
        return min(input)
    
    def einstein_t_norm(self,input):
            return np.prod(input) / (2 - np.sum(input) + np.prod(input))
    
    def bounded_deference(self,rule_strengths):
        return np.max([0, np.sum(rule_strengths) - 1])
    
    def hamacher(self,rule_strengths):
        return np.prod(rule_strengths) / (np.sum(rule_strengths) - np.prod(rule_strengths) + 1)
    
