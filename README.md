## Use Python at CBS

Python is not installed by default at the CBS RA (yet). In order to use Python you need to ask CBS (`microdata@cbs.nl`) to activate it for you. 

There are a few packages that are installed by default (e.g., pandas, pyreadstat, matplotlib). 

If you need specific versions, you need to email CBS a environment.yml file with your requirements. This repository has a standard environment.yml with most of the tools researchers use. Before sending it, open "environment.yml" and change the number (0000 in the example) for your project number.

You can also create your own environment file locally, where 0000 is your project number:
```sh
conda create -n 0000 -c conda-forge python=3
conda activate 0000
conda install jupyter notebook scikit-learn pandas matplotlib seaborn jupyterlab notebook plotly IPython pyreadstat openpyxl dask vaex modin polars pyarrow numpy scipy statsmodels pymc3 eli5 SHAP LIME networkx igraph tensorflow keras pytorch pytorch_geometric 
conda env export --from-history > ~/environment.yml
```

If you require specific versions, you can check `conda env export` and add the versions to the `environment.yml` file.

Once CBS has installed it, you may see a new icon with the right version of Python. If this is not the case, you need to activate the Python environment manually. You can open a `Python Prompt`, and run the following code, where 0000 is your project number:

```sh
conda activate 0000.
jupyter notebook --notebook-dir=H:
```

That will open a jupyter notebook based on your shared disk (`H:`).


## Contact
This is a project by the [ODISSEI Social Data Science (SoDa)](https://odissei-data.nl/nl/soda/) team.
Do you have questions, suggestions, or remarks on the technical implementation? File an issue in the
issue tracker or feel free to contact [Erik-Jan van Kesteren](https://github.com/vankesteren).

