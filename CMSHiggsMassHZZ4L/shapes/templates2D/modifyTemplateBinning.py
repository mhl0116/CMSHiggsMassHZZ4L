from ROOT import *
from array import array

def histogramBinFix(hist,histname):

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

          xBins.append(140)

          hist_fix = TH2F(histname,histname,nBinsNew+1,xBins,dBinsY,dLowY,dHighY)

          for nybin in range(1,hist_fix.GetYaxis().GetNbins()+1):
              for nxbin in range(1,hist_fix.GetXaxis().GetNbins()+1):
                  binnum = hist.FindBin(hist_fix.GetXaxis().GetBinCenter(nxbin),hist_fix.GetYaxis().GetBinCenter(nybin))
                  binval = hist.GetBinContent(binnum)
                  currentbin = hist_fix.FindBin(hist_fix.GetXaxis().GetBinCenter(nxbin),hist_fix.GetYaxis().GetBinCenter(nybin))
                  hist_fix.SetBinContent(currentbin,binval)

          return hist_fix

f1 = TFile("Dsignal_4mu.root")
hist = f1.Get("h_mzzD")
hist_new = histogramBinFix(hist, "h_mzzD")

f2 = TFile("Dsignal_4mu_new.root","RECREATE")
f2.cd()
hist_new.Write()
f2.Close()
