import ROOT
import sys
import os


class DetectorClass:
	def __init__(self, detectorName="Hira"):
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		# PUT IN A CONDITIONAL TO CHECK AND SEE IF THE DETECTOR EXISTS
		self.detectorName = detectorName
		# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

		nptoolLibPath, nptoolOutputsPath = self.ParsePath()
		if (nptoolLibPath == "") or (nptoolOutputsPath == ""):
			message = "\033[1;31mYou haven't sourced the NPTOOL bash script properly.\033[0m"
			raise ValueError(message)
		self.NPLibPath = nptoolLibPath
		self.NPOutputsPath = nptoolOutputsPath

		# Initialzing Detector class from user's NPTOOL directory
		self.incPath = self.NPLibPath + "/include/"
		if (self.incPath == "/include/"):
			message = "\033[1;31mFailed to load the include path {0} for your nptool environment.\n\033[0m".format(self.libPath)
			raise ValueError(message)
		ROOT.gInterpreter.AddIncludePath(self.incPath)
		detInclude = self.NPLibPath + "/Detectors/" + self.detectorName
		ROOT.gInterpreter.AddIncludePath(detInclude)

		self.libPath = self.NPLibPath + "/lib/libNP" + self.detectorName + ".so" 
		if (os.path.isfile(self.incPath) == 1): # shared object does not exist
			message = "\033[1;31mYour NPTOOL is fucked up, the file {0} doesn't exist.\n\033[0m".format(self.incPath)
			raise ValueError(message)
		ROOT.gSystem.Load(self.libPath)
		corePath = self.NPLibPath + "/lib/libNPCore.so"
		ROOT.gSystem.Load(corePath)

		detectorDataPath = self.incPath + "/T" + self.detectorName + "Data.h"
		ROOT.gInterpreter.AddIncludePath(detectorDataPath)
		detectorPhysicsPath = self.incPath + "/T" + self.detectorName + "Physics.h"
		ROOT.gInterpreter.AddIncludePath(detectorPhysicsPath)

		return



	def ParsePath(self):
		NPLibPath = ""
		NPOutputsPath = ""
		pathVars = ROOT.gSystem.Getenv("PATH")
		if (pathVars == ""):
			message = "\033[1;31mOk something is SERIOUSLY wrong with what you've done, you aint even got a path. How'd you manage that? Go fix it lol like restart your shell dumbass.\033[0m"
			raise ValueError(message)
		parsedPath = pathVars.split(":")
		for i in range(len(parsedPath)):
			splitString = parsedPath[i].split("/")
			for j in range(len(splitString)):
				if (splitString[j] == "NPLib"):
					NPLibPath = parsedPath[i].split("/bin")[0]
					NPOutputsPath = parsedPath[i].split("NPLib/bin")[0] + "Outputs/Simulation/"

		return NPLibPath, NPOutputsPath






