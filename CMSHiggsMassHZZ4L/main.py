import ROOT

import utils.makemodel 
import utils.makedatacard

import shapes.DCB_parametrization 
import shapes.signal_shape_parametrization_13TeV_WH
import shapes.signal_shape_parametrization_13TeV_ZH
import shapes.bkg_shape_parametriztion_13TeV_qqZZ
import shapes.bkg_shape_parametriztion_13TeV_ggZZ

import yields.signalYields_4mu
import yields.signalYields_4e
import yields.signalYields_2e2mu

import sys

class main():

      def __init__(self, config=0): # config: fs, dim, refit

          self.channel = "1"
          self.dim = "1D"

          self.mH = 125
          self.MH = ROOT.RooRealVar("MH","MH",self.mH)

          #inputs for workspace
          self.CMS_zz4l_mass = ROOT.RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",105,140)
          self.CMS_zz4l_mass.setBins(700)

          massErrBinning = self.GetBinning("shapes/templates2D/Dm_signal_4mu.root", "h_Dm")
          self.CMS_zz4l_massErr = ROOT.RooRealVar("CMS_zz4l_massErr", "CMS_zz4l_massErr",massErrBinning[1],massErrBinning[2])
          self.CMS_zz4l_massErr.setBins(massErrBinning[0])

          KDBinning = self.GetBinning("shapes/templates2D/Dsignal_4mu.root", "h_mzzD","y")
          self.MELA_KD = ROOT.RooRealVar("MELA_KD","MELA_KD",KDBinning[1],KDBinning[2])
          self.MELA_KD.setBins(KDBinning[0])

          self.categories = ["ggH","qqH","WH","ZH","ttH"]

          w_in = ROOT.RooWorkspace("w_in")
          getattr(w_in,'import')(self.CMS_zz4l_mass)
          getattr(w_in,'import')(self.CMS_zz4l_massErr)
          getattr(w_in,'import')(self.MELA_KD)
          self.w_out = ROOT.RooWorkspace("w_out")

          workspaceConfig = {"channel":self.channel, "w_in":w_in, "MH":125, "w_out":self.w_out}
          self.models = utils.makemodel.MakeModel(workspaceConfig)

          self.paramShapes = {"DCB": self.PickShapePerChannel(shapes.DCB_parametrization.shape),\
                              "WH_nonRes": self.PickShapePerChannel(shapes.signal_shape_parametrization_13TeV_WH.shape),\
                              "ZH_nonRes": self.PickShapePerChannel(shapes.signal_shape_parametrization_13TeV_ZH.shape),\
                              "qqZZ": self.PickShapePerChannel(shapes.bkg_shape_parametriztion_13TeV_qqZZ.shape),\
                              "ggZZ": self.PickShapePerChannel(shapes.bkg_shape_parametriztion_13TeV_qqZZ.shape) } 

          self.yields = yields.signalYields_4mu.signalYields_4mu

          #inputs for datacard
          processlist = ["ggH_hzz", "qqH_hzz", "WH_hzz", "ZH_hzz", "ttH_hzz", "bkg_qqzz", "bkg_ggzz", "bkg_zjets"]
          rates = ["1","1","1","1","1",str(22.6892), str(2.48368), str(12.2527)]
          datacardfile =  open("test.txt", "w")
          datacardInputs = {\
                                 "txtfile": datacardfile, \
                                 "nChannel": 1, "nSig": 5, "nBkg": 3,\
                                 "workspaceName": "hzz4l_4muS_13TeV.input.root",
                                 "channelName": "a1",\
                                 "obsEvents": 59,\
                                 "processList": processlist, "rates": rates                                 
                                }

          self.datacard = utils.makedatacard.Makedatacard(datacardInputs)

      def BuildDatacard(self):

          self.datacard.WriteDatacard() 


      def BuildWorkspace(self):

          if self.dim == "1D":

             #signal
             doubleCB = ROOT.RooDoubleCB()
             for cat in self.categories:
                 name_dcb = "signalCB_"+cat+"_"+self.channel
                 if (cat == "WH" or cat == "ZH"):
                    #res WH/ZH
                    self.models.MakeDoubleCB(cat+"_res", self.paramShapes["DCB"], False)
                    #manipulate name of parameter in shape dictionary
                    landaushape = {"mean": (self.paramShapes[cat+"_nonRes"])[cat+"p0"],\
                                   "sigma": (self.paramShapes[cat+"_nonRes"])[cat+"p1"]}
                    #frac
                    frac = (self.paramShapes[cat+"_nonRes"])[cat+"frac"]
                    rv_frac = ROOT.RooRealVar(cat+"_frac_"+self.channel,"",float(frac) )
                    #nonRes WH/ZH
                    self.models.MakeLandau(cat+"_nonRes", landaushape)
                    doubleCB = ROOT.RooAddPdf(name_dcb, name_dcb, self.w_out.pdf(cat+"_res"), self.w_out.pdf(cat+"_nonRes"), rv_frac)
                    getattr(self.w_out,'import')(doubleCB)
                 else:
                    self.models.MakeDoubleCB(name_dcb, self.paramShapes["DCB"], False)
