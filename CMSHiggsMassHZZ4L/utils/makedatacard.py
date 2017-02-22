class Makedatacard():

      def __init__(self, config):

          self.self.txtfile = config["txtfile"]
          self.nChannel = config["nChannel"]  
          self.nSig = config["nSig"]
          self.nBkg = config["nBkg"]
          self.workspaceName = config["workspaceName"]
          self.channelName = config["channelName"]
          self.obsEvents = config["obsEvents"]
          self.processList = config["processList"]
          self.rates = config["rates"]


      def WriteComment(self, comment):
      
          self.txtfile.write("## {0}\n".format(comment) )
      
      
      def WriteBasicNum(self, nChannel, nSig, nBkg, nNuisance=0):
      
          self.txtfile.write("imax {0}\n".format(nChannel) )
          self.txtfile.write("jmax {0}\n".format(nSig + nBkg - 1) )
          if nNuisance > 0:
             self.txtfile.write("kmax {0}\n".format(nNuisance) )
          else:
             self.txtfile.write("kmax *\n")
          self.txtfile.write("------------\n")
      
      
      def WriteShape(self, workspaceName, option=""):
      
          self.txtfile.write("shapes * * {0} w:$PROCESS \n".format(workspaceName) )
          self.txtfile.write("------------\n")
      
      
      def WriteObs(self, channelName, obsEvents):
      
          self.txtfile.write("bin {0} \n".format(channelName) )
          self.txtfile.write("observation {0} \n".format(obsEvents) )
          self.txtfile.write("------------\n")
      
      
      def WriteExpect(self, channelName, nSig, nBkg, processList, rates):
      
          self.txtfile.write("bin " + " ".join.([channelName]*len(processList) ) + "\n")
          self.txtfile.write("process " + " ".join(processList) + "\n")
          self.txtfile.write("process ")
          self.txtfile.write(" ".join([i-len(sell.nSig)+1 for i in range(nSig)]) )
          self.txtfile.write(" ".join([i+1 for i in range(nBkg)]) + "\n")
          self.txtfile.write("rate " + " ".join(rates) + "\n")
          self.txtfile.write("------------\n")


      def WriteDatacard(self):

          self.WriteBasicNum(self.nChannel, self.nSig, self.nBkg)
          self.WriteShape(self.workspaceName)
          self.WriteObs(self.channelName, self.obsEvents)
          self.WriteComment("## mass window [105.0,140.0]")
          self.WriteExpect(self.channelName, self.nSig, self.nBkg, self.processList, self.rates)


