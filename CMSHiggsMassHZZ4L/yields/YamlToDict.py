def GetDict(fs, cat):
#    yaml = [line.strip() for line in open("yield_"+fs+".yaml", 'r')]
    yaml = [line.strip() for line in open("yields_per_tag_category_13TeV_"+fs+"_6cat.yaml", 'r')]

    if not cat == 'VBF':
       catYaml = [line for line in yaml if cat+':' in line]
       catDict = [catYaml[i].replace(cat, 'name_'+cat+'_'+str(i)).replace(": ","='")+"'" for i in range(len(catYaml))]
    else:
       catYaml = [line for line in yaml if 'qqH:' in line]
       catDict = [catYaml[i].replace('qqH', 'name_VBF_'+str(i)).replace(": ","='")+"'" for i in range(len(catYaml))]

    yields = ""
    for x in catDict:
#        print '           '+cat
#        print '   ' + cat
        yields += (x.split("'"))[1]
#    print cat,":",yields
#    print ''
    return yields

finalState = ['4e', '4mu', '2e2mu']
cats = ['ggH', 'VBF', 'WH_lep', 'WH_had', 'ZH_lep', 'ZH_had', 'ttH']


for fs in finalState:
#    print '        if (self.channel == self.ID_' + fs  + ') :'
#    print 'if (self.channel == self.ID_' + fs  + ') :'
    with open("signalYields_"+fs+".py","w") as myfile:
         myfile.write("signalYields_"+fs+"={"+"\\\n")
         for cat in cats:
             if not cat == 'ttH':
                myfile.write("'"+cat + "':'" + GetDict(fs, cat) + "', \\\n")
             else:
                myfile.write("'"+cat + "':'" + GetDict(fs, cat) + "' \\\n")
         myfile.write("}")
#    print ''
