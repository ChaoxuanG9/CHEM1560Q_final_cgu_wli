import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import os
import cirpy
import copy


df = pd.read_excel('ao8b00576_si_001.xlsx', engine='openpyxl')
print(df.shape)
print(df.columns)
df.head()

df_test = df.iloc[:2]

df_test['smiles'] = df_test['cas registry number'].apply(lambda x: cirpy.resolve(x, 'smiles'))

def create_lithiums(coords:list):
  x_acc = 0
  y_acc = 0
  z_acc = 0
  total_atoms = len(coords)
  for atom in coords:
    atom = atom.replace("   ", ",").replace(" ","")
    atom = atom.split(",")
    x_acc += float(atom[1])
    y_acc += float(atom[2])
    z_acc += float(atom[3])
  com = ["{:.4f}".format(x_acc/total_atoms), "{:.4f}".format(y_acc/total_atoms), "{:.4f}".format(z_acc/total_atoms)]

  new_coords = []
  for cord in coords[2:-1]:
    current = copy.deepcopy(cord)
    current_list = current.replace("   ", ",").replace(" ","").split(",")
    new_coords.append([current_list[0],current_list[1],current_list[2],current_list[3]])

  max_coords = []
  max_x = -999
  max_y = -999
  max_z = -999
  for element in new_coords:
    x = float(element[1])
    y = float(element[2])
    z = float(element[3])
    if x > max_x:
      max_x = x
    if y > max_y:
      max_y = y
    if z > max_z:
      max_z = z
  max_coords = [max_x, max_y, max_z]

  min_coords = []
  min_x = 999
  min_y = 999
  min_z = 999
  for element in new_coords:
    x = float(element[1])
    y = float(element[2])
    z = float(element[3])
    if x < min_x:
      min_x = x
    if y < min_y:
      min_y = y
    if z < min_z:
      min_z = z
  min_coords = [min_x, min_y, min_z]

  lithium_positions = []
  pos_x_li = 'Li' + '    ' + "{:.4f}".format(float(max_coords[0]) + 3) + '    ' + str(com[1]) + '    ' + str(com[2])
  pos_x_li = pos_x_li.replace("    -", "   -")

  pos_y_li = 'Li' + '    ' + str(com[0]) + '    ' + "{:.4f}".format(float(max_coords[1]) + 3) + '    ' + str(com[2])
  pos_y_li = pos_y_li.replace("    -", "   -")

  pos_z_li = 'Li' + '    ' + str(com[0]) + '    ' + str(com[1]) + '    ' + "{:.4f}".format(float(max_coords[2]) + 3)
  pos_z_li = pos_z_li.replace("    -", "   -")

  neg_x_li = 'Li' + '    ' + "{:.4f}".format(float(min_coords[0]) - 3) + '    ' + str(com[1]) + '    ' + str(com[2])
  neg_x_li = neg_x_li.replace("    -", "   -")

  neg_y_li = 'Li' + '    ' + str(com[0]) + '    ' + "{:.4f}".format(float(min_coords[1]) - 3) + '    ' + str(com[2])
  neg_y_li = neg_y_li.replace("    -", "   -")

  neg_z_li = 'Li' + '    ' + str(com[0]) + '    ' + str(com[1]) + '    ' + "{:.4f}".format(float(min_coords[2]) - 3)
  neg_z_li = neg_z_li.replace("    -", "   -")

  lithium_positions.append(pos_x_li)
  lithium_positions.append(pos_y_li)
  lithium_positions.append(pos_z_li)
  lithium_positions.append(neg_x_li)
  lithium_positions.append(neg_y_li)
  lithium_positions.append(neg_z_li)

  return lithium_positions


# Parent Directory path
parent_dir = "Gaussian"

for row in df_test.iloc[:].itertuples(index=False):
  cas_no = row[4]
  smiles = row.smiles
  coord = cirpy.resolve(smiles, 'xyz').split("\n")

  lithiums = create_lithiums(coord[2:-1])
  
  path = os.path.join(parent_dir, str(cas_no)+'/inp0')
  if not os.path.exists(path):  
  # Create a new directory because it does not exist 
    os.makedirs(path) 
  # generate input file
  with open(path + '/inp.txt', 'w') as f:
    f.write("%Mem=16GB\n%NProcShared=8\n#P M062X/6-31+G** EmpiricalDispersion=GD3 SCRF(SMD,solvent=DiMethylSulfoxide) Opt Freq\n")
    f.write("\n")
    f.write(cas_no+"\n")
    f.write("\n")
    f.write("0 1\n")
    for c in coord[2:]:
      f.write(" "+c+"\n")
  
  counter = 1
  for li in lithiums:
    path = os.path.join(parent_dir, str(cas_no)+'/inp{}'.format(str(counter)))
    if not os.path.exists(path):  
    # Create a new directory because it does not exist 
      os.makedirs(path) 
    with open(path + '/inp.txt'.format(counter), 'w') as f:
      f.write("%Mem=16GB\n%NProcShared=8\n#P M062X/6-31+G** EmpiricalDispersion=GD3 SCRF(SMD,solvent=DiMethylSulfoxide) Opt Freq\n")
      f.write("\n")
      f.write(cas_no+"\n")
      f.write("\n")
      f.write("1 1\n")
      for c in coord[2:-1]:
        f.write(" "+c+"\n")
      f.write(" "+li+"\n")
      f.write("\n")
    counter += 1
