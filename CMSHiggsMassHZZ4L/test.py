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


