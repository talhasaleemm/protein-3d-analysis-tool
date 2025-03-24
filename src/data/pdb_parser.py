import numpy as np
from Bio.PDB import PDBParser

def parse_pdb(file_name):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(file_name.split('.')[0], file_name)
    coords = []
    atom_types = []
    residue_names = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    coords.append(atom.get_coord())
                    atom_types.append(atom.get_name())
                    residue_names.append(residue.get_resname())
    return np.array(coords), atom_types, residue_names
