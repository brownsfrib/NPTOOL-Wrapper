import ROOT
import os
import sys

def PlotdEE(fileName):
	
	tFile = ROOT.TFile(fileName, "READ")
	if not (os.path.exists(fileName)):
		message = "\033[1;31mFile " + fileName + "does not exist.\n\n\033[0m"
		raise ValueError(message)

	bins = 200
	hist = ROOT.TH2D("hist", "HiRA Test; E (MeV); dE (MeV)", bins, 0.0, 200.0, bins, 0.0, 20.0)

	tree = tFile.Get("AnalyzedTree")
	treeReader = ROOT.TTreeReader(tree)
	
	readerMult = ROOT.TTreeReaderValue('vector<int>')(treeReader, "Mult")
	readerE = ROOT.TTreeReaderValue('vector<double>')(treeReader, "ECsI")
	readerdE = ROOT.TTreeReaderValue('vector<double>')(treeReader, "DSSD")
	
	#for entry in treeReader:
	while treeReader.Next():
		mult = readerMult.Get()[0]
		CsIE = readerE.Get()
		DSSD = readerdE.Get()
		for i in range(mult):
			hist.Fill(CsIE[i], DSSD[i])
	
	can = ROOT.TCanvas()
	hist.Draw("colz")
	input() # This exists to keep the histogram graphics up and running
	return

if __name__ == "__main__":
	PlotdEE("./../outputs/test-norot-new.root")
	
