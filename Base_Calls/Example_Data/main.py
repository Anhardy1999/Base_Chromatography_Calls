from BaseCall_Chromatography import BaseCalls
from random_data_gen import RandomGen
import pandas as pd
import sys


df_1 = RandomGen()
df_1.write_to_csv('Random_Gen_1')
df_2 = df_1.random_failed_calls(N = True)
df_2.to_csv('Random_Gen_2.csv', index=False)


data_1 = pd.read_csv('Random_Gen_1.csv')
data_1_calls = BaseCalls(data_1)
base_calls_1 = data_1_calls.base_call()
base_call_results, n_Counts = data_1_calls.base_call_error()
method_call_error, mean_error = data_1_calls.method_call_error()
base_calls_1.to_csv('Standard_Data_Simu.csv')

data_2 = pd.read_csv('Random_Gen_2.csv')
data_2_calls = BaseCalls(data_2)
base_calls_2 = data_2_calls.base_call()
base_calls_2.to_csv('Error_Data_Simu.csv')
base_call_results_2, n_Counts_2 = data_2_calls.base_call_error()
method_call_error_2, mean_error_2 = data_2_calls.method_call_error()


original_stdout = sys.stdout
with open('Simulation_Results.txt', 'w') as f:
    sys.stdout = f
    print(f'{1} + Standard Simulation Base Call Error: \n A: {base_call_results[0]}\n C: {base_call_results[1]}') 
    print(f' G: {base_call_results[2]}\n T: {base_call_results[3]}\n N: Counts: {n_Counts}')
    print(f'{2} + Method Call Errors: {method_call_error}\n Method Call Mean Error: {mean_error}\n')

    print(f'{3} + Error Simulation Base Call Error: \n A: {base_call_results_2[0]}\n C: {base_call_results_2[1]}') 
    print(f' G: {base_call_results_2[2]}\n T: {base_call_results_2[3]}\n N: Counts: {n_Counts_2}')
    print(f'{4} + Method Call Error: {method_call_error_2}\n Method Call Mean Error: {mean_error_2}')
    sys.stdout = original_stdout
