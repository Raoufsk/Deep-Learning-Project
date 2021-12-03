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
print(samples.head())
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
to_keep = samples_genes[samples_genes["CANCER_TYPE"] > "500"]
to_keep = to_keep[to_keep.index != "UNKNOWN"]
to_keep = to_keep[to_keep.index != "Cancer of Unknown Primary"]

# without patients data
samples_genes.to_csv("preprocessed_file_v0_filtered", sep = "\t", compression = "zip")

# with patients data
samples_genes = samples_genes.join(samples[
	["SEX", "PRIMARY_RACE", "ETHNICITY", 
	"INT_CONTACT", "INT_DOD", "YEAR_CONTACT", 
	"DEAD", "YEAR_DEATH"]])

samples_genes.to_csv("preprocessed_file_v1_filtered", sep = "\t", compression = "zip")