import ROOT
import ../yields/signalYields_4e
import ../yields/signalYields_4mu
import ../yields/signalYields_2e2mu

class GetYields():

      def __init__(self, config):

          self.MH = ROOT.RooRealVar("MH","MH", config["MH"])
          self.MH.setConstant(True)

          self.channel = config["channel"]

          self.yields = {"1":signalYields_4mu, "2":signalYields_4e, "3":signalYields_2e2mu}

      def signalYields(self): 

          rfvSigRate_ggH = ROOT.RooFormulaVar("ggH_hzz_norm", (self.yields)[self.channel]['ggH'], ROOT.RooArgList(self.MH))
          rfvSigRate_VBF = ROOT.RooFormulaVar("VBF_hzz_norm", (self.yields)[self.channel]['VBF'], ROOT.RooArgList(self.MH))
          rfvSigRate_WH = ROOT.RooFormulaVar("WH_hzz_norm", (self.yields)[self.channel]['WH_lep']+(self.yields)[self.channel]['WH_had'], ROOT.RooArgList(self.MH))
          rfvSigRate_ZH = ROOT.RooFormulaVar("ZH_hzz_norm", (self.yields)[self.channel]['ZH_lep']+(self.yields)[self.channel]['ZH_had'], ROOT.RooArgList(self.MH))
          rfvSigRate_ttH = ROOT.RooFormulaVar("ttH_hzz_norm", (self.yields)[self.channel]['ttH'], ROOT.RooArgList(self.MH))

      def backgroundYields(self):

