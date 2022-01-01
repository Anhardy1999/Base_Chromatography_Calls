# Base Call Algorithms

## random_data_gen: 
Randomly generates a dataset. Simulates a base call algorithm.
Has the option of generating random errors including:
- Random misscalls: Simulates having an accurate reference, but the algorithm intensity chooses the wrong base.
- Random failed calls: Simulates an algorithm being unable

##  BaseCall_Chromatography: 
Makes basecalls based on the structure of the randomly generated dataset.
- Processes the df by making sure all values are converted to floats
- Calls bases and marks any call that doesn't have values (a row of 0s) as N symbolizing a failed called from the chromatography algorithm.
- Calculates the overall error of the algorithm. 

## Example Datasets
[Randomly Generated with no errors](Base_Calls/Randomly_Generated_Data.csv)

[Randomly Generated with Errors](Base_Calls/Sample_Generated_Data_w_Errors.csv)
