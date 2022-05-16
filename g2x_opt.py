"""
convert molecualr geometry from Gaussian output to xyz format
"""

import subprocess

# line number of the last coordinate output
ln_str = subprocess.check_output("awk '/Standard orientation/{print NR}' out.txt | tail -1", shell=True)
ln_int = int(ln_str)
# print(ln_int)

ln_count = 0
num_atom = 0

data = []

def num2element(num):
    return {
        '1': 'H',
        '2': 'He',
        '3': 'Li',
        '4': 'Be',
        '5': 'B',
        '6': 'C',
        '7': 'N',
        '8': 'O',
        '9': 'F',
        '10': 'Ne',
        '11': 'Na',
        '12': 'Mg',
        '13': 'Al',
        '14': 'Si',
        '15': 'P',
        '16': 'S',
        '17': 'Cl',
        '18': 'Ar',
        '19': 'K',
        '20': 'Ca',
        '21': 'Sc',
        '22': 'Ti',
        '23': 'V',
        '24': 'Cr',
        '25': 'Mn',
        '26': 'Fe',
        '27': 'Co',
        '28': 'Ni',
        '29': 'Cu',
        '30': 'Zn',
        '31': 'Ga',
        '32': 'Ge',
        '33': 'As',
        '34': 'Se',
        '35': 'Br',
        '36': 'Kr',
        '40': 'Zr',
        '41': 'Nb',
        '42': 'Mo',
        '47': 'Ag',
        '49': 'In',
        '50': 'Sn',
        '51': 'Sb',
        '52': 'Te',
        '53': 'I',
        '56': 'Ba',
        '78': 'Pt',
        '79': 'Au'
    }.get(num)

# read the coordinates
for line in open('out'):
    if (ln_count < (ln_int + 4)):
        ln_count = ln_count + 1
        continue
    if (line.startswith(' ----')):
        break
    num_atom = num_atom + 1
    ln_array = line.split()
    data.append([ln_array[1], ln_array[3], ln_array[4], ln_array[5]])

f = open('opt_xyz.txt', 'w')
# print(name, file = f)
print(num_atom, file = f)
print("", file = f)

for d in data:
    element = num2element(d[0])
    print(" {}   {}  {}  {}".format(element, d[1], d[2], d[3]), file = f)

f.close()
print("Gaussian standard output converted to xyz file !!!")