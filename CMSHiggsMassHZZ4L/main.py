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
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")

class main():

      def __init__(self, config=0): # config: fs, dim, refit ##### move ALL hardcoded number into config

          self.lumi = 35.8671
          self.datatreename = "data_obs"

          self.channel = "1"
          self.dim = "1D"

          self.mH = 125
          self.MH = ROOT.RooRealVar("MH","MH",self.mH)

          #intermediate workspace to save all models (intermediate and final models)
          self.w_out = ROOT.RooWorkspace("w")

          #inputs for workspace
          ## observables
          ### m4l
          self.CMS_zz4l_mass = ROOT.RooRealVar("CMS_zz4l_mass","CMS_zz4l_mass",105,140)
          self.CMS_zz4l_mass.setBins(700)
          ### m4lErr/m4l
          massErrBinning = self.GetBinning("shapes/templates2D/Dm_signal_4mu.root", "h_Dm")
          self.CMS_zz4l_massErr = ROOT.RooRealVar("CMS_zz4l_massErr", "CMS_zz4l_massErr",massErrBinning[1],massErrBinning[2])
          self.CMS_zz4l_massErr.setBins(massErrBinning[0])
          ### D_bkg^kin (ME-based kinematic discriminat)
          KDBinning = self.GetBinning("shapes/templates2D/Dsignal_4mu.root", "h_mzzD","y")
          self.MELA_KD = ROOT.RooRealVar("MELA_KD","MELA_KD",KDBinning[1],KDBinning[2])
          self.MELA_KD.setBins(KDBinning[0])
          ### load observables into w_in for model building
          ### 1D(m4l), 2D(m4l, m4lErr/m4l), 3D(m4l, m4l/m4lErr, KD)
          w_in = ROOT.RooWorkspace("w_in")
          getattr(w_in,'import')(self.CMS_zz4l_mass)
          getattr(w_in,'import')(self.CMS_zz4l_massErr)
          getattr(w_in,'import')(self.MELA_KD)

          ## production modes
          self.categories = ["ggH","qqH","WH","ZH","ttH"]

          ## create "MakeModel" class to build models
          workspaceConfig = {"channel":self.channel, "w_in":w_in, "MH":125, "w_out":self.w_out}
          self.models = utils.makemodel.MakeModel(workspaceConfig)

          ## prepare input shapes (m4l,m4lErr/m4l,KD) to build models
          self.PrepareShapesToBuildModel()

          ## yields for signal and background
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

          self.LoadYields()
          self.LoadData()

          if self.dim == "1D": self.BuildModels_1D()
          if self.dim == "2D": self.BuildModels_2D()
          if self.dim == "3D": self.BuildModels_3D()


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
          rfvSigRate_WH = ROOT.RooFormulaVar("WH_hzz_norm", (self.yields)["WH_lep"]+"+"+(self.yields)["WH_had"], ROOT.RooArgList(self.MH))
          rfvSigRate_ZH = ROOT.RooFormulaVar("ZH_hzz_norm", (self.yields)["ZH_lep"]+"+"+(self.yields)["ZH_had"], ROOT.RooArgList(self.MH))
          rfvSigRate_ttH = ROOT.RooFormulaVar("ttH_hzz_norm", (self.yields)["ttH"], ROOT.RooArgList(self.MH))

          getattr(self.w_out,'import')(rfvSigRate_ggH, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_VBF, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_WH, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_ZH, ROOT.RooFit.RecycleConflictNodes())
          getattr(self.w_out,'import')(rfvSigRate_ttH, ROOT.RooFit.RecycleConflictNodes())


      def LoadData(self):

          datafiledict = {"1":"hzz4mu_"+str(self.lumi)+".root",\
                          "2":"hzz4e_"+str(self.lumi)+".root",\
                          "3":"hzz2e2mu_"+str(self.lumi)+".root"}

          datafilename = "data/" + datafiledict[self.channel]
          datafile = ROOT.TFile(datafilename)
          datatree = datafile.Get(self.datatreename)
          data_obs = ROOT.RooDataSet()
          if self.dim == "1D":
             data_obs = ROOT.RooDataSet("data_obs","data_obs",datatree,ROOT.RooArgSet(self.CMS_zz4l_mass))
          if self.dim == "2D":
             data_obs = ROOT.RooDataSet("data_obs","data_obs",datatree,ROOT.RooArgSet(self.CMS_zz4l_mass,self.CMS_zz4l_massErr))
          if self.dim == "3D":
             data_obs = ROOT.RooDataSet("data_obs","data_obs",datatree,ROOT.RooArgSet(self.CMS_zz4l_mass,self.CMS_zz4l_massErr,self.MELA_KD))
        
          getattr(self.w_out,'import')(data_obs)#, ROOT.RooFit.RecycleConflictNodes())

  
      def BuildModels_1D(self):

          #signal
          doubleCB = ROOT.RooDoubleCB()
          for cat in self.categories:
              name_dcb = cat+"_hzz"
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
                 getattr(self.w_out,'import')(doubleCB,ROOT.RooFit.RecycleConflictNodes())
              else:
                 self.models.MakeDoubleCB(name_dcb, self.paramShapes["DCB"], False)

          #irr background
          name_qqzz = "bkg_qqzz"
          bernsteinShape = {"b0": (self.paramShapes["qqZZ"])["chebPol1"],\
                            "b1": (self.paramShapes["qqZZ"])["chebPol2"],\
                            "b2": (self.paramShapes["qqZZ"])["chebPol3"],}
          qqzz = self.models.MakeBernstein(name_qqzz, bernsteinShape)

          name_ggzz = "bkg_ggzz"
          bernsteinShape = {"b0": (self.paramShapes["ggZZ"])["chebPol1"],\
                            "b1": (self.paramShapes["ggZZ"])["chebPol2"],\
                            "b2": (self.paramShapes["ggZZ"])["chebPol3"],}
          ggzz = self.models.MakeBernstein(name_ggzz, bernsteinShape)

          #red background
          zjets = self.models.GetZXShape_4mu_reco()


      def BuildModels_2D(self):

          #signal
          doubleCB = ROOT.RooDoubleCB()
          for cat in self.categories:
              name_dcb = cat+"_hzz_1D"
              if (cat == "WH" or cat == "ZH"):
                 #res WH/ZH
                 self.models.MakeDoubleCB(cat+"_res", self.paramShapes["DCB"], True)
                 #manipulate name of parameter in shape dictionary
                 landaushape = {"mean": (self.paramShapes[cat+"_nonRes"])[cat+"p0"],\
                                "sigma": (self.paramShapes[cat+"_nonRes"])[cat+"p1"]}
                 #frac
                 frac = (self.paramShapes[cat+"_nonRes"])[cat+"frac"]
                 rv_frac = ROOT.RooRealVar(cat+"_frac_"+self.channel,"",float(frac) )
                 #nonRes WH/ZH
                 self.models.MakeLandau(cat+"_nonRes", landaushape)
                 doubleCB = ROOT.RooAddPdf(name_dcb, name_dcb, self.w_out.pdf(cat+"_res"), self.w_out.pdf(cat+"_nonRes"), rv_frac)
                 getattr(self.w_out,'import')(doubleCB,ROOT.RooFit.RecycleConflictNodes())
              else:
                 self.models.MakeDoubleCB(name_dcb, self.paramShapes["DCB"], True)

          #irreducible background
          name_qqzz = "bkg_qqzz_1D"
          bernsteinShape = {"b0": (self.paramShapes["qqZZ"])["chebPol1"],\
                            "b1": (self.paramShapes["qqZZ"])["chebPol2"],\
                            "b2": (self.paramShapes["qqZZ"])["chebPol3"],}
          qqzz = self.models.MakeBernstein(name_qqzz, bernsteinShape)

          name_ggzz = "bkg_ggzz_1D"
          bernsteinShape = {"b0": (self.paramShapes["ggZZ"])["chebPol1"],\
                            "b1": (self.paramShapes["ggZZ"])["chebPol2"],\
                            "b2": (self.paramShapes["ggZZ"])["chebPol3"],}
          ggzz = self.models.MakeBernstein(name_ggzz, bernsteinShape)

          #reducible background
          zjets = self.models.GetZXShape_4mu_reco()
          ## treatmeant of zjets m4l shape can be improved
          self.w_out.pdf("bkg_zjets").SetName("bkg_zjets_1D")

          ## build 2D (m4l, m4lErr/m4l) model
          for cat in self.categories:
              self.models.MakeConditionalProd(cat+"_hzz", w_out.pdf("pdfErr_s"), w_out.pdf(cat+"_hzz_1D"), self.CMS_zz4l_mass)
          self.models.MakeConditionalProd("bkg_qqzz", w_out.pdf("pdfErr_qqzz"), w_out.pdf("bkg_qqzz_1D"), self.CMS_zz4l_mass) 
          self.models.MakeConditionalProd("bkg_ggzz", w_out.pdf("pdfErr_ggzz"), w_out.pdf("bkg_ggzz_1D"), self.CMS_zz4l_mass)
          self.models.MakeConditionalProd("bkg_zjets", w_out.pdf("pdfErr_zjets"), w_out.pdf("bkg_zjets_1D"), self.CMS_zz4l_mass)


      def BuildModels_3D(self):

          #assume 2D(m4l, m4lErr/m4l) model is already made
          ## signal
          for cat in self.categories:
              self.w_out.pdf(cat+"_hzz").SetName(cat+"_hzz_2D")
              sigTemplateMorphPdf = ROOT.FastVerticalInterpHistPdf2D("sigTemplateMorphPdf_"+cat,"",self.CMS_zz4l_mass,self.MELA_KD,\
                                                                     true, ROOT.RooArgList(self.w_out.pdf("sigTemplatePdf")), ROOT.RooArgList(),1.0,1)

              sigCB3d = ROOT.RooProdPdf(cat+"_hzz","", ROOT.RooArgSet(self.w_out.pdf(cat+"_hzz_2D")),\
                                        ROOT.RooFit.Conditional(ROOT.RooArgSet(sigTemplateMorphPdf),ROOT.RooArgSet(self.MELA_KD) ) )

              getattr(self.w_out,'import')(sigCB3d,ROOT.RooFit.RecycleConflictNodes())

          ## qqzz and ggzz
          for cat in ["qqzz","ggzz"]:
              self.w_out.pdf("bkg_"+cat).SetName("bkg_"+cat+"_2D")
              bkgTemplateMorphPdf_zz = ROOT.FastVerticalInterpHistPdf2D("bkgTemplatMorphPdf_"+cat,"",self.CMS_zz4l_mass,self.MELA_KD,\
                                                                        true,ROOT.RooArgList(self.w_out.pdf("bkgTemplatePdf_"+cat)),ROOT.RooArgList(),1.0,1)

          bkg3d_zz = ROOT.RooProdPdf("bkg_"+cat,"",ROOT.RooArgSet(ROOT.RooArgSet(self.w_out.pdf("bkg_"+cat+"_2D")),\
                                       ROOT.RooFit.Conditional(ROOT.RooArgSet(bkgTemplateMorphPdf_zz),ROOT.RooArgSet(self.MELA_KD) ) )

          getattr(self.w_out,'import')(bkg3d_zz,ROOT.RooFit.RecycleConflictNodes())

          ## zjets
          self.w_out.pdf("bkg_zjets").SetName("bkg_zjets_2D")

          funcList_zjets = ROOT.RooArgList()
          morphBkgVarName = "CMS_zz4l_bkgMELA"
          alphaMorphBkg = ROOT.RooRealVar(morphBkgVarName,morphBkgVarName,0,-20,20)
          morphVarListBkg = ROOT.RooArgList()

          funcList_zjets.add(self.w_out.pdf("bkgTemplatePdf_ZX"))
          funcList_zjets.add(self.w_out.pdf("bkgTemplatePdf_ZX_up"))
          funcList_zjets.add(self.w_out.pdf("bkgTemplatePdf_ZX_dn"))
          alphaMorphBkg.setConstant(False)
          morphVarListBkg.add(alphaMorphBkg)
          bkgTemplateMorphPdf_zjets = ROOT.FastVerticalInterpHistPdf2D("bkgTemplatMorphPdf_ZX","",self.CMS_zz4l_mass,self.MELA_KD,\
                                                                       true,funcList_zjets,morphVarListBkg,1.0,1)
          bkg3d_zjets = ROOT.RooProdPdf("bkg_zjets","",ROOT.RooArgSet(self.w_out.pdf("bkg_zjets_2D")),\
                                        ROOT.RooFit.Conditional(ROOT.RooArgSet(bkgTemplateMorphPdf_zjets),ROOT.RooArgSet(self.MELA_KD) ) )

          

      def PrepareShapesToBuildModel(self):

          ## 1D model parameters
          self.paramShapes = \
          {\
          "DCB": self.PickShapePerChannel(shapes.DCB_parametrization.shape),\
          "WH_nonRes": self.PickShapePerChannel(shapes.signal_shape_parametrization_13TeV_WH.shape),\
          "ZH_nonRes": self.PickShapePerChannel(shapes.signal_shape_parametrization_13TeV_ZH.shape),\
          "qqZZ": self.PickShapePerChannel(shapes.bkg_shape_parametriztion_13TeV_qqZZ.shape),\
          "ggZZ": self.PickShapePerChannel(shapes.bkg_shape_parametriztion_13TeV_ggZZ.shape) \
           }

          ## m4lErr/m4l template for 2D(m4l, m4lErr/m4l) model building
          self.models.HistTemplateToPdf("shapes/templates2D/Dm_signal_4mu.root", "d_Dm", "pdfErr_s", \
                                        ROOT.RooArgList(self.CMS_zz4l_massErr), ROOT.RooArgSet(self.CMS_zz4l_massErr)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dm_qqZZ_4mu.root", "d_Dm", "pdfErr_qqzz", \
                                        ROOT.RooArgList(self.CMS_zz4l_massErr), ROOT.RooArgSet(self.CMS_zz4l_massErr)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dm_ggZZ_4mu.root", "d_Dm", "pdfErrS_ggzz", \
                                        ROOT.RooArgList(self.CMS_zz4l_massErr), ROOT.RooArgSet(self.CMS_zz4l_massErr)),\
          self.models.HistTemplateToPdf("shapes/templates2D/pdfErrZX_4mu.root", "pdfErrZX_4mu", "pdfErr_zx", \
                                        ROOT.RooArgList(self.CMS_zz4l_massErr), ROOT.RooArgSet(self.CMS_zz4l_massErr))\

          ## KD template for 3D(m4l, m4l/m4lErr, KD) model building 
          self.models.HistTemplateToPdf("shapes/templates2D/Dsignal_4mu.root", "h_mzzD", "sigTemplatePdf",\
                                        ROOT.RooArgList(self.CMS_zz4l_mass, self.MELA_KD),\
                                        ROOT.RooArgSet(self.CMS_zz4l_mass, self.MELA_KD)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dbackground_qqZZ_4mu.root", "h_mzzD", "bkgTemplatePdf_qqzz",\
                                        ROOT.RooArgList(self.CMS_zz4l_mass, self.MELA_KD),\
                                        ROOT.RooArgSet(self.CMS_zz4l_mass, self.MELA_KD)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dbackground_ggZZ_4mu.root", "h_mzzD", "bkgTemplatePdf_ggzz",\
                                        ROOT.RooArgList(self.CMS_zz4l_mass, self.MELA_KD),\
                                        ROOT.RooArgSet(self.CMS_zz4l_mass, self.MELA_KD)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dbackground_ZX_4mu.root", "h_mzzD", "bkgTemplatePdf_ZX",\
                                        ROOT.RooArgList(self.CMS_zz4l_mass, self.MELA_KD),\
                                        ROOT.RooArgSet(self.CMS_zz4l_mass, self.MELA_KD)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dbackground_ZX_4mu.root", "h_mzzD_up", "bkgTemplateZX_up",\
                                        ROOT.RooArgList(self.CMS_zz4l_mass, self.MELA_KD),\
                                        ROOT.RooArgSet(self.CMS_zz4l_mass, self.MELA_KD)),\
          self.models.HistTemplateToPdf("shapes/templates2D/Dbackground_ZX_4mu.root", "h_mzzD_dn", "bkgTemplateZX_dn",\
                                        ROOT.RooArgList(self.CMS_zz4l_mass, self.MELA_KD),\
                                        ROOT.RooArgSet(self.CMS_zz4l_mass, self.MELA_KD)),\
          


      def MakeSlimWorkspace(self):
          print "put only useful var/pdf/rooformulavar/dataset in workspace"

test = main()

test.BuildWorkspace()
test.w_out.Print()
test.w_out.writeToFile("hzz4l_4muS_13TeV.input.root")

test.BuildDatacard()
