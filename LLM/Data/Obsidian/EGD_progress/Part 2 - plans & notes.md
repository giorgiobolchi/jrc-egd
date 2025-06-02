 

##### Goal: 
- map the interconnections between targets across thematic areas (eg, how the achievement of a target might influence another target) and perform a network analysis (connection with Verdiana's work) to determine synergies, trade-offs and other measures such as centralities.

##### Methods logic: 
- Use an LLM to automatically assign positive and negative connections between all available targets, based on the target content and the context of report 1 and 2.
- Cross-validate the LLM-generated connections with expert knowledge that would be gathered during expert consultation workshops

##### Strategies timeline

1. **all targets + report1**
	- feed all targets table and report 1 and ask the LLM to connect targets based on their interfluences
	- → **failed**,  llama3.3. can't take sucha big prompt

2. **separate TAs loop + report1**
	- feed report 1 (without references to make it shorter )  and targets separately by TA and ask the LLM to connect targets based on their interinfluences, loop through all the possible TA pairs (in both directions) because we can't feed everything in one go
	- → **failed**, some TA pairs are too which also make the prompt long for  llama3.3.

3. **Chunks loop+ report1**
	- [[2025-03-06]] → [[2025-03-10]]
	- divide targets dataset into 10 equal-sized chunks, and add report 1 (without references), and then loop over all the possible chunk pairs in both directions and for each ask the LLM to assign connections based on potential influences of targets on one another. This chunk-division strategy is chosen so that the final prompt  will have an amount of tokens inferior to ~85k tokens, which should be manageable by the JRC llama3.3. 
		- → **worked**, got 90 files with connections (cf answer format), but the connections and justification do not always make sense and are mostly positive. Probably report1 does not provide enough context for the AI to determine the inter-influences of targets when they'd be implemented.
		- answer format: 
			- *target_code* (e.g., TA1.9)
			- *target_content* (e.g., The contribution of the sectors covered by the EU ETS with respect to the EU Climate ambition should be of -62 % compared to 2005 (increasing the linear emissions reduction factor from 2.2 % per year up to 4.4 %))
			- *impact_target* (the target code of the target that is likely to be positively or negatively affected by the implementation and requirements of the target in the 'target_code' column)
			- *impact_type* (positive '+' or negative '-')
			- *justification*


4. **150 targets from report1 (target_assessment) + chunks loop + report2 chapters
	- [[2025-03-10]] → [[2025-03-11]] 
	- Keep the chunk strategy but make the following changes: 
		-  [x] based on chiara's feedback, instead of feeding report 1 (which does not tell much about the potential impacts of the implementation of each target), update the targets data to add the 'target_assessment column' from report1, and reduce amount of targets by selecting only the 150 targets mentioned in  report1.
		-  [x] add report2 chapter 3, chapter 4, chapter 2.2, and if possible chapter 5.1 and 6.1, but trim the reference list to shorten the prompt
		-  [x] → done using llama3.3 on [[2025-03-11]] 



5.  **Macro-groups + 288 targets +  chunks loop + report1**
	-  [x] Re-generate .md files from updated 'target_NACE_classification+assessments.xlsx' and add new targets to the canvases (cf list in [[2025-03-11]]).
		- → done manually 
		- → done with LLM (gpt on [[2025-03-13]], and llama3.3 on [[2025-03-14]])
	-  [x] create new dataset with a column 'macro_group' in addition to target_code, target_content etc
	-  [ ] note: can these macro_groups/sub_themes be as reported in report1 'treemap of topics'??
	-  [ ] Re-run the code as in strategy n°3, but instead of feeding all targets, group the targets in 'macro-groups' / 'sub-themes', so that the output table would be less long and also easier to work with with experts. It does require a restructuring of the dataset based on the obsidian canvases I made in december. 

6. **Macro-groups + 150 targets + split loop + report1 assessment + report2 chapters**
	- → [[2025-03-20]]
	Limitations: only considering targets from report1 leaves out certain subthemes (cf [[2025-03-25]])


7. **Macro-groups + 254 targets + split loop + report1 assessment + report2 chapters**
	→ [[2025-03-25]]
	- important realistation → [[2025-03-27]]



8.  Leveling with Verdiana's work
	
	# **A -** **sub-themes network**
	
	
	- [x] wait for report 2 update
	- [ ] re-generate network with:
			- 150 targets from report1 *grouped into sub-themes*
			- assessments
			- updated report 2 chapters
	
	- [ ] clean and review network
	- [ ] split generated data & make survey
	- [ ] send to experts
	- [ ] process results
	- [ ] network analysis verdiana
	
	
	
	# **B - policy documents network
	
	- [x] wait for report 2 update
	- [ ] re-generate network with:
			- 150 targets from report1 *grouped by policy documents*
			- targets  assessments
			- *subset of report 2 chapters* related to the policy documents
	
	- [ ] clean and review network
	- [ ] split generated data & make survey
	- [ ] send to experts
	- [ ] process results
	- [ ] network analysis verdiana


	# **C - all 150 targets
		
	- [x] wait for report 2 update
	- [ ] re-generate network with:
				- 150 targets from report1 *grouped by policy documents*
				- targets  assessments
				- *subset of report 2 chapters* related to the policy documents
		
		- [ ] clean and review network
		- [ ] split generated data & make survey
		- [ ] send to experts
		- [ ] process results
		- [ ] network analysis verdiana
	




**Report_2 modifications**

chapter_1 : kept only the costs of inaction
chapter_2,3,4,5,7 : cut out the bibliographies to save tokens (cf [[2025-04-18]])


# Notes

from [[2025-02-27]] to ................


- [[2025-03-07]]
	- the LLM pipeline seem to work, though slowly, but the connection that are generated between targets and the justifications do not seem to make much sense.
	- Shall I simplify the target dataset that I feed into the pipeline, and group targets by sub-themes within each thematic areas? 
		- → eg, TA2 clean, affordable and secure energy → subdivide into 'macro_targets'/'sub-theme': Energy efficiency (eg buildings), hydrogen, ocean, wind, solar..
		- → simplifying not only would make the network easier to be generated but also easier to work with during  workshops with experts.
		- → each individual target will of course still be accessible and indicated as belonging to a specific sub-group/sub-theme


- [[2025-03-10]] → [[]]  
	- add target assessments from report1 to main initial target dataset:
	- extra targets that I filled in empty target slots: **! ADD THEM ON THE CANVASES !**
	-  - extra targets that I filled in empty target slots: 
		- [x] TA2.41
		- [x] TA2.33
		- [x] TA2.34
		- [x] TA3.38
		- [x] TA3.48
		- [x] TA3.49
		- [x] TA3.50
		- [x] TA3.51
		- [x] TA3.52
		- [x] TA4.18
		- [x] TA4.19
		- [x] TA7.6
		- [x] TA7.8
		- [x] TA7.9
		- [x] TA7.25
		-

same as TA1.16 → TA2.33
same as TA2.29 → TA2.34




