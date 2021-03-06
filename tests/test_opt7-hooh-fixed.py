#! Various constrained energy minimizations of HOOH with cc-pvdz RHF.
#! For "fixed" coordinates, the final value is provided by the user.
import pytest

import psi4
import optking

# Minimized energy with OH bonds at 0.950 Angstroms.  #TEST
OH_950_stre       = -150.78666731                     #TEST
# Minimized energy with OOH angles at 105.0 degrees.  #TEST
OOH_105_bend      = -150.78617696                     #TEST
# Minimized energy with HOOH torsion at 120.0 degrees.  #TEST
HOOH_120_dihedral = -150.78664695                       #TEST

# Constrained minimization with O-H bonds fixed to reach equilibrium at 0.950 Angstroms.

f1 = ({'fixed_distance': "1 2 0.950 3 4 0.950"}, OH_950_stre)
f2 = ({'fixed_bend': '1 2 3 105 2 3 4 105.0'}, OOH_105_bend)
f3 = ({'fixed_dihedral': '1 2 3 4 120.0'}, HOOH_120_dihedral)

@pytest.mark.parametrize("option, expected", [f1, f2, f3])
def test_hooh_fixed_OH_stre(option, expected):
    hooh = psi4.geometry("""
      H
      O 1 0.90
      O 2 1.40 1 100.0 
      H 3 0.90 2 100.0 1 115.0
    """)

    psi4.core.clean_options()

    psi4_options = {
      'diis': 'false',
      'basis': 'cc-pvdz',
      'g_convergence': 'gau_verytight'
    }
    
    psi4.set_options(psi4_options)
    
    psi4.set_module_options('Optking', option)
    
    json_output = optking.optimize_psi4('hf')
    E = json_output['energies'][-1]
    assert psi4.compare_values(expected, E)  # TEST


#def test_hooh_fixed_OOH_bend():    
#    # Constrained minimization with O-O-H angles fixed to reach eq. at 105.0 degrees.
#    hooh = psi4.geometry("""
#      H
#      O 1 0.90
#      O 2 1.40 1 100.0
#      H 3 0.90 2 100.0 1 115.0
#    """)
#    psi4options = {
#      'diis': 'false',
#      'basis': 'cc-pvdz',
#      'g_convergence': 'gau_verytight'
#    }
#
#    psi4.set_options(psi4options)
# 
#    bend_coordinates = (""" 
#        1 2 3 105.0 
#        2 3 4 105.0
#    """)
#    
#    psi4.set_module_options('Optking', {'fixed_bend': bend_coordinates})
#    
#    json_output = optking.Psi4Opt('hf', psi4options)
#    thisenergy = json_output['properties']['return_energy']
#    assert psi4.compare_values(OOH_105_bend , thisenergy, 6, "Int. Coord. RHF opt of HOOH with O-O-H fixed to 105, energy") #TEST
#
#def test_hooh_fixed_HOOH_tor():    
#    # Constrained minimization with H-O-O-H dihedral fixed to 120.0 degrees.
#    hooh = psi4.geometry("""
#      H
#      O 1 0.90
#      O 2 1.40 1 100.0
#      H 3 0.90 2 100.0 1 115.0
#    """)
#    
#    psi4options = {
#      'diis': 'false',
#      'basis': 'cc-pvdz',
#      'g_convergence': 'gau_verytight'
#    }
#
#    psi4.set_options(psi4options)
#
#    dihedral_angle = ("""
#        1 2 3 4 120.0
#    """)
#    
#    psi4.set_module_options('Optking', {'fixed_dihedral': dihedral_angle})
#    
#    json_output = optking.Psi4Opt('hf', psi4options)
#    thisenergy = json_output['properties']['return_energy']
#    assert psi4.compare_values(HOOH_120_dihedral , thisenergy, 6, "Int. Coord. RHF opt of HOOH with H-O-O-H fixed to 120, energy") #TEST
