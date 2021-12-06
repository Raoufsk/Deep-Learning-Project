import pandas as pd
import plotly.express as px

from umap import UMAP

f = pd.read_csv(
    "preprocessed_file_v1", 
    header = 0, 
    index_col = 0, 
    sep = "\t")

file = pd.read_csv(
	"data_clinical_sample.txt", 
	header = 0, 
	index_col = 0, 
	sep = "\t")

data = f[["CANCER_TYPE", "SEX", "PRIMARY_RACE", "ETHNICITY", 
	"YEAR_CONTACT", "DEAD", "YEAR_DEATH"]]

f = f.drop(["CANCER_TYPE", "SEX", "PRIMARY_RACE", "ETHNICITY", 
	"YEAR_CONTACT", "DEAD", "YEAR_DEATH"], axis = 1)

reducer = UMAP(
    n_components = 2, 
    random_state = 0)

U = reducer.fit_transform(f)

df = pd.DataFrame(index = f.index)

df["U1"] = U[:, 0]
df["U2"] = U[:, 1]

df = df.join(file["SAMPLE_TYPE"])

fig = px.scatter(
    data_frame = df.dropna(), 
    x = "U1", y = "U2",
    color = "SAMPLE_TYPE", 
    title = "umap")

fig.show()
fig.write_html("fig_sample_type.html")