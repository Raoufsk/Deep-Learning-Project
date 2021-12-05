#Author: BOUDEMIA Ala eddine
#Plot different histograms and pie charts

import pandas as pd
import plotly.express as px

file = pd.read_csv(
	"data_clinical_sample.txt", 
	header = 0, 
	index_col = 0, 
	sep = "\t")

file = file[
	["SAMPLE_TYPE", "CANCER_TYPE", 
	"CANCER_TYPE_DETAILED"]]

fig1 = px.histogram(
	file, x = "SAMPLE_TYPE")
fig1.show()
fig1.write_html("hist_sample_type.html")

fig2 = px.histogram(
	file, x = "CANCER_TYPE") 
fig2.show()
fig2.write_html("hist_cancer_type.html")

var = file.groupby("CANCER_TYPE").agg({"CANCER_TYPE":"count"})
fig3 = px.pie(
	var, 
	values = "CANCER_TYPE", 
	names = var.index)
fig3.show()
fig3.write_html("pie_cancer_type.html")

to_keep = var[var["CANCER_TYPE"] > 500]
to_keep = to_keep[to_keep.index != "UNKNOWN"]
to_keep = to_keep[to_keep.index != "Cancer of Unknown Primary"]

fig4 = px.histogram(
	to_keep, 
	x = to_keep.index,
	y = "CANCER_TYPE") 
fig4.show()
fig4.write_html("hist_cancer_type_filtered.html")

fig5 = px.pie(
	to_keep, 
	values = "CANCER_TYPE", 
	names = to_keep.index)
fig5.show()
fig5.write_html("pie_cancer_type_filtered.html")