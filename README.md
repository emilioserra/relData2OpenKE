 # relData2OpenKE
 
Scripts to translate Knowledge bases in relData format into OpenKE format.
See these projects in:

 - https://github.com/phohenecker/rel-data#data-format
  
 -  https://github.com/thunlp/OpenKE

relData2OpenKE.py allows to specify the folder where the KB in rel-data format is stored and the outputPath, also the partitions for training/validation/testing which are created based only on infereable data.

The output includes the OpenKE files:

 - Entity2id
 - Relation2id
- Train2id
- Valid2id
- Test2id

relData2OpenKE basically:
- uses sample2EntitiesAndTriples.py, to deal with each sample of rel-data format, e.g. 5000.individuals, 5000.classes…
- objects of sample2EntitiesAndTriples for all samples are used to generate aux files that, among others,
	-  consider class belonging as another simple relation,
	- consider global identifiers for entities/relations/classes.
- uses iDManager.py  to map entity/classes names to new IDs avoding repetitions 
	- relData gives different identifiers to the same individuals/classes
- and generate the final OpenKE files.
