## Use Python at CBS

This repository contains a general environment.yml to send to Statistics Netherlands

Before sending, open "environment.yml" and change the number (0000 in the example) for your project number.

You can also create you, where 0000 is your project number:
```sh
conda create -n 0000 -c conda-forge python=3
conda activate 0000
conda install jupyter notebook scikit-learn pandas matplotlib seaborn jupyterlab notebook plotly IPython pyreadstat openpyxl dask vaex modin polars pyarrow numpy scipy statsmodels pymc3 eli5 SHAP LIME networkx igraph tensorflow keras pytorch pytorch_geometric 
conda env export --from-history > ~/environment.yml
```


Once we have the environment available, you can activate it from Python Prompt with, where 0000 is your project number:

```sh
conda activate 0000.
jupyter notebook --notebook-dir=H:
``