#                    getattr(self.w_out,'import')(doubleCB)

             #irr background
             name_qqzz = "bkg_qqzzTmp_"+self.channel
             bernsteinShape = {"b0": (self.paramShapes["qqZZ"])["chebPol1"],\
                               "b1": (self.paramShapes["qqZZ"])["chebPol2"],\
                               "b2": (self.paramShapes["qqZZ"])["chebPol3"],}
             qqzz = self.models.MakeBernstein(name_qqzz, bernsteinShape)
#             getattr(self.w_out,'import')(qqzz)

             name_ggzz = "bkg_ggzzTmp_"+self.channel
             bernsteinShape = {"b0": (self.paramShapes["ggZZ"])["chebPol1"],\
                               "b1": (self.paramShapes["ggZZ"])["chebPol2"],\
                               "b2": (self.paramShapes["ggZZ"])["chebPol3"],}
             ggzz = self.models.MakeBernstein(name_ggzz, bernsteinShape)
#             getattr(self.w_out,'import')(ggzz)

             #red background
             zjets = self.models.GetZXShape_4mu_reco()


          '''
          if dim == 2:

             get err*3
             MakeDoubleDCB(self, name, doubleCBShape, includeErr)
             MakeLandau * 2
             MakeBernstein(self, name, bernsteinShape) * 2
             ZJets
             GetSignal + GetBackground yields

             qqzz,ggzz,zjets * err

          if dim == 3:

             get err*3
             get kd*3
             manipulate kd
             MakeDoubleDCB(self, name, doubleCBShape, includeErr)
             MakeLandau * 2
             MakeBernstein(self, name, bernsteinShape) * 2
             ZJets
             GetSignal + GetBackground yields

             qqzz,ggzz,zjets * err
          '''
      

      def GetBinning(self, filename, templatename, axis="x"):  

          TempFile = ROOT.TFile(filename)
          Template = TempFile.Get(templatename)
          Bins,Low,High = 0, 0, 0

          if axis == "y":
             Bins = Template.GetYaxis().GetNbins()
             Low = Template.GetYaxis().GetXmin()
             High = Template.GetYaxis().GetXmax()
          else:
             Bins = Template.GetXaxis().GetNbins()
             Low = Template.GetXaxis().GetXmin()
             High = Template.GetXaxis().GetXmax()

          binning = [Bins, Low, High]

          return binning


      def PickShapePerChannel(self, shape_in):
  
          shape_out = {}
          for key in shape_in:
              if "_"+self.channel in key: # "_1", "_2", "_3"
                 shape_out[(key.split("_"))[0]] = shape_in[key]

          return shape_out

      def LoadYields(self):

          rfvSigRate_ggH = ROOT.RooFormulaVar("ggH_hzz_norm", (self.yields)["ggH"], ROOT.RooArgList(self.MH))
          rfvSigRate_VBF = ROOT.RooFormulaVar("qqH_hzz_norm",(self.yields)["VBF"], ROOT.RooArgList(self.MH))
#          rfvSigRate_WH = ROOT.RooFormulaVar("WH_hzz_norm", (self.yields)["WH_lep"]+"+"+(self.yields)["WH_had"], ROOT.RooArgList(self.MH))
#          rfvSigRate_ZH = ROOT.RooFormulaVar("ZH_hzz_norm", (self.yields)["ZH_lep"]+"+"+(self.yields)["ZH_had"], ROOT.RooArgList(self.MH))
          rfvSigRate_WH = ROOT.RooFormulaVar("WH_hzz_norm", (self.yields)["WH_lep"], ROOT.RooArgList(self.MH))
          rfvSigRate_ZH = ROOT.RooFormulaVar("ZH_hzz_norm", (self.yields)["ZH_lep"], ROOT.RooArgList(self.MH))
          rfvSigRate_ttH = ROOT.RooFormulaVar("ttH_hzz_norm", (self.yields)["ttH"], ROOT.RooArgList(self.MH))

          getattr(self.w_out,'import')(rfvSigRate_ggH, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_VBF, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_WH, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_ZH, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_ttH, ROOT.RooFit.RecycleConflictNodes())




test = main()
test.BuildWorkspace()
test.LoadYields()
test.w_out.Print()
test.BuildDatacard()
