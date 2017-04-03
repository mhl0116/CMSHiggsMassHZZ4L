import ROOT

class MakeModel():

      def __init__(self, config):

          self.MH = ROOT.RooRealVar("MH","MH", 125) 
          self.MH.setConstant(True)

          ### redesign so that take only input: vars, shapes, paras, report model one at a time ###
          self.w_in = config["w_in"] #workspace containing observables initially (m4l,m4lErr/m4l,kd)
          self.channel = config["channel"]

          self.CMS_zz4l_mass = self.w_in.var("CMS_zz4l_mass")
          self.CMS_zz4l_massErr = self.w_in.var("CMS_zz4l_massErr")
          self.MELA_KD = self.w_in.var("MELA_KD")

          self.signalCB = ROOT.RooDoubleCB()

          self.w_out = ROOT.RooWorkspace()

      #def FillWorkspace():

      def getVariable(self,trueVar,falseVar,testStatement):

          if (testStatement):
             return trueVar
          else:
             return falseVar

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
          name = "CMS_zz4l_n_sig_{0}".format(self.channel)
          CMS_zz4l_n = ROOT.RooRealVar(name,"CMS_zz4l_n",0.0,-0.99,0.99)

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

          rfv_mean_CB = ROOT.RooFormulaVar("mean_"+self.channel,"(" + doubleCBShape["mean"] + ")"+"+@0*@1", ROOT.RooArgList(self.MH, CMS_zz4l_mean_sig))
          #there should not be difference in results to define mean of CB in these two ways (check)
          #rfv_mean_CB = ROOT.RooFormulaVar("mean_"+self.channel,"(" + doubleCBShape["mean"] + ")"+"*(1+@1)", ROOT.RooArgList(self.MH, CMS_zz4l_mean_sig))
          rfv_sigma_CB = ROOT.RooFormulaVar("sigma_"+self.channel,"(" + doubleCBShape["sigma"] + ")"+"*(1+@1)", ROOT.RooArgList(self.MH, CMS_zz4l_sigma_sig))
          rfv_MassErr = ROOT.RooFormulaVar("rfv_MassErr_"+self.channel,"@1*@0*(1+@2)",ROOT.RooArgList(self.MassErr, self.MH, CMS_zz4l_sigma_sig))

          self.signalCB = ROOT.RooDoubleCB(name, name, self.CMS_zz4l_mass, \
                                      rfv_mean_CB, self.getVariable(rfv_MassErr, rfv_sigma_CB, includeErr), \
                                      rfv_alpha_CB, rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)

          #return signalCB



      #make below two as python template
      def MakeModel_EBE(self, name, model, errPdf): #m4l + per-event mass uncertainty

          modelEBE = ROOT.RooProdPdf(name, name, ROOT.RooArgSet(errPdf), ROOT.RooFit.Conditional(ROOT.RooArgSet(model), ROOT.RooArgSet(self.CMS_zz4l_mass) ) )


      def MakeModel_KD(self, name, model, KDPdf): #m4l + per-event mass uncertainty + ME kinematic discriminant

          modelEBE_KD = ROOT.RooProdPdf(name,name,ROOT.RooArgSet(model, ROOT.RooFit.Conditional(ROOT.RooArgSet(KDPdf),ROOT.RooArgSet(self.MELA_KD) ) )






'''
        w = ROOT.RooWorkspace("w","w")
        #w.importClassCode(RooqqZZPdf_v2.Class(),True)
        #w.importClassCode(RooggZZPdf_v2.Class(),True)
        w.importClassCode(RooDoubleCB.Class(),True)
        w.importClassCode(RooFormulaVar.Class(),True)

        getattr(w,'import')(data_obs,ROOT.RooFit.Rename("data_obs")) ### Should this be renamed?

        if (self.is2D == 0):
            if not self.bIncludingError:
                        signalCB_ggH.SetNameTitle("ggH_hzz","ggH_hzz")
                        signalCB_VBF.SetNameTitle("qqH_hzz","qqH_hzz")
                        signalCB_WH.SetNameTitle("WH_hzz","WH_hzz")
                        signalCB_ZH.SetNameTitle("ZH_hzz","ZH_hzz")
                        signalCB_ttH.SetNameTitle("ttH_hzz","ttH_hzz")

                        getattr(w,'import')(signalCB_ggH, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(signalCB_VBF, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(signalCB_WH, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(signalCB_ZH, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(signalCB_ttH, ROOT.RooFit.RecycleConflictNodes())
            else:
                        sig_ggHErr.SetNameTitle("ggH_hzz","ggH_hzz")
                        sig_VBFErr.SetNameTitle("qqH_hzz","qqH_hzz")
                        sig_WHErr.SetNameTitle("WH_hzz","WH_hzz")
                        sig_ZHErr.SetNameTitle("ZH_hzz","ZH_hzz")
                        sig_ttHErr.SetNameTitle("ttH_hzz","ttH_hzz")

                        getattr(w,'import')(sig_ggHErr, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(sig_VBFErr, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(sig_WHErr, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(sig_ZHErr, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(sig_ttHErr, ROOT.RooFit.RecycleConflictNodes())


        if (self.is2D == 1):

                    sigCB2d_ggH.SetNameTitle("ggH_hzz","ggH_hzz")
                    sigCB2d_VBF.SetNameTitle("qqH_hzz","qqH_hzz")
                    sigCB2d_WH.SetNameTitle("WH_hzz","WH_hzz")
                    sigCB2d_ZH.SetNameTitle("ZH_hzz","ZH_hzz")
                    sigCB2d_ttH.SetNameTitle("ttH_hzz","ttH_hzz")

                    getattr(w,'import')(sigCB2d_ggH, ROOT.RooFit.RecycleConflictNodes())
                    getattr(w,'import')(sigCB2d_VBF, ROOT.RooFit.RecycleConflictNodes())
                    getattr(w,'import')(sigCB2d_WH, ROOT.RooFit.RecycleConflictNodes())
                    getattr(w,'import')(sigCB2d_ZH, ROOT.RooFit.RecycleConflictNodes())
                    getattr(w,'import')(sigCB2d_ttH, ROOT.RooFit.RecycleConflictNodes())

        if (self.is2D == 0):
                if not self.bIncludingError:
                        bkg_qqzz.SetNameTitle("bkg_qqzz","bkg_qqzz")
                        bkg_ggzz.SetNameTitle("bkg_ggzz","bkg_ggzz")
                        bkg_zjets.SetNameTitle("bkg_zjets","bkg_zjets")
                        getattr(w,'import')(bkg_qqzz, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(bkg_ggzz, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(bkg_zjets, ROOT.RooFit.RecycleConflictNodes())
                else:
                        bkg_qqzzErr.SetNameTitle("bkg_qqzz","bkg_qqzz")
                        bkg_ggzzErr.SetNameTitle("bkg_ggzz","bkg_ggzz")
                        bkg_zjetsErr.SetNameTitle("bkg_zjets","bkg_zjets")
                        getattr(w,'import')(bkg_qqzzErr, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(bkg_ggzzErr, ROOT.RooFit.RecycleConflictNodes())
                        getattr(w,'import')(bkg_zjetsErr, ROOT.RooFit.RecycleConflictNodes())

        if (self.is2D == 1):
                getattr(w,'import')(bkg2d_qqzz,ROOT.RooFit.RecycleConflictNodes())
                getattr(w,'import')(bkg2d_ggzz,ROOT.RooFit.RecycleConflictNodes())
                getattr(w,'import')(bkg2d_zjets,ROOT.RooFit.RecycleConflictNodes())


        getattr(w,'import')(rfvSigRate_ggH, ROOT.RooFit.RecycleConflictNodes())
        getattr(w,'import')(rfvSigRate_VBF, ROOT.RooFit.RecycleConflictNodes())
        getattr(w,'import')(rfvSigRate_WH, ROOT.RooFit.RecycleConflictNodes())
        getattr(w,'import')(rfvSigRate_ZH, ROOT.RooFit.RecycleConflictNodes())
        getattr(w,'import')(rfvSigRate_ttH, ROOT.RooFit.RecycleConflictNodes())

        CMS_zz4l_mass.setRange(self.low_M,self.high_M)

'''
