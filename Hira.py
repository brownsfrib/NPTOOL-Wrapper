# ROOT/PyROOT/Python includes
import numpy as np # always uptop fuck you think this is
import ROOT
import sys
import os

# Importing custom NPTOOL "wrapper"
from Detector.Detector import DetectorClass

def RunAnalysis(className, fileName):
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	classType = DetectorClass(className)
	filePath = classType.NPOutputsPath + fileName
	if not (os.path.exists(filePath)):
		message = "\033[1;31mSimulation file " + filePath + " does not exist.\033[0m\n\n"
		raise ValueError(message)

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
		raise ValueError(message)

	InputParser = ROOT.NPL.InputParser(detectorFilePath) # There's some weird namespace fuckery happening here
	Physics.ReadConfiguration(InputParser)
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	# Don't touch anything inbetween the brackets!!!!

	outputFile = ROOT.TFile(fileName, "RECREATE")
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

	sys.stdout.write("\n\033[1;32m")
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

		if (event % 5000) == 0:
			percentage = 100.0*(float(event)/float(tree.GetEntries()))
			message = "Finished with " + str(round(percentage, 2)) + "% of events."
			sys.stdout.write("\r{0}".format(message))
			sys.stdout.flush()

	sys.stdout.write("\rFinshed with 100.0% of events.")
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


def EventAnalysis(physicsClass):
	mult = physicsClass.EventMultiplicity
	return mult


if __name__ == "__main__":
	RunAnalysis("Hira", "test-norot-new.root")





