from mpmath import iv
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import warnings

class Tconorm:

    def apply(self, input, tconorm):
        if tconorm == 'max':
            return self.tconorm_max(input_array=input)
    
    def tconorm_max(self,input_array:list) -> dict:
        result = {}

        for input in input_array:
            for input_set in input:
                if result.get(input_set[-1]) is not None:
                    result[input_set[-1]] = max(result[input_set[-1]],input_set[0])
                else:
                    result[input_set[-1]] = input_set[0]

        return result
    

                
                
            


       
    
