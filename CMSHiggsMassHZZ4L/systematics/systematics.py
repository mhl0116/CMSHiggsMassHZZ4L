class Systematics():

      def __init__(self, config):

          self.txtfile = config["txtfile"]
          self.sysDict_lnN = config["sysDict_lnN"] # {"name1":"xxx,xxx,xxx,-,xxx", "name2":"..."}
          self.names_lnN = config["names_lnN"]
          self.sysDict_param = config["sysDict_param"] 
          self.names_param = config["names_param"]


      def WriteSystematics(self):

          for name in self.names_lnN:
              WriteSystematic_lnN(name, self.sysDict_lnN[name])
          for name in self.names_param:
              WriteSystematic_lnN(name, self.sysDict_param[name])
             

      def WriteSystematic_lnN(self, name, sys):

          self.txtfile.write(name + " lnN ")
          self.txtfile.write(" ".join(sys) + "\n")


      def WriteSystematic_param(self, name, sys):      

          self.txtfile.write(name + " param " + sys + "\n")
