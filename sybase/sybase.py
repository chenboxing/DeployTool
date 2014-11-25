from  base import Base
import  subprocess

class Sybase(Base):

    def __init__(self):
        Base.__init__(self)
        self.xml_file = "sybase/sybase.xml"
        self.module_name = "sybase"
        self.log_file_name = "sybase"

    def sy_deploy(self):
        dbname = self.settings["sy_dbname"]
        self.logger.info("db name is %s" % dbname)
        self.logger.error("debug message db name is %s" % dbname)
        self.logger.error("error message db name is %s" % dbname)
        print("deploy sybase")




