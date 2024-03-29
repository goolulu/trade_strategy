import pandas as pd
import numpy as np

dates = pd.date_range('2023-01-01', periods=6)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))

print(df)
