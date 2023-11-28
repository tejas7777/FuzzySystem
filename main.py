from case1_index import SingletonFuzzySet
from case2_index import NonSingletonFuzzySet

def call_singleton(temperature,age,headache):
    singleton_instance = SingletonFuzzySet(temperature=temperature,age=age,headache=headache)
    #singleton_instance.get_input_plots()
    singleton_instance.calculate_firing_strengths()
    singleton_instance.process_ruleset(tnorm='hamacher')
    #singleton_instance.plot_fuzzified_output()
    print("singleton_final_output:",singleton_instance.defuzzyfy(defuzzifier='centroid'))

def call_nonsingleton(temperature,age,headache):
    non_single_ton_instance = NonSingletonFuzzySet(temperature=temperature,age=age,headache=headache)
    #non_single_ton_instance.get_input_plots()
    non_single_ton_instance.calculate_firing_strengths()
    non_single_ton_instance.process_ruleset(tnorm='hamacher')
    #non_single_ton_instance.plot_fuzzified_output()
    print("nonsingleton_final_output:",non_single_ton_instance.defuzzyfy(defuzzifier='centroid'))



if __name__ == '__main__':
    inputs_to_test = [
        {
            "temperature":[35,36],"age":[70,80],"headache":[5,6],
        },
        {
            "temperature":[31,32],"age":[20,25],"headache":[0,1],
        },
        {
            "temperature":[38,39],"age":[70,80],"headache":[0,1],
        },
        {
            "temperature":[35,36],"age":[20,25],"headache":[9,10],
        }
    ]

    for input in inputs_to_test:
        call_singleton(sum(input["temperature"])/2,sum(input["age"])/2,sum(input["headache"])/2)
        call_nonsingleton(input["temperature"],input["age"],input["headache"])
        print("-----------NEXT___INPUT-----------------")



