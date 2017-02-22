def WriteComment(txtfile, comment):

    txtfile.write("## {0}\n".format(comment) )


def WriteBasicNum(txtfile, nChannel, nSig, nBkg, nNuisance=0):

    txtfile.write("imax {0}\n".format(nChannel) )
    txtfile.write("jmax {0}\n".format(nSig + nBkg - 1) )
    if nNuisance > 0:
       txtfile.write("kmax {0}\n".format(nNuisance) )
    else:
       txtfile.write("kmax *\n")
    txtfile.write("------------\n")


def WriteShape(txtfile, workspaceName, option=""):

    txtfile.write("shapes * * {0} w:$PROCESS \n".format(workspaceName) )
    txtfile.write("------------\n")


def WriteObs(txtfile, channelName, obsEvents):

    txtfile.write("bin {0} \n".format(channelName) )
    txtfile.write("observation {0} \n".format(obsEvents) )
    txtfile.write("------------\n")


def WriteExpect(txtfile, channelName, processList, nSig, nBkg, rates):

    txtfile.write("bin " + " ".join.([channelName]*len(processList) ) + "\n")
    txtfile.write("process " + " ".join(processList) + "\n")
    txtfile.write("process ")
    txtfile.write(" ".join([i-len(nSig)+1 for i in range(nSig)]) )
    txtfile.write(" ".join([i+1 for i in range(nBkg)]) + "\n")
    txtfile.write("rate " + " ".join(rates) + "\n")
    txtfile.write("------------\n")

