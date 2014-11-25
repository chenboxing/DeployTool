__author__ = 'boxingchen'

import sys
import os
from xml.etree import ElementTree
import ConfigParser
import logging
import logging.config
import logging.handlers
import subprocess

class Base(object):

    def __init__(self):
        self.xml_file = 'menu.xml'
        self.settings_file = "settings.ini"
        self.log_file_name = "deploy.log"
        self.module_name = "Deployment Tools"
        self._settings = {}
        self._logger = None
        self._shortcut_keys = []   #the list of shortcut keys
        self._parameter_keys = []  #the list of parameters about the xml file



    def render(self):
        """
        Parse current menu file to render the content to the console screen
        """
        #render screen
        #try:
        #    os.system("clear")
        #except:
        #    pass

        tmp = "\n===  %s  ===\n" % self.module_name

        # show parameters for the menu
        if len(self.parameter_keys) > 0 :
            tmp += "Parameters:\n"
            for parameter in self.parameter_keys:
                tmp += "* .. %-50s : %s\n" % (parameter['desp'],self.settings[parameter['key']])

        tmp += "\n"
        for shortcut in self.shortcut_keys:
            tmp += "%s.) %s\n" % (shortcut['key'].upper(), shortcut['desp'])

        tmp += "\nPlease select a choice or Press enter to exit:"
        c = raw_input(tmp)
        return c

    def save_parameters(self):
        """
        Save parameters to ini file
        """
        conf = ConfigParser.ConfigParser()
        conf.read(self.settings_file)


        isDirty = False
        for parameter in self.parameter_keys:
            print("%s : %s" % (parameter['key'],self.settings[parameter['key']]))
            new_value = raw_input("Please type a new value for %s , or press enter to keep it:" % parameter["desp"])
            if new_value != '':
                conf.set("parameters",parameter['key'],new_value)
                if new_value != self.settings[parameter['key']]:
                    isDirty = True

        if isDirty == True:
            confirm_val = raw_input("Are you sure to save the changes(Y/n):")
            if confirm_val.upper() == "Y":
                #Save config file
                settings_abs_path = os.path.abspath(self.settings_file)
                print(settings_abs_path)
                conf.write(open(settings_abs_path, "w"))
                self._settings = {}
                #re-fresh screen



    def __parse_xml(self):
        root = ElementTree.parse(os.path.abspath(self.xml_file))
        elt_opts_lst = root.getiterator("option")
        self._parameter_keys = []
        for nd_opt in elt_opts_lst:
            option = {}
            option['key']  = nd_opt.attrib['key']
            if not self.settings.has_key(option['key']):
                self._settings[option['key']] = ''
            option['desp'] = nd_opt.text
            self._parameter_keys.append(option)

        #retrieve shortcuts from xml files
        self._shortcut_keys = []
        elt_keys_lst = root.getiterator("shortcut")
        for nd_shortcut in elt_keys_lst:
           shortcut = {}
           shortcut['key']  = nd_shortcut.attrib['key']
           shortcut['desp'] = nd_shortcut.text
           shortcut['command'] = nd_shortcut.attrib['command']
           self._shortcut_keys.append(shortcut)

    @property
    def logger(self):
        if self._logger == None:

            logger = logging.getLogger("")
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            formatter.datefmt = "%a, %d %b %Y %H:%M:%S"
            # Add TimedRotatingFileHandler to logger
            #log_file_name = os.path.abspath("logs/" + self.log_file_name)
            file_handler = logging.handlers.TimedRotatingFileHandler("logs/" + self.log_file_name, 'D', 1, 10)
            # setting the name of suffix , just like the format of
            file_handler.suffix = "%Y%m%d.log"

            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            #settings output of console
            console_handle = logging.StreamHandler()
            console_handle.setFormatter(formatter)
            logger.addHandler(console_handle)

            self._logger = logger

        return self._logger



    @property
    def shortcut_keys(self):
        if len(self._shortcut_keys) == 0:
            self.__parse_xml()
        return self._shortcut_keys

    @property
    def parameter_keys(self):
        if len(self._parameter_keys) == 0:
            self.__parse_xml()
        return self._parameter_keys

    @property
    def settings(self):
        if len(self._settings) == 0:
            conf = ConfigParser.ConfigParser()
            settings_abs_file = os.path.abspath(self.settings_file)
            conf.read(settings_abs_file)
            for (key,val) in conf.items("parameters"):
                self._settings[key] = val
        return self._settings

    def wait_for_input(self):
        loop = True

        while loop != False :
            c = self.render()
            #print(self)
            #c = sys.stdin.readline().strip()
            if( c == ""):
                return
                #sys.exit(0)
            else:
                for shortcut in self.shortcut_keys:
                    if c.upper() == shortcut['key'] :
                        command = shortcut['command']
                        if command.endswith('()'): #python code  unix.a
                            command =command.replace('()','')
                            if command.find(".") > -1:  ##to enter sub menu screen, parse unix.Sybase()
                                items = command.split('.')
                                dir_path = os.path.abspath(items[0])
                                sys.path.append(dir_path)
                                module01 = __import__(items[0])       #file name
                                cls = getattr(module01, items[1])     #class
                                obj = cls()
                                obj.wait_for_input()
                            else:
                                getattr(self,command)()
                                #eval(command)()
                        else:  #should be other script file to be executed
                            cmd_abs_path = os.path.abspath(shortcut['command'])
                            cmd = [cmd_abs_path]
                            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                            output = proc.stdout.read()
                            #show output in screen
                            print output
                            #log outptu
                            self.logger.info(output)






