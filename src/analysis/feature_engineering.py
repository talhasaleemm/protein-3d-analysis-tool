import numpy as np
import pandas as pd

def create_enriched_dataset(coords, atom_types, residue_names):
    df = pd.DataFrame(coords, columns=["X", "Y", "Z"])
    df['Atom_Type'] = atom_types
    df['Residue'] = residue_names

    # Synthetic features
    df['Distance_From_Center'] = np.sqrt(df['X']**2 + df['Y']**2 + df['Z']**2)
    df['XY_Angle'] = np.arctan2(df['Y'], df['X'])
    df['YZ_Angle'] = np.arctan2(df['Z'], df['Y'])
    df['XZ_Angle'] = np.arctan2(df['Z'], df['X'])

    # Labels based on distance, then randomly flip ~20% to avoid 100% accuracy
    df['Label'] = np.where(df['Distance_From_Center'] > df['Distance_From_Center'].median(), 1, 0)
    flip_mask = np.random.rand(len(df)) < 0.20
    df.loc[flip_mask, 'Label'] = 1 - df.loc[flip_mask, 'Label']
    return df
