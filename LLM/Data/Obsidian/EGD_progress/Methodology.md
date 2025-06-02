


### Part 1: NACE to targets




#### Data

- gather data: NACE categories, target list, report 1 + report 1 annex
- ESTAT data: *estat_nama_10_a64*, *estat_env_ac_ainah_r2*


#### Connection to NACE categories
- LLM : data + prompt → assigns up to 3 NACE categories for each level for every target of a thematic area. Triplicats are generated per thematic area
- select triplicats with less NAs to have more data to work with and potentially discard during reviewing
- manually format and review the assignations

#### Connection to ESTAT data
- Manually connect ESTAT data to the targets based on the NACE classification.





### Part 2: targets interlinkages


#### Data
- targets were gathered by the team before i started the traineeship, and *target_NACE_classification.xlsx*. Based on various policy documents
- only 150 targets were selected as in Report1 where they have been assessed
- gathered data:  | thematic_area | sub_theme | target_code | policy_document_short | policy_document | target_content | SDG_code | target_assessment |  | sub_theme_justification | 

#### Determination of interlinkages 
- LLM: llama3.3 @ JRC: target data + subthemes/policy docs + assessments of report 1 + context of report2 + prompt (asking for positive/negative and weights 1to3)
- (annex: prompt, code, data)
- manually review and formatting 

#### Cross-validation with expert knowledge
- manually format into experts surveys
- send to experts
- manually aggregate expert-reviewed interlinkages

#### Network analysis
- network analysis verdiana