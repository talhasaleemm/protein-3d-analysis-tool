import requests

def download_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        file_name = f"{pdb_id}.pdb"
        with open(file_name, "wb") as file:
            file.write(response.content)
        return file_name
    else:
        raise ValueError(f"Failed to fetch PDB file for ID {pdb_id}. Status Code: {response.status_code}")

def fetch_protein_metadata(pdb_id):
    try:
        url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            title = data.get('struct', {}).get('title', 'Not available')
            resolution = data.get('rcsb_entry_info', {}).get('resolution_combined', 'Not available')
            experimental_method = data.get('exptl', [{}])[0].get('method', 'Not available')
            deposition_date = data.get('rcsb_accession_info', {}).get('deposit_date', 'Not available')
            return {
                'title': title,
                'resolution': resolution,
                'experimental_method': experimental_method,
                'deposition_date': deposition_date
            }
        else:
            return {
                'title': 'Metadata unavailable',
                'resolution': 'N/A',
                'experimental_method': 'N/A',
                'deposition_date': 'N/A'
            }
    except Exception:
        return {
            'title': 'Error fetching metadata',
            'resolution': 'N/A',
            'experimental_method': 'N/A',
            'deposition_date': 'N/A'
        }
