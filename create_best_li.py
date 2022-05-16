import sys
import subprocess
import os

doc_to_energy = {}

def num2element(num:int)->str:
    """Obtain the atomic name associated with a given atomic number

    Args:
        num (int): the aforementioned given atomic number

    Returns:
        str: the aforementioned atomic name
    """
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

def get_energy(path:str)->float:
    """Obtain the sum of electronic and thermal free energies of a molecule given
    its filepath to its Gaussian software output

    Args:
        path (str): the aforementioned given filepath

    Returns:
        float: the aforemented summed free energy
    """
    try:
        g_str = subprocess.check_output("grep 'Sum of electronic and thermal Free Energies=' {}".format(path), shell=True)
        g_value = float(str(g_str).split()[-1][:-3])
    except:
        g_value = 9999
    return g_value

# this will catch terminal running case
# enter as:
# python3 create_best_li.py 'Gaussian/872-36-6/inp0/out.txt' 'Gaussian/872-36-6/inp1/out.txt' 'Gaussian/872-36-6/inp2/out.txt'
# right now, it is configured for three inputs, but you can add more to end and then change
# doc_filepaths to include up to end
if __name__ == '__main__':

    parent_dir = str(os.getcwd())
    print(parent_dir)

    cas_no = parent_dir.split('/')[-1]

    # store all filepaths in a list
    doc_filepaths = [parent_dir+"/"+arg+'/out.txt' for arg in sys.argv[1:8]]
    # doc_filepaths = sys.argv[1:8]
    print('given filepaths:',doc_filepaths)

    # for each filepath...
    for file in doc_filepaths:
        #create dic entry {filepath: energy}
        doc_to_energy[file] = get_energy(file)
    
    #get filepath associated with minimum energy
    min_energy_file = min(doc_to_energy, key=doc_to_energy.get)
    
    with open("free_e.txt", "a") as myfile:
        myfile.write(' Sum of electronic and thermal Free Energies=         ' + str(doc_to_energy[min_energy_file]) +'\n')
    
    print('path to min energy file:', min_energy_file)
    print('reached end')

    #str.format does not seem to work; therefore, using % operator instead
    ln_str = subprocess.check_output(["awk '/Standard orientation/{print NR}' %s | tail -1" % min_energy_file], shell=True)

    #this is the hard-coded alternative
    # ln_str = subprocess.check_output(["awk '/Standard orientation/{print NR}' Gaussian/872-36-6/inp1/out.txt | tail -1"], shell=True)

    ln_int = int(ln_str)

    #toy-example directory, hardcoded for this cas-no
    

    #create a new folder called opt_inp
    path = os.path.join(parent_dir, 'opt_inp')
    if not os.path.exists(path):  
    # Create a new directory because it does not exist 
        os.makedirs(path) 

    data = []
    ln_count = 0
    num_atom = 0

    # read the coordinates
    for line in open(min_energy_file):
        if (ln_count < (ln_int + 4)):
            ln_count = ln_count + 1
            continue
        if (line.startswith(' ----')):
            break
        num_atom = num_atom + 1
        ln_array = line.split()
        data.append([ln_array[1], ln_array[3], ln_array[4], ln_array[5]])

    f = open(path + '/opt.xyz', 'w')
    # print(name, file = f)
    print(num_atom, file = f)
    print("", file = f)

    for d in data:
        element = num2element(d[0])
        print(" {}   {}  {}  {}".format(element, d[1], d[2], d[3]), file = f)

    f.close()

    with open(path + '/inp.txt', 'w') as f:
        f.write("%Mem=16GB\n%NProcShared=8\n#P M062X/6-31+G** EmpiricalDispersion=GD3 SCRF(SMD,solvent=DiMethylSulfoxide) Opt Freq\n")
        f.write("\n")

        #cas-no is hard-coded since we are only using this molecule in our example;
        f.write(cas_no+"\n")
        f.write("\n")
        f.write("0 2\n")
        for d in data:
            element = num2element(d[0])
            f.write(" {}   {}  {}  {} \n".format(element, d[1], d[2], d[3]))
        f.write("\n")
    print("Gaussian standard output converted to xyz file !!!")
