import random
import pandas as pd
import numpy as np


# Randomly generates simple datasets

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
            for determining when a call calculation should be made. 
                
            The function checks for the greatest value between the four bases. Conditions 
            are set for each column and will add the base with the highest "color" reading 
            to the designated column. 
                
            N is set inplace if the max value between the bases is 0 as that indicates an unclear base call. 
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

    def write_to_csv(self, name = 'Randomly_Generated_Data'):
        ''' Writes the randomly generated data to a CSV file.
        Parameters: 
            Name: Only the name of the file. File extension to be added automatically.
        Returns:
            A csv file. 
        '''

        df = self.df_ref
        return df.to_csv(name+'.csv', index = False)


    def random_failed_calls(self, perc_error = .2, N = False, perc_n_replacement = 0.02):
        ''' Will generate random 0s in rows to simulate failed base calls. Defaults: .2, False
            Parameters:
                perc: the fraction of error you would like to have in the file
                n: determines whether or not failed base calls (values set to 0) are in the dataset. 
            Returns: Randomly generated dataframe with errors
        '''

        if perc_error <= 1 and perc_error >= 0:
            df = self.df_ref
            refs = list(df.filter(like = 'ref').columns.values)
            A = list(df.filter(like = 'A').columns.values)
            T = list(df.filter(like= 'T').columns.values)
            for ref in refs:
                new_bases = []
                sample_ref = df[ref].sample(frac = perc_error)
                for i in range(len(df.loc[sample_ref.index])):
                    new_bases.append(random.choice(['A', 'C', 'G', 'T']))
                df.loc[sample_ref.index, ref] = new_bases
            if N == True:
                if perc_n_replacement <= 1 and perc_n_replacement >= 0:
                    for a, t in zip(A, T):
                        ref_start = a
                        ref_end = t
                        base_range = list(df.loc[:, ref_start:ref_end].columns.values)
                        sample = df[base_range].sample(frac = (perc_n_replacement))
                        df.loc[sample.index, sample.columns.values] = 0
            return df
        else:
            raise ValueError(f'Not a valid fraction value. Please put in a value in range 0-1')

      

