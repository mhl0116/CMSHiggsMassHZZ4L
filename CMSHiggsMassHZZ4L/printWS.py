#!/usr/bin/env python

import sys, re


def usage():
    print  >> sys.stderr,"""

    usage: printWS.py inputFile 

    """
    sys.exit(1)

#----------------------------------------------------------------------

def findWorkspace(rootFile):
    """ searches for a toplevel RooWorkspace instance in the given TFile """

    import ROOT

    retval = None

    for key in rootFile.GetListOfKeys():
        name = key.GetName()

        obj = rootFile.Get(name)

        if isinstance(obj,ROOT.RooWorkspace):
	    print obj.GetName()
            if retval == None:
                retval = obj
            else:
                print >> sys.stderr,"more than one instance of RooWorkspace found in file",rootFile
                sys.exit(1)

    if retval == None:
        print >> sys.stderr,"no RooWorkspace found in file",rootFile
        sys.exit(1)

    return retval    

#----------------------------------------------------------------------
# main
#----------------------------------------------------------------------

ARGV = sys.argv[1:]

if len(ARGV) != 1:
    usage()

inputFname = ARGV.pop(0)


#----------

import ROOT ; gcs = []
#ROOT.gSystem.Load("$CMSSW_BASE/lib/${SCRAM_ARCH}/libHiggsAnalysisCombinedLimit.so")
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

# suppress RooFit's INFO messages
# (see e.g. http://root.cern.ch/phpBB3/viewtopic.php?f=15&t=15024 )
ROOT.gErrorIgnoreLevel = ROOT.kWarning
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)


fin = ROOT.TFile(inputFname)
#assert fin.IsOpen()

ws = findWorkspace(fin)

ws.Print()
