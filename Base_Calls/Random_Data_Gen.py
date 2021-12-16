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
  for i in range(1,5):
      for base in bases:
          col_name = base + '_' + str(i)
          names.append(col_name)
      i+=1

  df = pd.DataFrame(values, columns=names)
  
  return df

