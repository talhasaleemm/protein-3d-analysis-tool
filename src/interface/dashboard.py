import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import functions from your modules
from src.data.pdb_fetcher import download_pdb, fetch_protein_metadata
from src.data.pdb_parser import parse_pdb
from src.analysis.feature_engineering import create_enriched_dataset
from src.analysis.model import train_evaluate_model
from src.visualization.viewer import visualize_3d_structure
from src.visualization.plot_utils import fig_to_base64

def run_analysis(pdb_id, view_style='cartoon'):
    try:
        pdb_file = download_pdb(pdb_id)
        metadata = fetch_protein_metadata(pdb_id)
        coords, atom_types, residue_names = parse_pdb(pdb_file)
        df = create_enriched_dataset(coords, atom_types, residue_names)

        residue_counts = df['Residue'].value_counts().head(10)
        X = df[['X', 'Y', 'Z', 'Distance_From_Center', 'XY_Angle', 'YZ_Angle', 'XZ_Angle']]
        y = df['Label']
        accuracy, class_report, cm, feature_importance, model = train_evaluate_model(X, y)

        # Generate plots (confusion matrix, feature importance, residue distribution, scatter plot)
        cm_fig, cm_ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=["Class 0", "Class 1"],
                    yticklabels=["Class 0", "Class 1"], ax=cm_ax)
        cm_ax.set_xlabel('Predicted')
        cm_ax.set_ylabel('Actual')
        cm_ax.set_title('Confusion Matrix')
        cm_base64 = fig_to_base64(cm_fig)

        fi_fig, fi_ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='Importance', y='Feature', data=feature_importance,
                    ax=fi_ax, palette='viridis')
        fi_ax.set_title('Feature Importance')
        fi_base64 = fig_to_base64(fi_fig)

        res_fig, res_ax = plt.subplots(figsize=(8, 5))
        residue_counts.plot(kind='bar', ax=res_ax,
                            color=sns.color_palette("husl", len(residue_counts)))
        res_ax.set_title('Top 10 Residues Distribution')
        res_base64 = fig_to_base64(res_fig)

        scatter_fig = plt.figure(figsize=(8, 8))
        ax = scatter_fig.add_subplot(111, projection='3d')
        sample_indices = np.random.choice(len(df), min(1000, len(df)), replace=False)
        sample_df = df.iloc[sample_indices]
        sample_predictions = model.predict(X.iloc[sample_indices])
        ax.scatter(sample_df['X'], sample_df['Y'], sample_df['Z'],
                   c=sample_predictions, cmap='coolwarm', alpha=0.7, s=30)
        ax.set_title('3D Distribution of Atoms with Predicted Classes')
        scatter_base64 = fig_to_base64(scatter_fig)

        viewer = visualize_3d_structure(pdb_id, view_style)

        html_report = f"""
        <div style="font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto;
                    background: linear-gradient(to bottom right, #f7f8fa, #e9ecef);
                    padding: 20px; border-radius: 15px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1); color: #333;">
            <div style="background: linear-gradient(to right, #3a0ca3, #4361ee);
                        color: #fff; padding: 20px; border-radius: 10px;
                        text-align: center; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 28px;">Protein 3D Structure Analysis Report</h1>
                <h2 style="margin: 10px 0 0 0; font-size: 22px;">PDB ID: {pdb_id}</h2>
                <p style="font-style: italic; margin: 5px 0 0 0;">
                    Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}
                </p>
            </div>
            <!-- More HTML code to embed the plots and metadata -->
        </div>
        """
        display(HTML(html_report))
        display(viewer)
        return df, model

    except ValueError as ve:
        error_html = f"""
        <div style="background-color: #fff; color: #000; padding: 20px;
                    border-radius: 10px; text-align: center; margin: 20px 0;
                    border: 2px solid #f44336;">
            <h3 style="margin:0;">Error Occurred</h3>
            <p>{ve}</p>
            <p>Please check the PDB ID and try again.</p>
        </div>
        """
        display(HTML(error_html))
    except Exception as e:
        error_html = f"""
        <div style="background-color: #fff; color: #000; padding: 20px;
                    border-radius: 10px; text-align: center; margin: 20px 0;
                    border: 2px solid #f44336;">
            <h3 style="margin:0;">Unexpected Error</h3>
            <p>{e}</p>
            <p>Please try again with a different PDB ID or check your connection.</p>
        </div>
        """
        display(HTML(error_html))

def create_interface():
    # Code for widgets and layout similar to your original script
    # Create inputs, progress bars, buttons and bind them to run_analysis
    # Then display the interface with IPython.display
    pass

if __name__ == "__main__":
    create_interface()
