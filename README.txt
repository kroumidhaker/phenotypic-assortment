PHENOTYPIC ASSORTMENT AND THE EVOLUTION OF COOPERATION
IN FINITE PERIODIC PHENOTYPE SPACES
Dhaker Kroumi | Version 1.0.0

These files reproduce seven figures from the study:
fig1, fig2, fig3, fig4, fig5, fig5_threshold_vs_n,
and fig7_threshold_vs_L.

To run the code
1. Unzip the archive and open a terminal in this folder.
2. Install the packages:
   python -m pip install -r requirements.txt
3. Generate the figures and data:
   python reproduce.py
4. Compare your results with the supplied data:
   python verify_results.py

You can also open reproduce_figures.ipynb in Jupyter and select
Run All. Both options run the same calculations.

What is included
- reference_results/: the figures, numerical data, and checks.
- reproduce_figures.ipynb: the code, with figures shown inline.
- DATA_DICTIONARY.txt: parameters and data columns.
- numerical_notes.pdf and .tex: formulas and numerical methods.
- CITATION.cff: citation details.

New runs save their files in results/. The supplied reference results
are kept unchanged. No external data files are needed.

The code uses finite spectral sums. The largest cases use a convergent
series with a checked error bound, as explained in the numerical notes.
These are calculations of the analytical threshold, not population
simulations.

Tested with Python 3.12.14. Package versions are listed in requirements.txt.
If you use these files, please cite the paper and this Zenodo record.


LICENSES

The Python scripts and source code in reproduce_figures.ipynb are licensed under the MIT License; see LICENSE.

The numerical data in reference_results/data/ and figures in reference_results/figures/ are licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/

Attribution: Dhaker Kroumi. Please cite the associated paper and the Zenodo archive when using these materials.
