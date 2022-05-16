import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import os

parent_dir = "Gaussian"

df = pd.read_excel('ao8b00576_si_001.xlsx', engine='openpyxl')
print(df.shape)
print(df.columns)
df.head()

df_test = df.iloc[:2]

calc = []
for row in df_test.iloc[:].itertuples(index=False):
  cas_no = row[4]

  path = os.path.join(parent_dir, str(cas_no)+'/')

  g_data = np.loadtxt(path + 'free_e.txt', dtype=str)

  Li_M_G = float(g_data[1][-1])
  red_Li_M_G = float(g_data[2][-1])
  bond_dG = Li_M_G - (-7.433944) - float(g_data[0][-1]) # Li+ G = -7.433944
  red_dG = red_Li_M_G - Li_M_G
  Vred_vLi = (0-red_dG) * 27.2114 - 1.4
  calc.append([Li_M_G, red_Li_M_G, bond_dG, Vred_vLi])

col_name=['Etot(Li-Mol+)\nHartree', 'Etot(Li-Mol0)\nHartree', 'association energy\nHartree', 'Li-Mol Vred\nV ( vs Li/Li+)']
df_test[col_name] = pd.DataFrame(calc, index=df_test.index)

df_test.to_csv(parent_dir + '/result_test.csv', index=False)