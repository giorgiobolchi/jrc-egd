

# Project title 

*Giorgio Bolchi*

------------------------------------------------------------------------

## Table of contents

- Part 1
	- Goal
	- Methods Overview
	- Relevant folders & files
	- Pipeline
- Part 2
	- Goal
	- Methods Overview
	- Relevant folders & files
	- Pipeline
- Extensive file structure & descriptions
	- Notes on file names
------------------------------------------------------------------------
## Part 1

##### Goal:
- Assign NACE categories  (level 1,2 and 3) to each EGD targets, and deduct which NACE categories are currently involved with each target
- Then, connect ESTAT data based on NACE categories to obtain a current snapshot of the contributions of each target to GHG, GDP and employment.

#####  Methodology: 
1. Use an LLM to assign NACE categories (level1,2,3) based on the description of each target.
2. Manually review and clean the generated tables
3. (Cross-validation with expert knowledge?)
4. Connect targets with respective NACE categories to ESTAT data on GHG emissions, contribution to GVA, and employment.

#####  Relevant folders & files:

- **Input** **Data**:
	- ```target_NACE_classification+assessments.xlsx``` 
	- ``XLSX_target_data_v1.2.xlsx```
	- ```REPORT_1/report1.pdf```
	- ```REPORT_1/report1_annex.pdf```
	- ```NACEdata.py```

- **Code**:
	- ```LLM_NACE_TAsplit.ipynb```: jupyter notebook to automatically assign NACE categories to EGD targets, based on the content of report_1. Results are generated in triplicats for each TA separately, because feeding all the targets at the same time was too big for the model (back then I was using gpt-4o).
	- ```LLM_NACE_chunks.ipynb```: similar script to the one above, but the data is split by equally-sized chunks instead of TA. I did not use it to generate results as the first script already worked, but it could be used in the future.


- **Output Data**:
	- ```Data/Outputs/0131 - NACE_to_TA```:
		- ```trial_1 (triplicats per TA)/```: folder containing all the raw triplicat files (i.e., 3 generated files per TA), containing the respective targets and the automatically assigned NACE-categories at level 1, 2 and 3. It also contains the comparison tables, to assess the consistency between triplicats.
		- ```NACE_to_TA_assignations_reviewed_CG_GB.xlsx```: table containing all targets and their automatically assigned NACE-categories, which has beed reviewed by Chiara (CG) and Giorgio (GB).
		- ```NACEdata_to_TA.xlsx```: files where the NACE_to_TA data is put together with data about GHG, GVA and employment (EMP_DC). Some plots were made. The ESTAT data that I've gathered is located in ```Data/ESTAT/```.


##### Pipeline:
 1. Manually format ```target_NACE_classification+assessments.xlsx``` into ``XLSX_target_data_v1.2.csv``` 
 2. Gather the API requirements, the input data and run ```LLM_NACE_TAsplit.ipynb``` (details about the code are explained in-line)
 3. The code outputs a list of files (triplicats per TA). I use the last block of code in ```LLM_NACE_TAsplit.ipynb``` and the Data Wrangler view in VScode to verify the consistency of answers per TA.
 4. Select the triplicat with less NA values (i.e, more NACE assignations) so to have more data to work with, and to eventually correct and discard during reviewing.
 5. Manually review the assigned NACE categories (```NACE_to_TA_assignations_reviewed_CG_GB.xlsx```
 6. (Cross-validation by experts?)
 7. Connect ESTAT data to the targets based on the NACE classification (```ESTAT/```)

------------------------------------------------------------------------
## Part 2 

##### Goal: 
- map the interconnections between targets across thematic areas (i.e., how the achievement of a target might influence another target) and perform a network analysis to observe synergies, trade-offs and other measures such as centralities.

##### Methodology: 
1. Use an LLM to automatically assign positive and negative connections between all available targets, based on the target content and the context of report 1 and 2.
2. Cross-validate the LLM-generated connections with expert knowledge that would be gathered during expert consultation workshops
3. Perform a network analysis using Verdiana's code.


#####  Relevant folder & files:


- **Input** **Data**:
	- ```target_NACE_classification+assessments.xlsx``` 
	- ```NACEdata.py```
	- ```targets_data_150.csv```or ```targets_data_250.csv```
	- ```REPORT_2/``` 
	- # add update rep2 chapters


- **Code**:
	- ```LLM_network_chunks.ipynb```: script that splits the data into equally-sized chunks so that they can be compared with one another (and avoid overloading the LLM) and determines the interlinkages between targets using a LLM. I used it only to generate the network between all targets (not between sub-themes), which had too long output. It outputs an aggregated table of interlinkages that needs to be manually formatted and reviewed.
	- ```LLM_network_split.ipynb```: script that splits the data by thematic areas, generates all the potential pairs of thematic areas to be compared with one another, and that  generates the interlinkages between targets using a LLM. It outputs an aggregated table of interlinkages that needs to be manually formatted and reviewed. I used it to generate the network tables that are to be cross-validated by experts.
	- ```LLM_subthemes.ipynb```: small script to automatically assign targets into pre-defined sub-themes. The sub-themes were defined manually, by also taking into account the groups of targets mentioned in report 1. The output list needs to be manually reviewed as the assignations by the LLM are not always correct.
	- ```network_analysis.ipynb```: small script to do load the formatted network tables into the networkx python package, and perform basic network analysis. But it is not Verdiana's extensive network analysis script.


- **Output Data**:
	- ```Data/Outputs/:
		- 



##### Pipeline:
1. 
2. Select target dataset: ```targets_data_150.csv``` (i.e., only targets from report 1) or ```targets_data_250.csv```(i.e., all targets).
3.  Gather the API requirements, the input data, adjust the file paths and model parameters and run ```LLM_network_split.ipynb``` (details about the code are explained in-line)


------------------------------------------------------------------------
### Extensive file structure & descriptions

- `Code/`: contains scripts
- `Data/`: contains source datasets and results
- `Documentation/`: contains extra documentation


------------------------------------------------------------------------

- `Code/`: 
	- ```targets_to_obsidian/```: folder containing code and data to automatically generate .md files for each targets so that they can be loaded into Obsidian.
	- ```Steve/```: old code from Steve
	- ```Verdiana/```:  code from Verdiana
	- ```backups/```: backup data that is nice to have but that is not necessary anymore.
	- ```json_to_gexf/```: folder containing some trial-and-error code to convert Obsidian files network into json or gexf format.
	- ```token.txt```: text file containing access token for the LLM
	- ```API.py```: script to access the LLM API via GPT@JRC and define functions.
	- ```LLM_NACE_TAsplit.ipynb```: script to use the LLM to generate the data for Part 1 of this project. It splits the data into thematic areas and automatically assign NACE categories to EGD targets. It considers the context of report 1. It generates 3 series of assignations per thematic areas (i.e., triplicates), so that consistency of responses can be checked. It outputs an aggregated table of interlinkages that needs to be manually formatted and reviewed.
	- ```LLM_NACE_chunks.ipynb```: script that splits the data into equally-sized chunks and automatically assign NACE categories to EGD targets using an LLM. It considers the context of report 1. It outputs an aggregated table of interlinkages that needs to be manually formatted and reviewed.
	- ```LLM_network_chunks.ipynb```: script that splits the data into equally-sized chunks so that they can be compared with one another (and avoid overloading the LLM) and determines the interlinkages between targets using a LLM. I used it only to generate the network between all targets (no sub-themes), which was too long. It outputs an aggregated table of interlinkages that needs to be manually formatted and reviewed.
	- ```LLM_network_split.ipynb```: script that splits the data by thematic areas, generates all the potential pairs of thematic areas to be compared with one another, and that  generates the interlinkages between targets using a LLM. I used it to generate the network tables that are to be cross-validated by experts. It outputs an aggregated table of interlinkages that needs to be manually formatted and reviewed.
	- ```LLM_subthemes.ipynb```: small script to automatically assign targets into pre-defined sub-themes. The sub-themes were defined manually, by also taking into account the groups of targets mentioned in report 1. The output list needs to be manually reviewed as the assignations by the LLM are not always correct.
	- ```LLM_trials.ipynb```: just a sandbox script to try things out.
	- ```network_analysis.ipynb```: small script to do load the formatted network tables into the networkx python package, and perform basic network analysis. It is not Verdiana's extensive network analysis script.

- `Data/`: 
	- ```backups/```: backup datasets that are potentially not relevant anymore
	- ```ESTAT/```: contains the ESTAT dataset inventory (generated by Michele) as well as those I have downloaded (GHG,GVA,employment)
	- ```Outputs/```: main output folders for generated results, it includes folders sorted by date. The folders with relevant data have been complemented with a title.
		- ```0131 - NACE_to_TA/```: main results folder for the Part 1 of this project. You can find all the aggregated NACE_to_target data in *NACE_to_TA_assignations_reviewed_CG_GB.xslx*
		- ```0319 - subthemes_to_targets/```: here i tried to automatically assign sub-themes to targets but it was not satisfying (I ended up chosing the subthemes manually).
		- ### ADD NEW NETWORK_150subthemes+weights data 
		- ### ADD NEW NETWORK_150policydocs+weights data 

	- ```targets_data_150.csv```: list of targets that are in report 1, with data on |thematic_area_code|thematic_area|sub_theme|target_code|target_content|target_assessment|sub_theme_justification|
	- ```targets_data_250.csv```: list of all targets (from *target_NACE_classification+assessments.xlsx*) with the same columns as in```targets_data_150.csv```.
	- ```target_NACE_classification.xlsx```: initial data table i was provided with.
	- ```target_NACE_classification+assessments.xlsx```: same table as above, but where I also added the assessments from report 1 to each target.
	- ```NACEdata.py```: list of NACE categories.


- `Documentation/`:
	- ```JRC_chat_models.csv```: list of available models at the JRC (in February 2025).
	- other files



------------------------------------------------------------------------

Notes on file names:

- "*network_150*" = interlinkages based on the ~150 targets from report1
- "*network_250*" / "*network_250+*" / "*network_254*" = interlinkages based on the ~250 targets from all the available targets