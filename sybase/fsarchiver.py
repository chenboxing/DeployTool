__author__ = 'boxingchen'
from base import Base
class FSArchiver(Base):
    def __init__(self):
        Base.__init__(self)
        self.xml_file = "sybase/fsarchiver.xml"
        self.module_name = "FSArchiver"
        self.log_file_name = "FSArchiver"
        self.settings_file = "sybase/fsarchiver.ini"
