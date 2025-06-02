


Notes:
- Potential limitations? nature conservation activities  are hard to classify as nace.
	- eg: TA6.14, TA6.43


- I am confused by all the comments about sectors that are gonna be **impacted** , i thought we just want to have a snapshot of the current state of things??
- i need better definition of the boundaries and criteria for selection of the nace categories because for now it is all either AI choice or subjective choices from us that are not experts, i have doubts about the methodology and relevance of this work
- i dont believe in it, wouldnt want to publish it with my name first



## GHG
**data**: estat_env_ac_ainah_r2

- **|!|** NACE level 2 for category B is missing




## GVA
**data**: estat_nama_10_a64

- for level2 nace, there are is no data for category B, except one row "B-E". But there is data for detailed categores C and E level2. So I will delete the row "B-E". I tried to infer the value of "B" by substracting the values of row "B-E" by all the rows of "C" and "E" but some values are missing and I anyway don't get the same values as row "B" from level 1.
- **|!|** sum of level_2 percentages do not sum up to 100, probably because there are some missing values (NA), but we might infer this sums up to roughly 20%
- chemical and petrol-related nace always have missing data at level 2
- motor and vehicles also after 2015, but also other categories