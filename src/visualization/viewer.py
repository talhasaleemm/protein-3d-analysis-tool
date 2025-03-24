import py3Dmol

def visualize_3d_structure(pdb_id, view_style='cartoon'):
    viewer = py3Dmol.view(query=f'pdb:{pdb_id}', width=600, height=400)
    if view_style == 'cartoon':
        viewer.setStyle({'cartoon': {'color': 'spectrum'}})
    elif view_style == 'stick':
        viewer.setStyle({'stick': {}})
    elif view_style == 'sphere':
        viewer.setStyle({'sphere': {'scale': 0.3}})
    elif view_style == 'surface':
        viewer.setStyle({'surface': {'opacity': 0.8}})
    viewer.addSurface(py3Dmol.VDW, {'opacity': 0.6, 'color': 'white'}, {'hetflag': True})
    viewer.addStyle({'hetflag': True}, {'stick': {'colorscheme': 'greenCarbon', 'radius': 0.2}})
    viewer.addStyle({'water': True}, {'sphere': {'colorscheme': 'blueTint', 'radius': 0.2}})
    viewer.zoomTo()
    viewer.spin(True)
    return viewer
