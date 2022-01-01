# Base Call Algorithms

## random_data_gen: 
Randomly generates a dataset. Simulates a base call algorithm.
Has the option of generating random errors including:
- Random misscalls: Simulates having an accurate reference, but the algorithm intensity chooses the wrong base.
- Random failed calls: Simulates an algorithm being unable

##  BaseCall_Chromatography: 
Makes basecalls based on the structure of the randomly generated dataset.
- Processes the dataframe by making sure all values are converted to floats
- Calls bases and marks any call that doesn't have values (a row of 0s) as N symbolizing a failed called from the chromatography algorithm.
- Calculates the overall error of the algorithm. 

## Example Datasets
[Randomly Generated with no errors](Base_Calls/Example_Data/Random_Gen_1.csv)

[Randomly Generated with errors](Base_Calls/Example_Data/Random_Gen_2.csv)

### Main.py
- Sample code using both python programs creates a randomly generated file and results. Outputs a textfile with the errors and accuracies of the simulated data.

[Simulation_Results.txt](https://github.com/Anhardy1999/Base_Chromatography_Calls/files/7798248/Simulation_Results.txt)
