from pandas.core import base
from BaseCall_Chromatography import BaseCalls
from random_data_gen import RandomGen
import pandas as pd
import numpy as np

df_1 = RandomGen()
df_1.write_to_csv('Random_Gen_1')
df_2 = df_1.random_failed_calls(N = True)
df_2.to_csv('Random_Gen_2.csv', index=False)


data_1 = pd.read_csv('Random_Gen_1.csv')
data_1_calls = BaseCalls(data_1)
base_calls_1 = data_1_calls.base_call()
base_call_results, N_Counts = data_1_calls.base_call_error()
method_call_accuracy, method_call_error, mean_error = data_1_calls.method_call_error()
base_calls_1.to_csv('Standard_Data_Simu.csv')
print(f'{1} + Error Simulation Base Call Error: \n A {base_call_results[0]}\n C {base_call_results[1]}\n') 
print(f' G: {base_call_results[2]}\n T: {base_call_results[3]}\n N: Counts: {N_Counts}')
print(f'{2} + Overall Method Call Accuracy: {method_call_accuracy}\n Method Error: {method_call_error}\n Method Call Mean Error: {mean_error}')

data_2 = pd.read_csv('Random_Gen_2.csv')
data_2_calls = BaseCalls(data_2)
base_calls_2 = data_2_calls.base_call()
base_calls_2.to_csv('Error_Data_Simu.csv')
base_call_results_2, N_Counts_2 = data_2_calls.base_call_error()
method_call_accuracy_2, method_call_error_2, mean_error_2 = data_2_calls.method_call_error()
print(f'{3} + Error Simulation Base Call Error: \n A {base_call_results_2[0]}\n C {base_call_results_2[1]}\n') 
print(f' G: {base_call_results_2[2]}\n T: {base_call_results_2[3]}\n N: Counts: {N_Counts_2}')
print(f'{4} + Overall Method Call Accuracy: {method_call_accuracy_2}\n Method Error: {method_call_error_2}\n Method Call Mean Error: {mean_error_2}')
