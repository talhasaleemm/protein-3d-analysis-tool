from setuptools import setup, find_packages

setup(
    name="protein3d",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'requests',
        'biopython',
        'scikit-learn',
        'py3Dmol',
        'ipywidgets',
        'jupyter'
    ],
    entry_points={
        'console_scripts': [
            'protein3d=main:create_interface',
        ],
    },
)
