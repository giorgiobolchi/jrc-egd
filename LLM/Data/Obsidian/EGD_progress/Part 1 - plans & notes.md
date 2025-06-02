



**goal**: 
- Assign NACE categories  (level 1,2 and 3) to each EGD targets, and deduct which NACE categories are currently involved with each target
- Then, connect ESTAT data based on NACE categories to  obtain a current snapshot of the contributions of each target to GHG, GDP and employment.

**methods**: 
- Use an LLM to assign NACE categories (level1,2,3) based on the description of each target.
- Manually review and clean the generated tables
- (Cross validation with expert knowledge through a workshop?)
- Connect targets with respective NACE categories to ESTAT data on GHG emissions, contibution to GVA, and employment.



## Plans

### A. LLama + report1

- [ ] redefine and re-run using local JRC LLama 3.3 + including correct report1
	- [x] Check code simone 
- [x] regenerate all tables → didnt work, went with gpt-4o results
- [x] clean tables
- [x] review
- [ ] connect NACE data to each target
	- GHG: MTons CO2 eq (including methane etc..)
	- GDP: GVA
	- Employment: EMP_DC
	- check chapter 1 (?) report 2 part of Robert → *Economic_context_2pager_ElMeligi_v1*



 big table: 
|target|nace_cat|ghg|gdp|emplyoment. (here it is simplified)



ideas of what to do with data:
amount of targets related to a nace categories (eg barplot?)



### C. Macro groups

### B. All targets to all nace_lvl3 → then drop


# Notes

from [[2025-01-21]] to [[2025-02-27]]
