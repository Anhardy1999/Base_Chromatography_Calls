import pandas as pd
import numpy as np


def random_gen(calls = 4, rows = 1000):
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
  values = np.random.rand(rows,calls*4)

  names = []
  i = 1
  for i in range(1,calls+1):
      for base in bases:
          col_name = base + '_' + str(i)
          names.append(col_name)
      i+=1

  df = pd.DataFrame(values, columns=names)
  
  return df

def ref_call(df):
  ''' Makes the ref calls based on the data in the provided dataframe to compare for errors.
            
            This function takes the range of base columns "A" and "T"  and uses those
            for determining when a call calculation should be made. 
            
            The function checks for the greatest value between the four bases. Conditions 
            are set for each column and will add the base with the highest "color" reading 
            to the designated column. 
            
            Uses the same idea as base_call except it inserts a reference column if needed.
  '''

  bases = ['A', 'C', 'G', 'T']
        
  A = list(df.filter(like = 'A').columns.values)
  T = list(df.filter(like= 'T').columns.values)
  i = 1
  for a, t in zip(A, T):
    ref_start = a
    ref_end = t
    base_range = list(df.loc[:, ref_start:ref_end].columns.values)
    conditions = [
      (df[base_range[0:]].idxmax(axis = 1) == base_range[0]),
      (df[base_range[0:]].idxmax(axis = 1) == base_range[1]),
      (df[base_range[0:]].idxmax(axis = 1) == base_range[2]),
      (df[base_range[0:]].idxmax(axis = 1) == base_range[3]),
      ]
    ref_name = 'ref_' + str(i)
    i += 1
    data = np.select(conditions, bases)
    if ref_name in df.columns:
      df = df.drop(ref_name, axis = 1)
    loc = df.columns.get_loc(a)
    df.insert(loc, ref_name, data)
        
   return df
