CXX=g++
CC=gcc
CFLAGS=-O2 -Wall
LDFLAGS=-Llib
PRFFLAGS=-lProof
THRDFLAGS=-lThread
INS=-I$(ROOTSYS)/include
INS2=-I$(ROOFITSYS)/include
INS3=-I$(ROOSTATSYS)/include
INSS=-I./include
INSSS=-I.

LD1=-L$(ROOFITSYS)/lib

CFLAGS += `root-config --cflags`
LIBS += `root-config --ldflags --glibs`
LIBS += -L$(ROOFITSYS)/lib -lRooFit -lRooFitCore -lRooStats
#LDFLAGS=`root-config –-ldflags –glibs` -lRooFit –lRooFitCore -lMinuit

LDa=-lRooFitCore
LDb=-lRooFit

OBJ1=TreeSlim_Sig.o
OBJ2=TreeSlim_Bkg.o
OBJ3=Template_Sig.o

.PHONY: clean all main test

all: TreeSlim_Sig TreeSlim_Bkg Template_Sig

TreeSlim_Sig: TreeSlim_Sig.o
	$(CXX) -o TreeSlim_Sig.exe $(OBJ1) $(LIBS)

TreeSlim_Bkg: TreeSlim_Bkg.o
	$(CXX) -o TreeSlim_Bkg.cc.exe $(OBJ2) $(LIBS)

Template_Sig: Template_Sig.o
	$(CXX) -o Template_Sig.exe $(OBJ3) $(LIBS)


clean:
	@rm *.o *.exe

##############RULES##############
.cc.o:
	$(CXX) $(CFLAGS) $(INS) $(INS2) $(INS3) $(INSS) ${INSSS} -c $<
.cpp.o:
	$(CXX) $(CFLAGS) $(INS) -c $<

