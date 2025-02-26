COMP 383 COMP BIO PYTHON PIPELINE PROJECT
1. Background
- The purpose of the project is to automate the execution of the software tools. These being mainly in the form of bowtie2 and piepline analysis.
2. Steps taken
- To begin we downloaded the sequences of our two donors. These being SRR5660030 and SRR5660033, which we did through the wget function in our terminal and used the SRA Normalized links.
	- The links to the websites where we got the links from are...
		- https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR5660033&display=data-access
		- https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR5660030&display=data-access 
- After downloading both of these donor sequences we performed a fasterq-dump of both donors to be turned into FASTQ format for future comparison use in the python script. 
3. Dependencies
- The required dependencies are os, SeqIO, Spades, Bowtie2, datasets, and BLAST+.
4. Running the Python Wrapper
- To run the wrapper first you will want to make a clone of 'myrepo' though "git clone https://github.com/BDal783/myrepo.git".
- After cloning the repo, you will want to make sure to cd into it and run the file 'PipelineProject_Brendon_Dal.py' without changing to your dedicated terminal. (one way if on visual studio is to run it by using the drop down next to the play button and clicking run python file)
- The output should add on to the PipelineProject.log file (if opened before running the py file make sure to refresh it)
