# Traineeship project

Giorgio Bolchi

------------------------------------------------------------------------

## Table of Contents
1. [Part 1](#part-1)
	- Goal
	- Methodology
	- Relevant folders & files
	- Pipeline
2. [Part 2](#part-2)
	- Goal
	- Methodology
	- Relevant folders & files
	- Pipeline
3. [Extensive File Structure & Descriptions](#extensive-file-structure--descriptions)
	 - Files
	 - Notes on file names

------------------------------------------------------------------------

## Part 1 -  NACE to targets

### Goal
- Assign NACE categories (level 1, 2, and 3) to each EGD target and deduce which NACE categories are currently involved with each target.
- Connect ESTAT data based on NACE categories to obtain a current snapshot of the contributions of each target to GHG, GDP, and employment.

### Methodology
1. Use an LLM to assign NACE categories (level 1, 2, and 3) based on the description of each target. I have used *llama-3.3-70b-instruct* through GPT@JRC.
2. Manually review and clean the generated tables.
3. (Cross-validation with expert knowledge?)
4. Connect targets to ESTAT data (GHG emissions, contribution to GVA, and employment) based on the NACE categories.

### Relevant Folders & Files
#### Input Data
- `target_NACE_classification+assessments.xlsx`: initial table
- `targets_data_250.csv`: dataset of all targets and associated data.
- `REPORT_1/report1.pdf`: Report 1 (Marelli et al., 2025)
- `REPORT_1/report1_annex.pdf`: Report 1 annex (Marelli et al., 2025)
- `NACEdata.py`: list of NACE categories (level 0 to 3)

#### Code
- `LLM_NACE_chunks.ipynb`: script to split the data in equally-sized chunks, and automatically assign NACE categories to each EGD targets based on their content and the context of report 1.
- `LLM_NACE_TAsplit.ipynb`: script to split the data per TA, and automatically assign NACE categories to each EGD targets based on their content and the context of report 1.



#### Output Data
- `Data/Outputs/0131 - NACE_to_TA`:
  - `trial_1 (triplicats per TA)/`: Folder containing all the raw triplicat files.
  - `NACE_to_TA_assignations_reviewed_CG_GB.xlsx`: Table containing all targets and their automatically assigned NACE categories.
  - `NACEdata_to_TA.xlsx`: Files where the NACE_to_TA data is put together with data about GHG, GVA, and employment (EMP_DC).

### Pipeline
1. Manually format and clean `target_NACE_classification+assessments.xlsx` into `XLSX_target_data_v1.2.csv`. Or select a dataset I have already formatted:  `targets_data_150.csv` or `targets_data_250.csv`. 
2. Gather the API requirements, the desired input data, and run `LLM_NACE_TAsplit.ipynb`.
3. The code outputs a list of files (3 replicats per TA).
4. Select the triplicats with less NA values
5. Manually aggregate all the TAs together and review the assigned NACE categories.
6. Manually connect ESTAT data to the targets based on the NACE classification.

**notes**: during Part 1 of this project I was still getting to know the LLM and a lot of the process was done manually.  I also used *gpt-4o* to assign NACE categories to the targets, but in the future it would be better to do it with the in-house JRC models (e.g., *llama3.3*). This whole pipeline would benefit from some improvements and automations.

------------------------------------------------------------------------
## Part 2 - Interlinkages networks

### Goal
- Map the interconnections between targets across thematic areas and perform a network analysis to observe synergies, trade-offs, and other measures such as centralities.

### Methodology
1. Use an LLM to automatically assign positive and negative connections between all available targets based on the target content and the context of report 1 and 2.
2. Cross-validate the LLM-generated connections with expert knowledge gathered during expert consultation workshops.
3. Perform a network analysis using Verdiana's code.

### Relevant Folders & Files
#### Input Data
- `target_NACE_classification+assessments.xlsx`
- `targets_data_150.csv` or `targets_data_250.csv`
- `REPORT_2/`
- ```subthemes.py```

#### Code
- `LLM_subthemes.ipynb`: Small script to automatically assign targets into pre-defined sub-themes.
- `LLM_network_TAsplit.ipynb`: Script that splits the data by thematic areas, generate all potential pairs of TA, and determines the interlinkages between targets within each TA pairs using a LLM. Splitting per TA avoid the generation of intra-TA interlinkages.
- `network_analysis.ipynb`: Small script to load the formatted network tables into the networkx Python package and perform basic network analysis.

(optional)
-  `LLM_network_chunks.ipynb`: Script that splits the data into equally-sized chunks, generate all potential pairs of chunks, and determines the interlinkages between targets within each chunk pairs using a LLM. I wrote it but did not end up using it as this creates intra-TA interlinkages. Instead, I split the data per TA (see `LLM_network_TAsplit.ipynb`).

#### Output Data
- `Data/Outputs/`: Main output folders for generated results.

### Pipeline
1. Double-check the list of manually selected sub-themes in `subthemes_list.py`.
2. Run `LLM_subthemes.ipynb` to automatically assign each target into sub-themes.
3. Manually review the sub-themes assignations.
4. Select a targets dataset: `targets_data_150.csv` or `targets_data_250.csv`.
5. Gather the API requirements, the desired input data, adjust the file paths and model parameters, and run `LLM_network_TAsplit.ipynb`.
6. Manually format and clean the aggregated results.
7. Manually review the interlinkages.
8. Cross-validate with expert knowledge.
9. Perform a network analysis with Verdiana's code.


------------------------------------------------------------------------
## Extensive File Structure & Descriptions

- ```Code/```:
	- `token.txt`: Text file containing access token for the LLM.
	- `API.py`: Script to access the LLM API via GPT@JRC and define useful related functions.
	- `LLM_NACE_TAsplit.ipynb`: Script to use the LLM to generate the data for Part 1 of this project: automatically assigns NACE categories to EGD targets.
	- `LLM_NACE_chunks.ipynb`: Script that splits the data into equally-sized chunks and automatically assigns NACE categories to EGD targets.
	- `LLM_network_chunks.ipynb`: Script that splits the data into equally-sized chunks, generate all potential pairs of chunks, and determines the interlinkages between targets within each chunk pairs using a LLM. I wrote it but did not end up using it as this creates intra-TA interlinkages. Instead, I split the data per TA (see `LLM_network_TAsplit.ipynb`).
	- `LLM_network_TAsplit.ipynb`: Script that splits the data by thematic areas, generate all potential pairs of TA, and determines the interlinkages between targets within each TA pairs using a LLM. Splitting per TA avoid the generation of intra-TA interlinkages.
	- `LLM_subthemes.ipynb`: Small script to automatically assign targets to pre-defined sub-themes using a LLM.
	- `network_analysis.ipynb`: Small script to load the formatted network tables into the networkx Python package and perform basic network analysis.

 - ```Data/```:
	- `backups/`: Backup data that is nice to keep but not necessary anymore.
	- `ESTAT/`: Contains the ESTAT dataset inventory and the downloaded datasets (GHG, GVA, employment).
	- `Outputs/`: Main output folders for generated results.
	- `targets_data_150.csv`: list of targets that are in report 1 (i.e., that have been assessed) and associated data.
	- `targets_data_250.csv`: list of all targets and associated data.
	- `target_NACE_classification.xlsx`: Initial dataset I was provided with.
	- `target_NACE_classification+assessments.xlsx`: Same table as above, but with assessments from report 1 added.
	- `NACEdata.py`: List of NACE categories.
	- `subthemes.py`: Lists of sub-themes that were manually selected.


 - ```Documentation/```:
	- `JRC_chat_models.csv`: List of available models at the JRC.
	- Other files.

## Notes on File Names
- "*network_150*" = Interlinkages based on the ~150 targets from report 1.
- "*network_250*" / "*network_250+*" / "*network_254*" = Interlinkages based on the ~250 targets from all available targets.
