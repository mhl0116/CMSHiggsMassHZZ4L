from ROOT import *
from array import array
from subprocess import call

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

#          hist_fix.Scale(1/hist_fix.Integral())
          return hist_fix

name = "Dbackground_ZX_4mu"

f1 = TFile(name + ".root")
hist = f1.Get("h_mzzD")
hist_new = histogramBinFix(hist, "h_mzzD_1")
del hist
hist_new.SetName("h_mzzD")

hist = f1.Get("h_mzzD_up")
hist_new_up = histogramBinFix(hist, "h_mzzD_1")
del hist
hist_new_up.SetName("h_mzzD_up")

hist = f1.Get("h_mzzD_dn")
hist_new_dn = histogramBinFix(hist, "h_mzzD_1")
del hist
hist_new_dn.SetName("h_mzzD_dn")


f2 = TFile(name + "_new.root","RECREATE")
f2.cd()
hist_new.Write()
hist_new_up.Write()
hist_new_dn.Write()

f2.Close()

call("mv "+name+"_new.root " + name + ".root",shell=True)
