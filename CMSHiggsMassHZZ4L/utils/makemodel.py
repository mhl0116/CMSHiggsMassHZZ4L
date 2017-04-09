import ROOT
import sys

class MakeModel():

      def __init__(self, config):

          self.MH = ROOT.RooRealVar("MH","MH", config["MH"]) 
          self.MH.setConstant(True)

          self.w_in = config["w_in"] #workspace containing observables initially (m4l,m4lErr/m4l,kd)
          self.channel = config["channel"]

          self.CMS_zz4l_mass = self.w_in.var("CMS_zz4l_mass")
          self.CMS_zz4l_massErr = self.w_in.var("CMS_zz4l_massErr")
          self.MELA_KD = self.w_in.var("MELA_KD")

          self.w_out = config["w_out"]


      def getVariable(self,trueVar,falseVar,testStatement):

          if (testStatement):
             return trueVar
          else:
             return falseVar


      def MakeDoubleCB(self, name, doubleCBShape, includeErr):

          #set up shape uncertainties
          CMS_zz4l_mean_sig = self.GetScaleUnc()
          CMS_zz4l_sigma_sig = self.GetResolutionUnc()

          #name = "CMS_zz4l_alpha2_{0}".format(self.channel)
          #CMS_zz4l_alpha2 = ROOT.RooRealVar(name,"CMS_zz4l_alpha2",0.0,-0.99,0.99)
          #name = "CMS_zz4l_n2_sig_{0}".format(self.channel)
          #CMS_zz4l_n2 = ROOT.RooRealVar(name,"CMS_zz4l_n2",0.0,-0.99,0.99)
          #name = "CMS_zz4l_alpha_{0}".format(self.channel)
          #CMS_zz4l_alpha = ROOT.RooRealVar(name,"CMS_zz4l_alpha",0.0,-0.99,0.99)
          tmpname = "CMS_zz4l_n_sig_{0}".format(self.channel)
          CMS_zz4l_n = ROOT.RooRealVar(tmpname,"CMS_zz4l_n",0.0,-0.99,0.99)

          CMS_zz4l_mean_sig.setVal(0)
          CMS_zz4l_sigma_sig.setVal(0)
          #CMS_zz4l_alpha.setVal(0)
          CMS_zz4l_n.setVal(0)
          #CMS_zz4l_alpha2.setVal(0)
          #CMS_zz4l_n2.setVal(0)

          #set up shape parameters
          rfv_n_CB = ROOT.RooFormulaVar("n_"+self.channel, "(" + doubleCBShape["n"] + ")*(1+@1)",ROOT.RooArgList(self.MH,CMS_zz4l_n))
          rfv_alpha_CB = ROOT.RooFormulaVar("alpha_"+self.channel,"(" + doubleCBShape["alpha"] + ")", ROOT.RooArgList(self.MH))
          rfv_n2_CB = ROOT.RooFormulaVar("n2_"+self.channel,"(" + doubleCBShape["n2"] + ")",ROOT.RooArgList(self.MH))
          rfv_alpha2_CB = ROOT.RooFormulaVar("alpha2_"+self.channel,"(" + doubleCBShape["alpha2"] + ")", ROOT.RooArgList(self.MH))

          #rfv_mean_CB = ROOT.RooFormulaVar("mean_"+self.channel,"(" + doubleCBShape["mean"] + ")"+"+@0*@1", ROOT.RooArgList(self.MH, CMS_zz4l_mean_sig))
          #there should not be difference in results to define mean of CB in these two ways (check)
          rfv_mean_CB = ROOT.RooFormulaVar("mean_"+self.channel,"(" + doubleCBShape["mean"] + ")"+"*(1+@1)", ROOT.RooArgList(self.MH, CMS_zz4l_mean_sig))
          rfv_sigma_CB = ROOT.RooFormulaVar("sigma_"+self.channel,"(" + doubleCBShape["sigma"] + ")"+"*(1+@1)", ROOT.RooArgList(self.MH, CMS_zz4l_sigma_sig))
          rfv_MassErr = ROOT.RooFormulaVar("rfv_MassErr_"+self.channel,"@1*@0*(1+@2)",ROOT.RooArgList(self.CMS_zz4l_massErr, self.MH, CMS_zz4l_sigma_sig))

          signalCB = ROOT.RooDoubleCB(name, name, self.CMS_zz4l_mass, rfv_mean_CB, self.getVariable(rfv_MassErr, rfv_sigma_CB, includeErr), rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)

          #signalCB.Print()
          getattr(self.w_out,'import')(signalCB,ROOT.RooFit.RecycleConflictNodes())
          #return signalCB


      #might not need these two
      def MakeBernstein(self, name, bernsteinShape):
 
          bernstein_b0 = ROOT.RooRealVar(name+"_b0", "", float(bernsteinShape["b0"]) )
          bernstein_b1 = ROOT.RooRealVar(name+"_b1", "", float(bernsteinShape["b1"]) )
          bernstein_b2 = ROOT.RooRealVar(name+"_b2", "", float(bernsteinShape["b2"]) )

          bernsteinShape = ROOT.RooBernstein(name, name, self.CMS_zz4l_mass, \
                                             ROOT.RooArgList(bernstein_b0, bernstein_b1, bernstein_b2) )

          getattr(self.w_out,'import')(bernsteinShape,ROOT.RooFit.RecycleConflictNodes())
          #return bernsteinShape


      def MakeLandau(self, name, landauShape):

          landauMean = ROOT.RooRealVar(name+"_landauMean","",float(landauShape["mean"]) )
          landauSigma = ROOT.RooRealVar(name+"_landauSigma","",float(landauShape["sigma"]) )
          landauShape = ROOT.RooLandau(name, name, self.CMS_zz4l_mass, landauMean, landauSigma) 
 
          getattr(self.w_out,'import')(landauShape,ROOT.RooFit.RecycleConflictNodes())
          #return landauShape


      #might not need this one
      def MakeConditionalProd(self, name, model1, model2, conditionalVar):

          conditionalProd = ROOT.RooProdPdf(name, name, ROOT.RooArgSet(model1), ROOT.RooFit.Conditional(ROOT.RooArgSet(model2), ROOT.RooArgSet(conditionalVar) ) )
          #modelEBE = ROOT.RooProdPdf(name, name, ROOT.RooArgSet(errPdf), ROOT.RooFit.Conditional(ROOT.RooArgSet(model), ROOT.RooArgSet(self.CMS_zz4l_mass) ) )
          #modelEBE_KD = ROOT.RooProdPdf(name,name,ROOT.RooArgSet(model), ROOT.RooFit.Conditional(ROOT.RooArgSet(KDPdf),ROOT.RooArgSet(self.MELA_KD) ) )
          getattr(self.w_out,'import')(conditionalProd,ROOT.RooFit.RecycleConflictNodes())
          #return conditionalProd


      #make below two as python template
      def GetScaleUnc(self):

          CMS_zz4l_mean_m_sig = ROOT.RooRealVar("CMS_zz4l_mean_m_sig", "", 0,-0.99,0.99)
          CMS_zz4l_mean_e_sig = ROOT.RooRealVar("CMS_zz4l_mean_e_sig", "", 0,-0.99,0.99)

          if self.channel == "1":
             rv_scaleUnc = CMS_zz4l_mean_m_sig
             return rv_scaleUnc

          if self.channel == "2":
             rv_scaleUnc = CMS_zz4l_mean_e_sig
             return rv_scaleUnc

          if self.channel == "3":
             rv_scaleUnc = ROOT.RooFormulaVar("CMS_zz4l_mean_m_e_sig", "", "(@0+@1)/2", \
                                               ROOT.RooArgList(CMS_zz4l_mean_m_sig, CMS_zz4l_mean_e_sig) )
             return rv_scaleUnc

      def GetResolutionUnc(self):

          CMS_zz4l_sigma_m_sig = ROOT.RooRealVar("CMS_zz4l_sigma_m_sig", "", 0,-0.99,0.99)
          CMS_zz4l_sigma_e_sig = ROOT.RooRealVar("CMS_zz4l_sigma_e_sig", "", 0,-0.99,0.99)

          if self.channel == "1":
             rv_resolutionUnc = CMS_zz4l_sigma_m_sig
             return rv_resolutionUnc

          if self.channel == "2":
             rv_resolutionUnc = CMS_zz4l_sigma_e_sig
             return rv_resolutionUnc

          if self.channel == "3":
             rv_resolutionUnc = ROOT.RooFormulaVar("CMS_zz4l_sigma_m_e_sig", "", "TMath::Sqrt((1+@0)*(1+@1))", \
                                                    ROOT.RooArgList(CMS_zz4l_sigma_m_sig, CMS_zz4l_sigma_e_sig) )
             return rv_resolutionUnc


      def GetZXShape_4mu_reco(self):

          p0_zjets_4mu = ROOT.RooRealVar("p0_zjets_4mu","p0_zjets_4mu",130.4)
          p1_zjets_4mu = ROOT.RooRealVar("p1_zjets_4mu","p1_zjets_4mu",15.6)
          landau_zjets_4mu = ROOT.RooFormulaVar("landau_zjets_4mu","TMath::Landau(@0,@1,@2)",ROOT.RooArgList(self.CMS_zz4l_mass,p0_zjets_4mu,p1_zjets_4mu))
          bkg_zjets = ROOT.RooGenericPdf("bkg_zjets","landau_zjets_4mu", ROOT.RooArgList(landau_zjets_4mu) )

          getattr(self.w_out,'import')(bkg_zjets)


      def GetZXShape_4e_reco(self):

          p0_zjets_4e = ROOT.RooRealVar("p0_zjets_4e","p0_zjets_4e",141.9)
          p1_zjets_4e = ROOT.RooRealVar("p1_zjets_4e","p1_zjets_4e",21.3)
          p2_zjets_4e = ROOT.RooRealVar("p2_zjets_4e","p2_zjets_4e",7.06)
          p3_zjets_4e = ROOT.RooRealVar("p3_zjets_4e","p3_zjets_4e",-0.00497)
          landau_zjets_4e = ROOT.RooFormulaVar("landau_zjets_4e","TMath::Landau(@0,@1,@2)",ROOT.RooArgList(self.CMS_zz4l_mass,p0_zjets_4e,p1_zjets_4e))
          bkg_zjets = ROOT.RooGenericPdf("bkg_zjetsTMP4e","landau_zjets_4e*(1+TMath::Exp(p2_zjets_4e+p3_zjets_4e*@3))", ROOT.RooArgList(landau_zjets_4e, p2_zjets_4e, p3_zjets_4e,self.CMS_zz4l_mass) )

          return bkg_zjets


      def GetZXShape_2e2mu_reco(self):

          p0_zjets_2e2mu = ROOT.RooRealVar("p0_zjets_2e2mu","p0_zjets_2e2mu",131.1)
          p1_zjets_2e2mu = ROOT.RooRealVar("p1_zjets_2e2mu","p1_zjets_2e2mu",18.1)
          p2_zjets_2e2mu = ROOT.RooRealVar("p2_zjets_2e2mu","p2_zjets_2e2mu",0.45)

          p3_zjets_2e2mu = ROOT.RooRealVar("p3_zjets_2e2mu","p3_zjets_2e2mu",133.8)
          p4_zjets_2e2mu = ROOT.RooRealVar("p4_zjets_2e2mu","p4_zjets_2e2mu",18.9)
          p5_zjets_2e2mu = ROOT.RooRealVar("p5_zjets_2e2mu","p5_zjets_2e2mu",0.55)

          landau_zjets_2e2mu = ROOT.RooFormulaVar("landau_zjets_2e2mu","TMath::Landau(@0,@1,@2)*@3 + TMath::Landau(@0,@4,@5)*@6",ROOT.RooArgList(self.CMS_zz4l_mass,p0_zjets_2e2mu, p1_zjets_2e2mu, p2_zjets_2e2mu, p3_zjets_2e2mu, p4_zjets_2e2mu, p5_zjets_2e2mu))
          bkg_zjets = ROOT.RooGenericPdf("bkg_zjetsTMP2e2mu","landau_zjets_2e2mu", ROOT.RooArgList(landau_zjets_2e2mu))

          return bkg_zjets


      def GetZXShape_4mu_refit(self):

          p0_zjets_4mu = ROOT.RooRealVar("p0_zjets_4mu","p0_zjets_4mu",134.1)
          p1_zjets_4mu = ROOT.RooRealVar("p1_zjets_4mu","p1_zjets_4mu",21.01)
          landau_zjets_4mu = ROOT.RooFormulaVar("landau_zjets_4mu","TMath::Landau(@0,@1,@2)",ROOT.RooArgList(self.CMS_zz4l_mass,p0_zjets_4mu,p1_zjets_4mu))
          bkg_zjets = ROOT.RooGenericPdf("bkg_zjetsTMP4mu","landau_zjets_4mu", ROOT.RooArgList(landau_zjets_4mu) )

          return bkg_zjets


      def GetZXShape_4e_refit(self):

          p0_zjets_4e = ROOT.RooRealVar("p0_zjets_4e","p0_zjets_4e",141.9)
          p1_zjets_4e = ROOT.RooRealVar("p1_zjets_4e","p1_zjets_4e",21.3)
          p2_zjets_4e = ROOT.RooRealVar("p2_zjets_4e","p2_zjets_4e",7.06)
          p3_zjets_4e = ROOT.RooRealVar("p3_zjets_4e","p3_zjets_4e",-0.00497)
          landau_zjets_4e = ROOT.RooFormulaVar("landau_zjets_4e","TMath::Landau(@0,@1,@2)",ROOT.RooArgList(self.CMS_zz4l_mass,p0_zjets_4e,p1_zjets_4e))
          bkg_zjets = ROOT.RooGenericPdf("bkg_zjetsTMP4e","landau_zjets_4e*(1+TMath::Exp(p2_zjets_4e+p3_zjets_4e*@3))", ROOT.RooArgList(landau_zjets_4e, p2_zjets_4e, p3_zjets_4e,self.CMS_zz4l_mass) )

          return bkg_zjets


      def GetZXShape_2e2mu_refit(self):

          p0_zjets_2e2mu = ROOT.RooRealVar("p0_zjets_2e2mu","p0_zjets_2e2mu",131.1)
          p1_zjets_2e2mu = ROOT.RooRealVar("p1_zjets_2e2mu","p1_zjets_2e2mu",18.1)
          p2_zjets_2e2mu = ROOT.RooRealVar("p2_zjets_2e2mu","p2_zjets_2e2mu",0.45)

          p3_zjets_2e2mu = ROOT.RooRealVar("p3_zjets_2e2mu","p3_zjets_2e2mu",133.8)
          p4_zjets_2e2mu = ROOT.RooRealVar("p4_zjets_2e2mu","p4_zjets_2e2mu",18.9)
          p5_zjets_2e2mu = ROOT.RooRealVar("p5_zjets_2e2mu","p5_zjets_2e2mu",0.55)

          landau_zjets_2e2mu = ROOT.RooFormulaVar("landau_zjets_2e2mu","TMath::Landau(@0,@1,@2)*@3 + TMath::Landau(@0,@4,@5)*@6",ROOT.RooArgList(self.CMS_zz4l_mass,p0_zjets_2e2mu, p1_zjets_2e2mu, p2_zjets_2e2mu, p3_zjets_2e2mu, p4_zjets_2e2mu, p5_zjets_2e2mu))
          bkg_zjets = ROOT.RooGenericPdf("bkg_zjetsTMP2e2mu","landau_zjets_2e2mu", ROOT.RooArgList(landau_zjets_2e2mu))

          return bkg_zjets



      def HistTemplateToPdf(self, fileName, templateName, pdfname, arglist, argset):

          templateFile = ROOT.TFile(fileName)
          template = templateFile.Get(templateName)
          datahistName = "datahist_"+templateName
          #tempDataHist = ROOT.RooDataHist(datahistName,datahistName,ROOT.RooArgList(var), template)
          #pdf = ROOT.RooHistPdf(pdfname,pdfname,ROOT.RooArgSet(var),tempDataHist)
          tempDataHist = ROOT.RooDataHist(datahistName,datahistName, arglist, template)
          pdf = ROOT.RooHistPdf(pdfname,pdfname,argset,tempDataHist)
          #var = RooArgList or RooArgset
          getattr(self.w_out,'import')(pdf,ROOT.RooFit.RecycleConflictNodes())


      def histogramBinFix(self,hist,histname):

          dBinsX = hist.GetXaxis().GetNbins()
          dBinsY = hist.GetYaxis().GetNbins()
          dLowY = hist.GetYaxis().GetXmin()
          dHighY = hist.GetYaxis().GetXmax()

          xBins = array('d', [105]) # e.g. self.low_M =105, self.high_M=140
          nBinsNew = 0
          for nxbin in range(1,dBinsX):
              if 105<hist.GetXaxis().GetBinLowEdge(nxbin):
                  if 140>hist.GetXaxis().GetBinLowEdge(nxbin):
                     xBins.append(hist.GetXaxis().GetBinLowEdge(nxbin))
                     nBinsNew+=1

          xBins.append(105)

          hist_fix = ROOT.TH2F(histname,histname,nBinsNew+1,xBins,dBinsY,dLowY,dHighY)

          for nxbin in range(1,hist_fix.GetXaxis().GetNbins()+1):
              binnum = hist.FindBin(hist_fix.GetXaxis().GetBinCenter(nxbin),hist_fix.GetYaxis().GetBinCenter(nybin))
              binval = hist.GetBinContent(binnum)
              currentbin = hist_fix.FindBin(hist_fix.GetXaxis().GetBinCenter(nxbin),hist_fix.GetYaxis().GetBinCenter(nybin))
              hist_fix.SetBinContent(currentbin,binval)

          return hist_fix

