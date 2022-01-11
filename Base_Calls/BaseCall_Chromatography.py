import pandas as pd
import numpy as np


class BaseCalls():

    def __init__(self, df):
        ''' Makes base calls on the provided dataframe. Adds a call column at the end of each set of bases (ACGT)
        Function is based on the randomly generated dataset where bases start with A and end with T. '''
        self.df = df

    def processing_dfs(self):
        ''' Changes necessary base call values to floats instead of strings 
        Only necessary if there are references sequences that have string values
        Otherwise, data should already have all floats. '''

        ref_seqs = list(self.df.filter(like='ref').columns.values)  
        cols = self.df.columns.drop(ref_seqs)
        self.df[cols] = self.df[cols].apply(pd.to_numeric, errors='coerce')
        


    def base_call(self):
        ''' Makes the base call based on the data in the provided dataframe.
            
            This function takes the range of base columns "A" and "T"  and uses those
            for determining when a call calculation should be made. 
            
            The function checks for the greatest value between the four bases. Conditions 
            are set for each column and will add the base with the value.
            
            N is set inplace if the max value between the bases is 0 as that indicates an unclear base call. 
        '''
        df = self.df

        bases = ['N', 'A', 'C', 'G', 'T']
        
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
            call_name = 'call_' + str(i)
            i += 1
            data = np.select(conditions, bases)
            if call_name in df.columns:
                df = df.drop(call_name, axis = 1)
            loc = df.columns.get_loc(t)+1
            df.insert(loc, call_name, data)
        
        return df

    def method_call_error(self):
        ''' Calculates the overall error of each call if there is a reference column in the dataframe '''
        df = self.df
        accuracy = []
        error = []
        ref_seqs = list(df.filter(like='ref').columns.values)
        calls = list(df.filter(like='call').columns.values)
        for ref_seq, call in zip(ref_seqs, calls):
            accuracy.append(sum(df[call] == df[ref_seq])/len(df[ref_seq]))
        for value in accuracy:
            error.append((1 - value)*100)
            
        ''' Determining the mean error between the two calls of each method '''
        mean_error = (abs(sum(error)))/len(error)
        return accuracy, error, mean_error

    def base_call_error(self): 
        ''' Calculates the error for each base in the method.
            Only used if there is a reference columns to compare to.
        
            Returned Data:
                Results come back as a list of list with errors.
                Bases are returned as errors.
                N's (where the calls were unclear and could be any base - data for each 
                base in provided csv is 0) are tallied. 
        '''

        df = self.df   
        bases = ['A', 'C', 'G', 'T', 'N']
        base_call_errors = []
        N_tally = []

        ref_seqs = list(df.filter(like='ref').columns.values)
        calls = list(df.filter(like='call').columns.values)
        for ref_seq, call in zip(ref_seqs, calls): 
            for base in bases:
                ref = len(df[df[ref_seq] == base])
                base_idx = list(np.where(df[ref_seq] == base)[0])
                correct_call = 0
                for idx in base_idx:
                    if df[ref_seq].loc[idx] == df[call].loc[idx]:
                        correct_call += 1
                if base == 'A':
                    A_error = abs((correct_call - ref)/ref)*100
                elif base == 'C':
                    C_error = abs((correct_call - ref)/ref)*100
                elif base == 'G':
                    G_error = abs((correct_call - ref)/ref)*100
                elif base == 'T':
                    T_error = abs((correct_call - ref)/ref)*100
                else:
                    N_counts = len(df[df[call] == base])
                    
            base_call_errors.extend([[A_error, C_error, G_error, T_error]])
            N_tally.append(N_counts)

        return base_call_errors, N_tally

    def return_heatmap(self, ref = 'ref_1', call = 'call_1', title = 'Reference Call Heatmap'):
        ''' Returns a heatmap of incorrect calls for a specified reference. By default ref and call are
        set to the first appearances. A default title "Reference Call Heatmap" is also set.
        Parameters:
        ref: the reference sequence you would like to use
        call: the call associated with the reference sequence
        title: what you would like to call the sequence'''
        df = self.df
        matrix = confusion_matrix(df[ref], df[call])
        fig, ax = plt.subplots(figsize=(10,10))
        ax = sns.heatmap(matrix, annot = True, cmap = 'BuPu', fmt = 'g')
        ax.set_title(title)
        names = df.groupby([call]).apply(lambda x: x[ref].value_counts().index[0])
        names = ['A', 'C', 'G', 'N', 'T']
        ax.xaxis.set_ticklabels(names)
        ax.yaxis.set_ticklabels(names)
        fig.savefig(title+'.png')
