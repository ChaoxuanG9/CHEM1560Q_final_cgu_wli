
# High-Throughput Work Flow for Calculating Reduction Potential of Lithium-Molecule Complexes

Our primary motivation behind this project was to extend our understanding of the chemical behavior of Li-ion battery additives. However, additive molecules are not always free-standing. Rather, they are likely associated with the Li+ ions at the electrode surface regions, thus bringing the entire complexes into reactions instead of solely the additives.

As such, this project presents a High-Throughput Work Flow for calculating the reduction potentials of the aforementioned Li-Molecule complexes. This is done by creating various Bash and Python scripts included in this repository.

The entire system works as follows:
1. Read in molecules given their CAS-NO and convert them into collections of coordinates of its constituent atoms. This is done using the CIRpy package.
2. Determine the optimal geometric configuration of the molecule complexed with the Li ion. To do this, we placed the Li ion in six different positions: 3 angstroms away from the  max-X, max-Y, max-Z, min-X, min-Y, and min-Z positions of the molecule. All six initial geometries were then fed into Gaussian to determine the "optimal" complex on the basis of the lowest free energy.
3. The "optimal" complex is then inputted into Gaussian once more, this time in a reduced state. This way, we are able to obtain the reduced free energy of Li-Molecule complex.
4. The reduction potential is finally calculated according to the following equation: $V_{red}=\{G_{tot}(A) - G_{tot}(A^-)\} /e - V_{shift}$ , where $V_{shift}$ corresponds to the difference between the absolute potential ($V_{abs}$) and the magnitude of the redox potential of the Li metal ($|V_{Li}|$)

### Gaussian Input Parameters Used:
```
%Mem=16GB
%NProcShared=8
#P UM062X/6-31+G** em=GD3 SCRF(SMD,solvent=DiMethylSulfoxide) Opt Freq SCF=XQC
#P M062X/6-31+G** EmpiricalDispersion=GD3 SCRF(SMD,solvent=DiMethylSulfoxide) Opt Freq
```
## Authors & Contributions

- Winston Li: Helped program work_flow.py and create_best_li.py. Oversaw general documentation of code.
- Chaoxuan Gu: Literature search, helped create .sh scripts. Oversaw Gaussian operations.


## References
1. Okamoto, Y. and Kubo, Y. (2018) ‘Ab Initio Calculations of the Redox Potentials of Additives for Lithium-Ion Batteries and Their Prediction through Machine Learning’, ACS Omega, 3(7), pp. 7868–7874. [doi:10.1021/acsomega.8b00576.](https://pubs-acs-org.revproxy.brown.edu/doi/abs/10.1021/acsomega.8b00576)
2. Marenich, A.V. et al. (2014) ‘Computational electrochemistry: prediction of liquid-phase reduction potentials’, Physical Chemistry Chemical Physics, 16(29), pp. 15068–15106. [doi:10.1039/C4CP01572J](https://pubs.rsc.org/en/content/articlelanding/2014/cp/c4cp01572j).
3. Sitzmann, M. et al. NCI/CADD Chemical Identity Resolver. https://cactus.nci.nih.gov/chemical/structure. 