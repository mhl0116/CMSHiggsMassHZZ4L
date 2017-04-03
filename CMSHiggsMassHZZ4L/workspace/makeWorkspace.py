import ROOT

signal:

DCB
WH/ZH

backgroud:

RooBernstein
Landau

2D,3D + additional pdf

class Makeworkspace():

      def __init__(self):

          self.w = ROOT.RooWorkspace()


      def FillVariables():
      def FillPdfs():
      def FillYields():




FillVariables(m4l,m4lerr)
FillPdfs(dcb)
FillPdfs(dcb+ebe)
-MakeDCB() 
-MakePdfErr() <- read template from file
--MakeRooVarFormula() * 6 <- make config from file

need a few RooRealVar in advance


###
massLow = 105
massHigh = 140
CMS_zz4l_mass = RooRealVar("CMS_zz4l_mass","",massLow,massHigh) 
CMS_zz4l_mass.setBins(700)

MH = ROOT.RooRealVar("MH","MH",mH)
MH.setConstant(True)

name = "CMS_zz4l_mean_m_sig"
CMS_zz4l_mean_m_sig = ROOT.RooRealVar(name,"CMS_zz4l_mean_sig",0.0,-10.0,10.0)
name = "CMS_zz4l_mean_m_err_{0}_{1:.0f}".format(self.channel,self.sqrts)
CMS_zz4l_mean_m_err = ROOT.RooRealVar(name,"CMS_zz4l_mean_m_err",float(theInputs['CMS_zz4l_mean_m_sig']))
name = "CMS_zz4l_sigma_m_sig"
CMS_zz4l_sigma_m_sig = ROOT.RooRealVar(name,"CMS_zz4l_sigma_sig",0.0,-0.99,0.99)

name = "CMS_zz4l_alpha2_{0}_{1:.0f}".format(self.channel,self.sqrts)
CMS_zz4l_alpha2 = ROOT.RooRealVar(name,"CMS_zz4l_alpha2",0.0,-0.99,0.99)
name = "CMS_zz4l_n2_sig_{0}_{1:.0f}".format(self.channel,self.sqrts)
CMS_zz4l_n2 = ROOT.RooRealVar(name,"CMS_zz4l_n2",0.0,-0.99,0.99)
name = "CMS_zz4l_alpha_{0}_{1:.0f}".format(self.channel,self.sqrts)
CMS_zz4l_alpha = ROOT.RooRealVar(name,"CMS_zz4l_alpha",0.0,-0.99,0.99)
name = "CMS_zz4l_n_sig_{0}_{1:.0f}".format(self.channel,self.sqrts)
CMS_zz4l_n = ROOT.RooRealVar(name,"CMS_zz4l_n",0.0,-0.99,0.99)

CMS_zz4l_mean_e_sig.setVal(0)
CMS_zz4l_mean_e_err.setConstant(kTRUE)
CMS_zz4l_sigma_e_sig.setVal(0)
CMS_zz4l_mean_m_sig.setVal(0)
CMS_zz4l_mean_m_err.setConstant(kTRUE)
CMS_zz4l_sigma_m_sig.setVal(0)
CMS_zz4l_alpha.setVal(0)
CMS_zz4l_n.setVal(0)
CMS_zz4l_alpha2.setVal(0)
CMS_zz4l_n2.setVal(0)

rfv_n_CB = ROOT.RooFormulaVar()
rfv_alpha_CB = ROOT.RooFormulaVar()
rfv_n2_CB = ROOT.RooFormulaVar()
rfv_alpha2_CB = ROOT.RooFormulaVar()
rfv_sigma_CB = ROOT.RooFormulaVar()
rfv_mean_CB = ROOT.RooFormulaVar()

rfv_n_CB = ROOT.RooFormulaVar(name,"("+sig[name]+")*(1+@1)",ROOT.RooArgList(self.MH,CMS_zz4l_n))
rfv_alpha_CB = ROOT.RooFormulaVar(name,"("+sig[name]+")", ROOT.RooArgList(self.MH))
rfv_n2_CB = ROOT.RooFormulaVar(name,"("+sig[name]+")",ROOT.RooArgList(self.MH))
rfv_alpha2_CB = ROOT.RooFormulaVar(name,"("+sig[name]+")", ROOT.RooArgList(self.MH))

CMS_zz4l_mean_sig_NoConv = ROOT.RooFormulaVar(name,"("+sig[name]+")"+"+@0*@1*@2", ROOT.RooArgList(self.MH, CMS_zz4l_mean_m_sig,CMS_zz4l_mean_m_err))
rfv_sigma_CB = ROOT.RooFormulaVar(name,"("+sig[name]+")"+"*(1+@1)", ROOT.RooArgList(self.MH, CMS_zz4l_sigma_m_sig))

signalCB_ggH = ROOT.RooDoubleCB(name,name,CMS_zz4l_mass, CMS_zz4l_mean_sig_NoConv, self.getVariable(rfv_MassErr,rfv_sigma_CB, self.bIncludingError),rfv_alpha_CB,rfv_n_CB, rfv_alpha2_CB, rfv_n2_CB)
