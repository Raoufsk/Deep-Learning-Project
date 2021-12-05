#Author: BOUDEMIA Ala eddine
#UMAP for based on cancer type

import pandas as pd
import plotly.express as px

from umap import UMAP

f = pd.read_csv(
    "preprocessed_file_v0", 
    header = 0, 
    index_col = 0, 
    sep = "\t")

reducer = UMAP(
    n_components = 2, 
    random_state = 0)

U = reducer.fit_transform(
    f.iloc[:, f.columns != "CANCER_TYPE"])

df = pd.DataFrame(index = f.index)

df["U1"] = U[:, 0]
df["U2"] = U[:, 1]

df = df.join(f["CANCER_TYPE"])

fig = px.scatter(
    data_frame = df.dropna(), 
    x = "U1", y = "U2",
    color = "CANCER_TYPE", 
    title = "umap")

fig.show()