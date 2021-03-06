import random
import pandas as pd
import numpy as np


class RandomGen():
        ''' Creates a simple dataframe that contains random floats between 0 and 1 for bases ACGT.
        For basic base calling algorithms.
        
        Parameters:
            - calls: The number of ACGT columns needed. For instance, supplying 4 will provide 
            4 A, 4 C, 4 G, and 4 T columns. This will amount to the number of base calls you would
            like to make. By default 4 calls will be made
            
            - rows: How much data you would like. By default there are 1000 rows.  
            
            returns a dataframe
            ''' 
        
    def __init__(self, calls = 4, rows = 1000):
        self.calls = calls
        self.rows = rows
        self.df = self.__random_gen()
        self.df_ref = self.__ref_call()

    def __random_gen(self):
        ''' Creates a simple dataframe that contains random floats between 0 and 1 for bases ACGT.
        For basic base calling algorithms.
        
        Parameters:
            - calls: The number of ACGT columns needed. For instance, supplying 4 will provide 
            4 A, 4 C, 4 G, and 4 T columns. This will amount to the number of base calls you would
            like to make. By default 4 calls will be made
            
            - rows: How much data you would like. By default there are 1000 rows.  
            
            returns a dataframe
            ''' 
        bases = ['A', 'C', 'G', 'T']
        
        values = np.random.rand(self.rows,self.calls*4)

        names = []
        i = 1
        for i in range(1,self.calls+1):
            for base in bases:
                col_name = base + '_' + str(i)
                names.append(col_name)
            i+=1

        df = pd.DataFrame(values, columns=names)

        return df

    def __ref_call(self):
        ''' Makes the ref calls based on the data in the provided dataframe to compare for errors.
                
            This function takes the range of base columns "A" and "T"  and uses those
            for determining the ref column.
                
            The function checks for the greatest value between the four bases. Conditions 
            are set for each column and will add the base with the highest "color" reading 
            to the designated column. 
         '''

        bases = ['N', 'A', 'C', 'G', 'T']
            
        df = self.df

        A = list(df.filter(like = 'A').columns.values)
        T = list(df.filter(like= 'T').columns.values)
        i = 1
        for a, t in zip(A, T):
            ref_start = a
            ref_end = t
            base_range = list(df.loc[:, ref_start:ref_end].columns.values)
            conditions = [
                (df[base_range[0:]].max(axis = 1) == 0),
                (df[base_range[0:]].idxmax(axis = 1) == base_range[0]),
                (df[base_range[0:]].idxmax(axis = 1) == base_range[1]),
                (df[base_range[0:]].idxmax(axis = 1) == base_range[2]),
                (df[base_range[0:]].idxmax(axis = 1) == base_range[3]),
            ]
            ref_name = 'ref_' + str(i)
            i += 1
            data = np.select(conditions, bases)
            if ref_name in self.df.columns:
                df = df.drop(ref_name, axis = 1)
            loc = df.columns.get_loc(a)
            df.insert(loc, ref_name, data)
        
        return df

    def write_to_csv(self, name = 'Randomly_Generated_Data.csv'):
        ''' Writes the randomly generated data to a CSV file.
        Parameters:
        Name: The name of the file. Extension must be included. 
        '''

        df = self.df_ref
        return df.to_csv(name, index = False)


    def random_failed_calls(self, min_perc_error = 0, max_perc_error = 0.2, N = False, min_perc_n = 0, max_perc_n = 0.2):
        ''' Will generate random error within the dataset. Provided a range of values, this function will generate varying
        error rates within each call
            Parameters:
                min_perc_error: The minimum percentage of error that can occur.
                max_perc_error: The maximum percentage of error that can occur.
                N: determines whether or not failed base calls (values set to 0) are in the dataset. 
                min_perc_error: The minimum percentage of N values that can occur in the dataset.
                max_perc_error: The maximum percentage of N values that can occur in the dataset. 
            Returns: Randomly generated dataframe with errors
        '''

        if max_perc_error <= 1 and min_perc_error >= 0:
            df = self.df_ref
            refs = list(df.filter(like = 'ref').columns.values)
            A = list(df.filter(like = 'A').columns.values)
            T = list(df.filter(like= 'T').columns.values)
            for ref in refs:
                new_bases = []
                error_rate = random.uniform(min_perc_error,max_perc_error)
                sample_ref = df[ref].sample(frac = error_rate)
                for i in range(len(df.loc[sample_ref.index])):
                    new_bases.append(random.choice(['A', 'C', 'G', 'T']))
                df.loc[sample_ref.index, ref] = new_bases
            if N == True:
                if perc_n_replacement <= 1 and perc_n_replacement >= 0:
                    for a, t in zip(A, T):
                        error_n = random.uniform(min_perc_n,max_perc_n)
                        ref_start = a
                        ref_end = t
                        base_range = list(df.loc[:, ref_start:ref_end].columns.values)
                        sample = df[base_range].sample(frac = error_n)
                        df.loc[sample.index, sample.columns.values] = 0
            return df
        else:
            raise ValueError(f'Not a valid fraction value. Please put in a value in range 0-1')

      

