import ROOT
import utils.makemodel 
import shapes
import yields

class main():

      def __init__(self, config): # config: fs, dim, refit

          self.channel = "1"

          self.dim = "1D"

          self.CMS_zz4l_mass = ROOT.RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",105,140)
          self.CMS_zz4l_mass.setBins(700)

          massErrBinning = self.GetBinning("Dm_signal_4mu.root", "h_Dm")
          self.CMS_zz4l_massErr = ROOT.RooRealVar("CMS_zz4l_massErr", "CMS_zz4l_massErr",massErrBinning[1],massErrBinning[2])
          self.CMS_zz4l_massErr.setBins(massErrBinning[0])

          KDBinning = self.GetBinning("Dsignal_4mu.root", "h_mzzD","y")
          self.MELA_KD = ROOT.RooRealVar("MELA_KD","MELA_KD",KDBinning[1],KDBinning[2])
          self.MELA_KD.setBins(KDBinning[0])

          self.categories = ["ggH","qqH","WH","ZH","ttH"]

          w_in = ROOT.RooWorkspace("w_in")
          getattr(w_in,'import')(self.CMS_zz4l_mass)
          getattr(w_in,'import')(self.CMS_zz4l_massErr)
          getattr(w_in,'import')(self.MELA_KD)
          workspaceConfig = {"channel":self.channel, "w_in":w_in, "MH":125}
          self.models = utils.makemodel.MakeModel(workspaceConfig)

          self.w_out = ROOT.RooWorkspace("w_out")

          self.paramShapes = {"DCB": shapes.DCB_parametrization.shape,\
                              "WH_nonRes": shapes.signal_shape_parametrization_13TeV_WH.shape,\
                              "ZH_nonRes": shapes.signal_shape_parametrization_13TeV_ZH.shape,\
                              "qqZZ": shapes.bkg_shape_parametriztion_13TeV_qqZZ.shape,\
                              "ggZZ": shapes.bkg_shape_parametriztion_13TeV_qqZZ.shape } 

#      def buildDatacard(self):

      def BuildWorkspace(self):

          if self.dim == "1D":

             #signal
             doubleCB = ROOT.RooAbsPdf()
             for cat in self.categories:
                 name_dcb = "signalCB_"+cat+"_"+self.channel
                 if cat == "WH" or cat == "ZH":
                    doubleCB_res = models.MakeDoubleCB("dcb_"+cat, self.paramShapes["DCB"], False)
                    #manipulate name of parameter in shape dictionary
                    landaushape = {"mean": (self.paramShapes[cat+"_nonRes"])[cat+"p0"],\
                                   "sigma": (self.paramShapes[cat+"_nonRes"])[cat+"p1"]}
                    #frac
                    frac = (self.paramShapes[cat+"_nonRes"])[cat+"frac"]
                    landau = models.Landau("nonres"+cat, landaushape)
                    doubleCB = ROOT.RooAddPdf(name_dcb, name_dcb, doubleCB_res, landau, frac)
                    getattr(self.w_out,'import')(doubleCB)
                 else:
                    doubleCB = models.MakeDoubleCB(name_dcb, self.paramShapes["DCB"], False)
                    getattr(self.w_out,'import')(doubleCB)

             #irr background
             name_qqzz = "bkg_qqzzTmp_"+self.channel
             bernsteinShape = {"b0": (self.paramShapes["qqZZ"])["chebPol1"],\
                               "b1": (self.paramShapes["qqZZ"])["chebPol2"],\
                               "b2": (self.paramShapes["qqZZ"])["chebPol3"],}
             qqzz = models.MakeBernstein(name_qqzz, bernsteinShape)
             getattr(self.w_out,'import')(qqzz)

             name_ggzz = "bkg_ggzzTmp_"+self.channel
             bernsteinShape = {"b0": (self.paramShapes["ggZZ"])["chebPol1"],\
                               "b1": (self.paramShapes["ggZZ"])["chebPol2"],\
                               "b2": (self.paramShapes["ggZZ"])["chebPol3"],}
             ggzz = models.MakeBernstein(name_ggzz, bernsteinShape)
             getattr(self.w_out,'import')(ggzz)

             #red background
             zjets = models.GetZXShape_4mu_reco()


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

          TempFile = ROOT.TFile(fileame)
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
          for key in shape:
              if "_"+self.channel in key: # "_1", "_2", "_3"
                 shape_out[(key.split("_"))[0]] = shape[key]

          return shape_out

      def LoadYields(self):
