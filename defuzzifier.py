class Defuzzifier:
    
    def apply(self,input,defuzzifier='centroid'):

        if defuzzifier == 'centroid':
            return self.centroid(input)
        
        if defuzzifier == 'bisector':
            return self.bisector(input)
        
        if defuzzifier == 'height':
            return self.height(input)

    
    def centroid(self, final_set: dict):
        if final_set is None:
            return
        
        x = list(final_set.keys())
        y = list(final_set.values())

        nominator_sum = 0
        denominator_sum = 0

        for i in range(len(x)):
            nominator_sum = nominator_sum + x[i]*y[i]
            denominator_sum = denominator_sum + y[i]

        if nominator_sum == 0 or denominator_sum == 0:
            return 0

        return nominator_sum/denominator_sum
    
    def bisector(self, final_set: dict):
 
        if final_set is None:
            return
         
        # Extract x and y values
        x_values = list(final_set.keys())
        y_values = list(final_set.values())

        # Calculate the total area under the curve
        total_area = sum(y_values)

        # Initialize variables for cumulative area and bisector x-value
        cumulative_area = 0
        bisector_x = None

        # Find the bisector x-value
        for i in range(len(x_values)):
            cumulative_area += y_values[i]
            if cumulative_area >= total_area / 2:
                bisector_x = x_values[i]
                break

        return bisector_x
    
    def height(self,fuzzy_set: dict):
        if fuzzy_set is None:
            return

        x = list(fuzzy_set.keys())
        y = list(fuzzy_set.values())

        h = max(y)  # Find the maximum y value (height)

        # Find the x values corresponding to the maximum height
        x_max = [x[i] for i in range(len(y)) if y[i] == h]

        if len(x_max) == 0:
            return 0

        return sum(x_max) / len(x_max)