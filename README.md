# Wrapper for converting NPTool Simulation Files to a 'Pythonic' Output
If you're uncomfortable with C++ and need to use NPTool, this let's you convert the simulation outputs from NPTool into a PyROOT styled output.
For the following example notes, I will assume an existing detector package exists. \
I will be using the HiRA detector as an example. \

1. Run a simulation using NPTool (check the nptool documentation for this) 
2. Using the template (in this repository called "ConvertHira.py"), update the part of the code following the data structure of your detector found in NPLib to fit your analysis.
	- This will require knowledge of your NPTool detector library, and sometimes this is not trivial. You'll need to at least know how to read C++ code.
3. Update the output TTree and corresponding for loop in the template code ("ConvertHira.py") to fit your analysis needs.

Once the conversion file ("ConvertHira.py") is updated, you can run the script in a few ways. \
First, in the **NPTOOL-Wrapper** directory, make a directory named "outputs" by typing: \
``` console
	mkdir outputs
```
Next, let's assume you have a simulation file named "simulation-test.root" located in your NPTool Outputs/Simulation directory. \
To convert the file, you can call
```console 
	python ConvertHira.py simulation-test.root
```
If you have multiple files ("simulation-test.root", "another-file.root", etc), you can call these files in one go: \
```console
	python ConvertHira.py simulation-test.root another-file.root
```
Alternatively, you can create an input text file ending with **.input** (for example, "hiraInput.input") and populate it with the names of each file you want to process.\
From here, you can call
```console
	python ConvertHira.py hiraInput.input
```
or if you wish to mix an input file with other **.root** files, you can call
```console 
	python ConverHira.py simulation-test.root hiraInput.input another-file.root
```
Only the set (unique file names ending with **.root**) will be processed by the conversion script. \
If the file does not exist in your NPTool Outputs/Simulation directory, the file will not be found. \
You can change this path at your leisue in the conversion code. \
**Have fun** :slightly_smiling_face:


