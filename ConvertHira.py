# ROOT/PyROOT/Python includes
import numpy as np # always uptop fuck you think this is
import ROOT
import sys
import os

# Importing custom NPTOOL "wrapper"
from Detector.Detector import DetectorClass

clearTerminal = lambda: os.system('clear')

def RunAnalysis(className, fileName):
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	classType = DetectorClass(className)
	filePath = classType.NPOutputsPath + fileName
	if not (os.path.exists(filePath)):
		message = "\033[1;31mSimulation file " + filePath + " does not exist.\033[0m\n\n"
		sys.stdout.write(message)
		return
	
	tfile = ROOT.TFile(filePath, "READ")
	tree = tfile.Get("SimulatedTree")
	treeReader = ROOT.TTreeReader(tree)
	dataTypeName = "T" + className + "Data"
	readerClass = ROOT.TTreeReaderValue(dataTypeName)(treeReader, className)

	# This CORRECTLY initializes the physics class
	classNameDynamic = "T" + className + "Physics"
	classCast = getattr(ROOT, classNameDynamic)
	Physics = classCast()

	# We need to create an InputParser and make it read in the detector ASCII file stored in object tree
	detectorAsciiFile = tfile.Get("DetectorConfiguration")
	detectorFilePath = detectorAsciiFile.GetTitle()
	if not (os.path.exists(detectorFilePath)):
		message = "\033[1;31mDetector input file taken from " + filePath + " does not exist.\033[0m\n\n"
		sys.stdout.write(message)
		return

	InputParser = ROOT.NPL.InputParser(detectorFilePath) # There's some weird namespace fuckery happening here
	Physics.ReadConfiguration(InputParser)
	#clearTerminal()
	sys.stdout.write("\n\n")

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	# Don't touch anything inbetween the brackets!!!!

	outputPath = "./outputs/" + fileName
	outputFile = ROOT.TFile(outputPath, "RECREATE")
	outTree = ROOT.TTree("AnalyzedTree", "Testing!")

	mult = ROOT.std.vector('int')(1)
	outTree.Branch("Mult", mult)

	ECsI = ROOT.std.vector('double')()
	outTree.Branch("ECsI", ECsI)

	DSSD = ROOT.std.vector('double')()
	outTree.Branch("DSSD", DSSD)

	Phi = ROOT.std.vector('double')()
	outTree.Branch("Phi", Phi)

	Theta = ROOT.std.vector('double')()
	outTree.Branch("Theta", Theta)

	for event in treeReader:

		mult.clear()
		ECsI.clear()
		DSSD.clear()
		Phi.clear()
		Theta.clear()

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		eventData = readerClass.Get()
		Physics.SetRawDataPointer(eventData)
		Physics.BuildSimplePhysicalEvent()
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		mult.push_back(Physics.EventMultiplicity)

		for i in range(Physics.EventMultiplicity):
			ECsI.push_back(Physics.CsI_E[i])					
			DSSD.push_back(Physics.ThickSi_E[i])

			xStripPos = Physics.GetPositionOfInteraction(i).X()
			yStripPos = Physics.GetPositionOfInteraction(i).Y()
			zStripPos = Physics.GetPositionOfInteraction(i).Z()

			if np.abs(xStripPos) <= 0.0001:
				Phi.push_back(-1000)
			else:
				Phi.push_back(np.arctan2(yStripPos, xStripPos))
			if np.abs(zStripPos) <= 0.0001:
				Theta.push_back(-1000)
			else:
				Theta.push_back(np.arctan2(yStripPos, zStripPos))
			
			if (Physics.CsI_E[i] > 0):
				ECsI.push_back(Physics.CsI_E[i])					
				DSSD.push_back(Physics.ThickSi_E[i])
			else:
				ECsI.push_back(-1000)
				DSSD.push_back(-1000)

	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		outTree.Fill()
		Physics.Clear()

		if (event % (int(0.075*tree.GetEntries()))) == 0:
			percentage = 100.0*(float(event)/float(tree.GetEntries()))
			message = "Finished with \033[1;32m" + str(round(percentage, 2)) + "%\033[0m of events for \033[4;33m" + filePath + "\033[0m"
			sys.stdout.write("\r{0}".format(message))
			sys.stdout.flush()

	writeMessage = "\rFinshed with \033[1;32m100.0%\033[0m of events for \033[4;33m" + filePath + "\033[0m"
	sys.stdout.write("{0}".format(writeMessage))
	sys.stdout.flush()
	sys.stdout.write("\n\033[0m")
	sys.stdout.write("\n")

	outTree.Write()
	outputFile.Write()
	outputFile.Close()
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	return 



def ReadInputFile(inputFilePath):
	fileList = []
	if not (os.path.exists(inputFilePath)):
		message = "\033[1;31mInput file path " + inputFilePath + " does not exist.\n\n\033[0m"
		raise ValueError(message)
	with open(inputFilePath) as openFile:
		lines = openFile.readlines()
		for line in lines:
			curLine = str(line.strip())
			parsedLine = [substr for substr in curLine]
			if (len(parsedLine) == 0):
				pass
			elif (parsedLine[0] == "#"):
				pass
			else:
				# Testing for a .root extension
				extension = os.path.splitext(curLine)[-1]
				if (extension == ".root"):
					fileList.append(curLine)
				else:
					pass

	return fileList

if __name__ == "__main__":
	args = sys.argv
	conversionFiles = []
	argSet = list(set(args))

	if len(argSet) == 1:
		message = "\033[1;31mYou didn't pass in the name of the ROOT file you want to convert.\033[0m\n\n"
		raise ValueError(message)

	else:
		for i in range(1, len(args)):
			extension = os.path.splitext(args[i])[-1]
			if (extension == ".input"):
				textInputFile = ReadInputFile(args[i])
				for j in range(len(textInputFile)):
					conversionFiles.append(textInputFile[j])
			elif (extension == ".root"):
				conversionFiles.append(args[i])
			else:
				pass

		for i in range(len(conversionFiles)):
			RunAnalysis("Hira", conversionFiles[i])






