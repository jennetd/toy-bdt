// Adapted from https://root.cern.ch/doc/v610/TMVAClassificationApplication_8C.html
// by Jennet Dickinson
// January 13, 2020

#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
using namespace TMVA;
void TMVAClassificationApplication( TString myMethodList = "" )
{
  //---------------------------------------------------------------
  // This loads the library
  TMVA::Tools::Instance();
  // Default MVA methods to be trained + tested
  std::map<std::string,int> Use;

  // Boosted Decision Trees
  Use["BDT"]             = 0; // uses Adaptive Boost
  Use["BDTG"]            = 1; // uses Gradient Boost
  Use["BDTB"]            = 0; // uses Bagging
  Use["BDTD"]            = 0; // decorrelation + Adaptive Boost
  Use["BDTF"]            = 0; // allow usage of fisher discriminant for node splitting

  std::cout << std::endl;
  std::cout << "==> Start TMVAClassificationApplication" << std::endl;
  // Select methods (don't look at this code - not of interest)
  if (myMethodList != "") {
    for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;
    std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
    for (UInt_t i=0; i<mlist.size(); i++) {
      std::string regMethod(mlist[i]);
      if (Use.find(regMethod) == Use.end()) {
	std::cout << "Method \"" << regMethod
		  << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
	for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
	  std::cout << it->first << " ";
	}
	std::cout << std::endl;
	return;
      }
      Use[regMethod] = 1;
    }
  }
  // --------------------------------------------------------------------------------------------------
  // Create the Reader object
  TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );
  // Create a set of variables and declare them to the reader
  // - the variable names MUST corresponds in name and type to those given in the weight file(s) used
  Float_t var1, var2;
  reader->AddVariable( "x", &var1 );
  reader->AddVariable( "y", &var2 );

  // Book the MVA methods
  TString dir    = "dataset/weights/";
  TString prefix = "TMVAClassification";
  // Book method(s)
  for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
    if (it->second) {
      TString methodName = TString(it->first) + TString(" method");
      TString weightfile = dir + prefix + TString("_") + TString(it->first) + TString(".weights.xml");
      reader->BookMVA( methodName, weightfile );
    }
  }
  // Book output histograms
  UInt_t nbin = 100;
  TH1F *histBdtG(0);

  if (Use["BDTG"])          histBdtG    = new TH1F( "MVA_BDTG",          "MVA_BDTG",          nbin, -1.0, 1.0 );

  // Prepare input tree (this must be replaced by your data source)
  // in this example, there is a toy tree with signal and one with background events
  // we'll later on use only the "signal" events for the test in this example.
  //
  TFile *input(0);
  TString fname = "test.root";
  if (!gSystem->AccessPathName( fname )) {
    input = TFile::Open( fname ); // check if file in local directory exists
  }
  else {
    TFile::SetCacheFileDir(".");
    input = TFile::Open("http://root.cern.ch/files/tmva_class_example.root", "CACHEREAD"); // if not: download from ROOT server
  }
  if (!input) {
    std::cout << "ERROR: could not open data file" << std::endl;
    exit(1);
  }
  std::cout << "--- TMVAClassificationApp    : Using input file: " << input->GetName() << std::endl;
  // Event loop
  // Prepare the event tree
  // - Here the variable names have to corresponds to your tree
  // - You can use the same variables as above which is slightly faster,
  //   but of course you can use different ones and copy the values inside the event loop
  //
  TFile *target  = new TFile( "TMVApp.root","RECREATE" );
  TTree* output = new TTree("output","output");
  double x, y, score;
  output->Branch("x",&x);
  output->Branch("y",&y);
  output->Branch("score",&score);
  
  std::cout << "--- Select signal sample" << std::endl;
  TTree* theTree = (TTree*)input->Get("sig");
  theTree->SetBranchAddress( "x", &var1 );
  theTree->SetBranchAddress( "y", &var2 );

  std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
  TStopwatch sw;
  sw.Start();
  for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {
    if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
    theTree->GetEntry(ievt);

    x = var1;
    y = var2;
    
    if (Use["BDTG"         ]){
      score = reader->EvaluateMVA( "BDTG method" );
      histBdtG   ->Fill( score );
      output->Fill();
    }
  }
  // Get elapsed time
  sw.Stop();
  std::cout << "--- End of event loop: "; sw.Print();

  std::cout << "--- Select background sample" << std::endl;
  TTree* theTree2 = (TTree*)input->Get("bkg");
  theTree2->SetBranchAddress( "x", &var1 );
  theTree2->SetBranchAddress( "y", &var2 );

  std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
  TStopwatch sw2;
  sw2.Start();
  for (Long64_t ievt=0; ievt<theTree2->GetEntries();ievt++) {
    if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
    theTree2->GetEntry(ievt);

    x =var1;
    y =var2;

    if (Use["BDTG"         ]){
      score = reader->EvaluateMVA( "BDTG method" );
      histBdtG   ->Fill( score );
      output->Fill();
    }
  }
  // Get elapsed time
  sw2.Stop();
  std::cout << "--- End of event loop: "; sw.Print();
  
  // Write histograms
  if (Use["BDTG"         ]){
    histBdtG->Write();
    output->Write();
  }
  target->Close();
  std::cout << "--- Created root file: \"TMVApp.root\" containing the MVA output histograms" << std::endl;
  delete reader;
  std::cout << "==> TMVAClassificationApplication is done!" << std::endl << std::endl;
}
int main( int argc, char** argv )
{
  TString methodList;
  for (int i=1; i<argc; i++) {
    TString regMethod(argv[i]);
    if(regMethod=="-b" || regMethod=="--batch") continue;
    if (!methodList.IsNull()) methodList += TString(",");
    methodList += regMethod;
  }
  TMVAClassificationApplication(methodList);
  return 0;
}
