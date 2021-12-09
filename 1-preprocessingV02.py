import pandas as pd 
import numpy as np

samples = pd.read_csv(
	"data_clinical_sample.txt",
	header = 0, 
	index_col = 0, 
	sep = "\t",
	dtype = str)

patients = pd.read_csv(
	"data_clinical_patient.txt",
	header = 0, 
    index_col = 0,
	sep = "\t",
	dtype = str)

samples = samples.join(patients)

mutations = pd.read_csv(
	"data_mutations_extended.txt",
	header = 0, 
	sep = "\t",
	dtype = str)

samples_genes = pd.DataFrame(
	index = samples["SAMPLE_ID"], 
	columns = mutations["Hugo_Symbol"].unique(),
	dtype = str)

for gene, sample in zip(mutations["Hugo_Symbol"], mutations["Tumor_Sample_Barcode"]):
	samples_genes.at[sample, gene] = 1

samples_genes.fillna(0, inplace = True)

samples.set_index("SAMPLE_ID", inplace = True)
samples_genes = samples_genes.join(samples["CANCER_TYPE"])

# Filter the low represented cancer types
counts = samples_genes.groupby("CANCER_TYPE").agg({"CANCER_TYPE":"count"})
to_keep = counts[counts["CANCER_TYPE"] > 1500]
to_keep = to_keep[to_keep.index != "UNKNOWN"]
to_keep = to_keep[to_keep.index != "Cancer of Unknown Primary"]
samples_genes = samples_genes[samples_genes.CANCER_TYPE.isin(to_keep.index)]

# without patients data
samples_genes.to_csv("preprocessed_file_v0_filtered", sep = "\t", compression = "zip")

# with patients data
samples_genes = samples_genes.join(samples[
	["SEX", "PRIMARY_RACE", "ETHNICITY", 
	"YEAR_CONTACT", "DEAD", "YEAR_DEATH", "AGE_AT_SEQ_REPORT"]])

samples_genes.to_csv("preprocessed_file_v2_filtered", sep = "\t", compression = "zip")