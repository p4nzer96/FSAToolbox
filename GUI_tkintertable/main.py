#!/usr/bin/env python
from __future__ import absolute_import, division, print_function




# from tkintertable import TableCanvas, TableModel


#import Pmw
import re, sys, os, time, pickle

script_dir = os.path.dirname( __file__ )
tkintertable_dir = os.path.join( script_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(tkintertable_dir)

from collections import OrderedDict
from tkintertable.Custom import MyTable
from tkintertable.TableModels import TableModel
from tkintertable.Tables_IO import TableImporter
from tkintertable.Prefs import Preferences

from tkinter import ttk
import json
import GUI_Utils
from loadfsa import *
from loadfsa_GUI import *

import time




try:
    from tkinter import *
    from tkinter.ttk import *
    import tkMessageBox
except:
    pass
    #from Tkinter import *
    #from ttk import *
if sys.version_info > (3, 0):
    from tkinter import filedialog, messagebox, simpledialog
    from tkinter import font
else:
    from tkinter import filedialog
    from tkinter import simpledialog
    from tkinter import messagebox
    from tkinter import font



class TablesApp(Frame):
    """
    Tables app
    """
    def __init__(self, parent=None, data=None, datafile=None):
        """Initialize the application."""
        #print("TablesApp__init__")
        super().__init__()
        self.parent = parent

        #If there is data to be loaded, show the dialog first
        if not self.parent:
            Frame.__init__(self)
            self.tablesapp_win = self.master
        else:
            self.tablesapp_win=Toplevel()

        # Get platform into a variable
        import platform
        self.currplatform=platform.system()
        if not hasattr(self,'defaultsavedir'):
            self.defaultsavedir = os.getcwd()

        self.preferences=Preferences('TablesApp',{'check_for_update':1})
        self.loadprefs()
        self.tablesapp_win.title('FSA Table Application')
        self.tablesapp_win.geometry('+200+200')
        self.x_size=800
        self.y_size=600
        self.createMenuBar()
        self.apptoolBar = ToolBar(self.tablesapp_win, self)
        self.apptoolBar.pack(fill=BOTH, expand=NO)
        # add find bar TODO
        # self.createSearchBar()

        if data != None:
            self.data = data
            self.new_project(data)
        elif datafile != None:
            self.open_project(datafile)
        else:
            self.new_project()

        self.tablesapp_win.protocol('WM_DELETE_WINDOW',self.quit)
        return

    def createMenuBar(self):
        """Create the menu bar for the application. """
        #print("createMenuBar")
        self.menu = Menu(self.tablesapp_win)
        '''
        self.proj_menu={'01New':{'cmd':self.new_project},
                        '02Open':{'cmd':self.open_project},
                        '03Import file on table(.txt,.fsa,.csv,.json)': {'cmd':self.import_file},
                        '04Analyze file(.txt,.fsa,.csv,.json)': {'cmd': self.just_analyze_file},
                        '05Close':{'cmd':self.close_project},
                        '06Save':{'cmd':self.save_project},
                        '07Save As':{'cmd':self.save_as_project},
                        '08Preferences..':{'cmd':self.showPrefsDialog},
                        '09Quit':{'cmd':self.quit}}
        '''
        self.proj_menu={'01New':{'cmd':self.new_project},
                        '02Close':{'cmd':self.close_project},
                        '03Preferences..':{'cmd':self.showPrefsDialog},
                        '04Quit':{'cmd':self.quit}}

        if self.parent:
            self.proj_menu['08Return to Database']={'cmd':self.return_data}
        self.proj_menu=self.create_pulldown(self.menu,self.proj_menu)
        self.menu.add_cascade(label='Project',menu=self.proj_menu['var'])

        '''
        self.records_menu={'01Add Row':{'cmd':self.add_Row},
                         '02Delete Row':{'cmd':self.delete_Row},
                         '03Add Column':{'cmd':self.add_Column},
                         '04Delete Column':{'cmd':self.delete_Column},
                         '05Auto Add Rows':{'cmd':self.autoAdd_Rows},
                         '06Auto Add Columns':{'cmd':self.autoAdd_Columns},
                         '07Find':{'cmd':self.createSearchBar},
                         '08From table to Json': {'cmd': self.from_Table_To_Json},
                         '09Analyze FSA': {'cmd': self.analyze_FSA},
                         }
        '''
        self.edit_menu={'01Add Row(s)':{'cmd':self.autoAdd_Rows},
                         '02Add Column':{'cmd':self.add_Column}
                         }

        self.edit_menu=self.create_pulldown(self.menu,self.edit_menu)
        self.menu.add_cascade(label='Edit',menu=self.edit_menu['var'])

        #self.sheet_menu={'01Add Sheet':{'cmd':self.add_Sheet}, '02Remove Sheet':{'cmd':self.delete_Sheet}, '03Copy Sheet':{'cmd':self.copy_Sheet}, '04Rename Sheet':{'cmd':self.rename_Sheet} }
        self.sheet_menu = {'01Rename Sheet': {'cmd': self.rename_Sheet},}
        self.sheet_menu=self.create_pulldown(self.menu,self.sheet_menu)
        # self.menu.add_cascade(label='Sheet',menu=self.sheet_menu['var'])
        self.menu.add_cascade(label='Sheet name', menu=self.sheet_menu['var'])

        self.analyze_file_menu={'01Analyze file(.txt,.fsa,.csv,.json)': {'cmd': self.just_analyze_file}}

        self.analyze_file_menu=self.create_pulldown(self.menu,self.analyze_file_menu)
        self.menu.add_cascade(label='Analyze file',menu=self.analyze_file_menu['var'])

        #self.IO_menu={'01Import from csv file':{'cmd':self.import_csv},'02Export to csv file':{'cmd':self.export_csv}}

        self.IO_menu={'01Import file on table(.txt,.fsa,.csv,.json)': {'cmd':self.import_file},
                      '02Export table to .csv file':{'cmd':self.export_csv},
                      '03Export table to .json file': {'cmd': self.from_Table_To_Json}
                      }

        self.IO_menu=self.create_pulldown(self.menu,self.IO_menu)
        self.menu.add_cascade(label='Import/Export',menu=self.IO_menu['var'])

        # Help menu

        #self.help_menu={'01Online Help':{'cmd':self.online_documentation},'02About':{'cmd':self.about_Tables}}
        self.help_menu={'01How to populate a .txt or .fsa file': {'cmd': self.help_how_populate_txt_or_fsa},
                        '02How to populate a .csv file': {'cmd': self.help_how_populate_csv},
                        '03How to populate a .json file': {'cmd': self.help_how_populate_json}}

        self.help_menu=self.create_pulldown(self.menu,self.help_menu)
        self.menu.add_cascade(label='Help',menu=self.help_menu['var'])
        self.tablesapp_win.config(menu=self.menu)
        return

    def create_pulldown(self,menu,dict):
        """ Create a pulldown in var from the info in dict  """
        #print("create_pulldown")
        var = Menu(menu,tearoff=0)
        items = dict.keys()
        #items.sort()
        for item in items:
            if item[-3:]=='sep':
                var.add_separator()
            else:
                # Do we have a command?
                command=None
                if 'cmd' in  dict[item]:
                    command=dict[item]['cmd']

                # Put the command in there
                if 'sc' in dict[item]:
                    var.add_command(label='%-25s %9s' %(item[2:],dict[item]['sc']),command=command)
                else:
                    var.add_command(label='%-25s' %(item[2:]),command=command)
        dict['var']=var
        return dict

    def createSearchBar(self, event=None):
        """Add a find entry box"""
        #print("createSearchBar")
        frame = Frame(self.tablesapp_win)
        row=0
        def close():
            frame.destroy()
        self.findtext=StringVar()
        self.findbox=Entry(frame,textvariable=self.findtext,width=30,bg='white')
        self.findbox.grid(row=row,column=1,sticky='news',columnspan=2,padx=2,pady=2)
        self.findbox.bind('<Return>',self.do_find_text)
        Label(frame,text='Find:').grid(row=row,column=0,sticky='ew')
        self.findagainbutton=Button(frame,text='Find Again', command=self.do_find_again)
        self.findagainbutton.grid(row=row,column=3,sticky='news',padx=2,pady=2)
        self.cbutton=Button(frame,text='Close', command=close)
        self.cbutton.grid(row=row,column=4,sticky='news',padx=2,pady=2)
        frame.pack(fill=BOTH, expand=NO)
        return

    def loadprefs(self):
        """Setup default prefs file if any of the keys are not present"""
        #print("loadprefs")
        defaultprefs = {'textsize':14,
                         'windowwidth': 800 ,'windowheight':600}
        for prop in defaultprefs.keys():
            try:
                self.preferences.get(prop)
            except:
                self.preferences.set(prop, defaultprefs[prop])
        return

    def showPrefsDialog(self):
        #print("showPrefsDialog")
        self.prefswindow = self.currenttable.showtablePrefs()
        return

    def new_project(self, data=None):
        """Create a new table, with model and add the frame"""
        #print("new_project")
        if hasattr(self,'currenttable'):
            self.notebook.destroy()
            self.currenttable.destroy()

        #Create the sheets dict
        self.sheets = {}
        self.notebook = Notebook(self.tablesapp_win)
        self.notebook.pack(fill='both', expand=1, padx=4, pady=4)
        if data !=None:
            for s in data.keys():
                sdata = data[s]
                try:
                    self.add_Sheet(s ,sdata)
                except:
                    print ('skipping')
        else:
            #do the table adding stuff for the initial sheet
            self.add_Sheet('sheet1')
        #self.notebook.setnaturalsize()
        return

    def open_project(self, filename=None):
        #print("open_project")
        if filename == None:
            filename=filedialog.askopenfilename(defaultextension='.tblprj"',
                                                      initialdir=os.getcwd(),
                                                      filetypes=[("TableApp project","*.tblprj"),
                                                                 ("All files","*.*")],
                                                      parent=self.tablesapp_win)
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
            data = pickle.load(fd)
            fd.close()
        self.new_project(data)
        self.filename=filename
        return

    def save_project(self):
        #print("save_project")
        if not hasattr(self, 'filename'):
            self.save_as_project()
        elif self.filename == None:
            self.save_as_project()
        else:
            self.do_save_project(self.filename)
        return

    def save_as_project(self):
        """Save as a new filename"""
        #print("save_as_project")
        filename=filedialog.asksaveasfilename(parent=self.tablesapp_win,
                                                defaultextension='.tblprj',
                                                initialdir=self.defaultsavedir,
                                                filetypes=[("TableApp project","*.tblprj"),
                                                           ("All files","*.*")])
        if not filename:
            print ('Returning')
            return
        self.filename=filename
        self.do_save_project(self.filename)
        return

    def do_save_project(self, filename):
        """Get model dicts and write all to pickle file"""
        #print("do_save_project")
        data = {}
        for s in self.sheets.keys():
            currtable = self.sheets[s]
            model = currtable.getModel()
            data[s] = model.getData()
        fd=open(filename,'wb')
        pickle.dump(data,fd)
        fd.close()
        return

    def just_analyze_file(self, filename=None):
        """Just analyze the imported file description of the fsa (txt, .fsa, .json or .csv)
        and report the Analysis results on the Results window"""
        #print("just_analyze_file")
        if filename == None:
            filename = filedialog.askopenfilename(defaultextension='.txt',
                                                  initialdir=os.getcwd(),
                                                  filetypes=[("Text files","*.txt"),
                                                             ("fsa files", "*.fsa"),
                                                             ("csv files","*.csv"),
                                                             ("json files","*.json"),
                                                             ("All files","*.*")],
                                                  parent=self.tablesapp_win)


        if os.path.isfile(filename):
            path_components = filename.split("/")
            sheet_name = path_components[-1]
            extension = os.path.splitext(filename)
            if ".txt" in extension or ".fsa" in extension:
                sheet_name = sheet_name.replace(".txt", "")
                sheet_name = sheet_name.replace(".fsa", "")
            elif ".json" in extension:
                sheet_name = sheet_name.replace(".json", "")
            elif ".csv" in extension:
                sheet_name = sheet_name.replace(".csv", "")

            GUI_Utils.last_sheet = sheet_name
            self.copy_Sheet(sheet_name)
            self.delete_Sheet()



        # from fsatoolbox.fsa import fsa
        # from loadfsa_GUI import fsa_GUI
        import analysis
        from tkinter import Button, Text, BOTH, StringVar
        from tkinter.ttk import Frame
        from GUI_Utils import TablesApp

        f = fsa_GUI()
        f.from_file_GUI(filename)

        X = f.X
        E = f.E
        x0 = f.x0
        Xm = f.Xm
        delta = f.delta
        # print(f)

        num_elements_per_row = 5
        text_content = "FSA name: " + GUI_Utils.last_sheet + "\n"
        text_content += "___________________________\n"

        dict_max_chars_per_row_found = {}

        if x0:
            # states
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            num_rows = 0
            text_states = ""
            text_states += "States: ["
            num_chars_per_line += len(text_states)
            max_chars_per_row_found = len(text_states)
            for i in range(len(X) - 1):
                current_text = str(X[i].label) + ", "
                text_states += current_text
                num_states_per_row += 1
                num_chars_per_line += len(current_text)
                if num_states_per_row >= num_elements_per_row:
                    text_states += "\n            "
                    num_states_per_row = 0
                    if num_rows == 0:
                        max_chars_per_row_found = num_chars_per_line
                    else:
                        if num_chars_per_line > max_chars_per_row_found:
                            max_chars_per_row_found = num_chars_per_line
                    num_rows += 1
                    num_chars_per_line = 0
            text_states += str(X[len(X) - 1].label) + "]\n"
            text_content += text_states
            num_chars_per_line += len(str(X[len(X) - 1].label) + "]\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"states": max_chars_per_row_found})

            # initial states
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_initial_states = ""
            text_initial_states += "Initial states: ["
            num_chars_per_line += len(text_initial_states)
            max_chars_per_row_found = len(text_initial_states)
            for i in range(len(x0) - 1):
                current_text = str(x0[i].label) + ", "
                text_initial_states += current_text
                num_states_per_row += 1
                num_chars_per_line += len(current_text)
                if num_states_per_row >= num_elements_per_row:
                    text_initial_states += "\n                    "
                    num_states_per_row = 0
                    if num_rows == 0:
                        max_chars_per_row_found = num_chars_per_line
                    else:
                        if num_chars_per_line > max_chars_per_row_found:
                            max_chars_per_row_found = num_chars_per_line
                    num_rows += 1
                    num_chars_per_line = 0
            text_initial_states += str(x0[len(x0) - 1].label) + "]\n"
            text_content += text_initial_states
            num_chars_per_line += len(str(x0[len(x0) - 1].label) + "]\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"init_states": max_chars_per_row_found})

            # final states
            text_final_states = ""
            if Xm:
                num_rows = 0
                max_chars_per_row_found = 0
                num_chars_per_line = 0
                num_states_per_row = 0
                text_final_states += "Final states: ["
                num_chars_per_line += len(text_final_states)
                max_chars_per_row_found = len(text_final_states)
                for i in range(len(Xm) - 1):
                    current_text = str(Xm[i].label) + ", "
                    text_final_states += current_text
                    num_states_per_row += 1
                    num_chars_per_line += len(current_text)
                    if num_states_per_row >= num_elements_per_row:
                        text_final_states += "\n                   "
                        num_states_per_row = 0
                        if num_rows == 0:
                            max_chars_per_row_found = num_chars_per_line
                        else:
                            if num_chars_per_line > max_chars_per_row_found:
                                max_chars_per_row_found = num_chars_per_line
                        num_rows += 1
                        num_chars_per_line = 0
                text_final_states += str(Xm[len(Xm) - 1].label) + "]\n"
                num_chars_per_line += len(str(Xm[len(Xm) - 1].label) + "]\n")
                text_content += text_final_states
            else:
                text_content += "Final states: []\n"
                num_chars_per_line += len("Final states: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"final_states": max_chars_per_row_found})

            # forbidden states
            text_forbidden_states = ""
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            num_forbidden_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].isForbidden == 1:
                    num_forbidden_states += 1
            if num_forbidden_states != 0:
                counter_forbidden_states = 0
                text_forbidden_states = ""
                text_forbidden_states += "Forbidden states: ["
                num_chars_per_line += len(text_forbidden_states)
                max_chars_per_row_found = len(text_forbidden_states)
                for i in range(len(X)):
                    if X[i].isForbidden == 1:
                        if counter_forbidden_states < num_forbidden_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_forbidden_states += 1
                        text_forbidden_states += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_forbidden_states += "\n                        "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                text_content += text_forbidden_states + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Forbidden states: []\n"
                num_chars_per_line += len("Forbidden states: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"forb_states": max_chars_per_row_found})

            text_content += "___________________________\n"

            # alphabet
            text_alphabet = ""
            if E:
                num_rows = 0
                max_chars_per_row_found = 0
                num_chars_per_line = 0
                num_events_per_row = 0
                text_alphabet = ""
                text_alphabet += "Alphabet: ["
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
                for i in range(len(E) - 1):
                    current_text = str(E[i].label) + ", "
                    text_alphabet += current_text
                    num_events_per_row += 1
                    num_chars_per_line += len(current_text)
                    if num_events_per_row >= num_elements_per_row:
                        text_alphabet += "\n                "
                        num_events_per_row = 0
                        if num_rows == 0:
                            max_chars_per_row_found = num_chars_per_line
                        else:
                            if num_chars_per_line > max_chars_per_row_found:
                                max_chars_per_row_found = num_chars_per_line
                        num_rows += 1
                        num_chars_per_line = 0
                text_alphabet += str(E[len(E) - 1].label) + "]\n"
                num_chars_per_line += len(str(E[len(E) - 1].label) + "]\n")
                text_content += text_alphabet
            else:
                text_content += "Alphabet: []\n"
                num_chars_per_line += len("Alphabet: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"alphabet": max_chars_per_row_found})

            # unobservable events
            text_alphabet = ""
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_events_per_row = 0
            num_unobservable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isObservable == 0:
                    num_unobservable_events += 1
            if num_unobservable_events != 0:
                counter_unobservable_events = 0
                text_alphabet = ""
                text_alphabet += "Unobservable events: ["
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isObservable == 0:
                        if counter_unobservable_events < num_unobservable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_unobservable_events += 1
                        text_alphabet += current_text
                        num_events_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_events_per_row >= num_elements_per_row:
                            text_alphabet += "\n                "
                            num_events_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
                text_content += text_alphabet + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Unobservable events: []\n"
                num_chars_per_line += len("Unobservable events: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"uo_events": max_chars_per_row_found})

            # uncontrollable events
            text_alphabet = ""
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_events_per_row = 0
            num_uncontrollable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isControllable == 0:
                    num_uncontrollable_events += 1
            if num_uncontrollable_events != 0:
                counter_uncontrollable_events = 0
                text_alphabet = ""
                text_alphabet += "Uncontrollable events: ["
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isControllable == 0:
                        if counter_uncontrollable_events < num_uncontrollable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_uncontrollable_events += 1
                        text_alphabet += current_text
                        num_events_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_events_per_row >= num_elements_per_row:
                            text_alphabet += "\n                                   "
                            num_events_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
                text_content += text_alphabet + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Uncontrollable events: []\n"
                num_chars_per_line += len("Uncontrollable events: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"uc_events": max_chars_per_row_found})

            # fault events
            text_alphabet = ""
            num_rows = 0
            num_events_per_row = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_fault_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isFault == 1:
                    num_fault_events += 1
            if num_fault_events != 0:
                counter_fault_events = 0
                text_alphabet = ""
                text_alphabet += "Fault events: ["
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isFault == 1:
                        if counter_fault_events < num_fault_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_fault_events += 1
                        text_alphabet += current_text
                        num_events_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_events_per_row >= num_elements_per_row:
                            text_alphabet += "\n                            "
                            num_events_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
                text_content += text_alphabet + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Fault events: []\n"
                num_chars_per_line += len("Fault events: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"f_events": max_chars_per_row_found})

            text_content += "___________________________\n"

            # delta relations
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_deltas_per_row = 0
            text_content += "Delta relations:\n"
            max_chars_per_row_found = len("Delta relations:\n")
            text_delta = ""
            if len(delta) != 0:
                for iter_X in range(len(X)):
                    current_start_filtered_deltas = f.filter_delta(start=str(X[iter_X].label), transition=None,
                                                                   end=None)
                    if len(current_start_filtered_deltas) == 0:
                        pass
                    else:
                        for iter_delta_row in range(len(current_start_filtered_deltas)):
                            if current_start_filtered_deltas.index[iter_delta_row] is not None:
                                current_text = "(" + str(
                                    current_start_filtered_deltas.iloc[iter_delta_row]["start"]) + ", " + str(
                                    current_start_filtered_deltas.iloc[iter_delta_row]["transition"]) + ", " + str(
                                    current_start_filtered_deltas.iloc[iter_delta_row]["end"]) + ")  "
                                text_delta += current_text
                                num_deltas_per_row += 1
                                num_chars_per_line += len(current_text)
                                if num_deltas_per_row >= num_elements_per_row:
                                    text_delta += "\n"
                                    num_deltas_per_row = 0
                                    if num_rows == 0:
                                        max_chars_per_row_found = num_chars_per_line
                                    else:
                                        if num_chars_per_line > max_chars_per_row_found:
                                            max_chars_per_row_found = num_chars_per_line
                                    num_rows += 1
                                    num_chars_per_line = 0
                            else:
                                pass
                text_content += text_delta + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += " []\n"
                num_chars_per_line += len(" []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"deltas": max_chars_per_row_found})

            # Reachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            is_reachable = analysis.get_reachability_info(f)
            text_content += "___________________________\n"
            text_content += "\nREACHABLE STATES\n"
            max_chars_per_row_found = len("\nREACHABLE STATES\n")
            text_content += "Reachable: ["
            num_chars_per_line += len("Reachable: [")
            text_reachability = ""
            num_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 1:
                    num_reachable_states += 1
            if num_reachable_states != 0:
                counter_reachable_states = 0
                for i in range(len(X)):
                    if X[i].is_Reachable:
                        if counter_reachable_states < num_reachable_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_reachable_states += 1
                        text_reachability += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_reachability += "\n                   "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_reachability += "]"
            text_content += text_reachability + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"reach_states": max_chars_per_row_found})

            # Unreachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not reachable: ["
            num_chars_per_line += len("Not reachable: [")
            max_chars_per_row_found = len("Not reachable: [")
            text_unreachability = ""
            num_unreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 0:
                    num_unreachable_states += 1
            counter_unreachable_states = 0
            if num_unreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_Reachable == 0:
                        if counter_unreachable_states < num_unreachable_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unreachable_states += 1
                        text_unreachability += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_unreachability += "\n                           "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_unreachability += "]"
                num_chars_per_line += len("]" + "\n")
            text_content += text_unreachability + "\n"
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_reach_states": max_chars_per_row_found})

            text_content += "FSA is reachable? "
            if is_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"

            # Co-Reachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            is_co_reachable = analysis.get_co_reachability_info(f)
            text_content += "___________________________\n"
            text_content += "\nCO-REACHABLE STATES\n"
            text_content += "Co-reachable: ["
            num_chars_per_line += len("Co-reachable: [")
            max_chars_per_row_found = len("\nCO-REACHABLE STATES\n")
            text_co_reachability = ""
            num_co_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 1:
                    num_co_reachable_states += 1
            counter_co_reachable_states = 0
            if num_co_reachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable:
                        if counter_co_reachable_states < num_co_reachable_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_co_reachable_states += 1
                        text_co_reachability += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_co_reachability += "\n                        "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_co_reachability += "]"
            text_content += text_co_reachability + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"co-reach_states": max_chars_per_row_found})

            # Not Co-Reachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not co-reachable: ["
            num_chars_per_line += len("Not co-reachable: [")
            max_chars_per_row_found = len("Not co-reachable: [")
            text_uncoreachability = ""
            num_uncoreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 0:
                    num_uncoreachable_states += 1
            counter_uncoreachable_states = 0
            if num_uncoreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable == 0:
                        if counter_uncoreachable_states < num_uncoreachable_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_uncoreachable_states += 1
                        text_uncoreachability += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_uncoreachability += "\n                                "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_uncoreachability += "]"
            text_content += text_uncoreachability + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_co-reach_states": max_chars_per_row_found})

            text_content += "FSA is co-reachable? "
            if is_co_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"

            # Blocking
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            is_blocking = analysis.get_blockingness_info(f)
            text_content += "___________________________\n"
            text_content += "\nBLOCKING STATES\n"
            max_chars_per_row_found = len("\nBLOCKING STATES\n")
            text_content += "Blocking: ["
            chars_count = len("Blocking: [")
            text_blocking = ""
            num_blocking_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Blocking == 1:
                    num_blocking_states += 1
            counter_blocking_states = 0
            if num_blocking_states != 0:
                for i in range(len(X)):
                    if X[i].is_Blocking:
                        if counter_blocking_states < num_blocking_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_blocking_states += 1
                        text_blocking += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_blocking += "\n               "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_blocking += "]"
            text_content += text_blocking + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"blocking": max_chars_per_row_found})

            # Not blocking
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not blocking: ["
            num_chars_per_line += len("Not blocking: [")
            max_chars_per_row_found = len("Not blocking: [")
            text_unblocking = ""
            num_unblocking_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Blocking == 0:
                    num_unblocking_states += 1
            counter_unblocking_states = 0
            if num_unblocking_states != 0:
                for i in range(len(X)):
                    if X[i].is_Blocking == 0:
                        if counter_unblocking_states < num_unblocking_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unblocking_states += 1
                        text_unblocking += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_unblocking += "\n                       "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_unblocking += "]"
            text_content += text_unblocking + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_blocking": max_chars_per_row_found})

            text_content += "FSA is blocking? "
            if is_blocking == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"

            # Dead
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            analysis.get_deadness_info(f)
            text_content += "___________________________\n"
            text_content += "\nDEAD STATES\n"
            max_chars_per_row_found = len("\nDEAD STATES\n")
            text_content += "Dead: ["
            num_chars_per_line += len("Dead: [")
            text_dead = ""
            num_dead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 1:
                    num_dead_states += 1
            counter_dead_states = 0
            if num_dead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead:
                        if counter_dead_states < num_dead_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_dead_states += 1
                        text_dead += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_dead += "\n                    "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_dead += "]"
            text_content += text_dead + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"dead": max_chars_per_row_found})

            # Not dead
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not dead: ["
            num_chars_per_line += len("Not dead: [")
            max_chars_per_row_found = len("Not dead: [")
            text_undead = ""
            num_undead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 0:
                    num_undead_states += 1
            counter_undead_states = 0
            if num_undead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead == 0:
                        if counter_undead_states < num_undead_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_undead_states += 1
                        text_undead += current_text
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_undead += "\n                  "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_undead += "]"
            text_content += text_undead + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_dead": max_chars_per_row_found})

            # Trim
            is_trim = analysis.get_trim_info(f)
            text_content += "___________________________\n"
            text_content += "\nTRIM\n"
            if is_trim == 1:
                text_content += "FSA is trim? YES\n"
            else:
                text_content += "FSA is trim? NO\n"

            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "___________________________\n"
            text_content += "\nREVERSIBILITY:\n"
            if is_reversible == 1:
                text_content += "FSA is reversible? YES\n"
            else:
                text_content += "FSA is reversible? NO\n"

        else:
            text_content = "Error: At least the initial state must be specified."

        import tkinter as tk
        import tkinter.scrolledtext as st

        # Creating tkinter window
        win = tk.Tk()
        win.title("Results window")

        # Title Label
        tk.Label(win,
                 text="FSA analysis results",
                 font=("Times New Roman", 17)).grid(column=0, row=0)

        # download button
        from tkinter.messagebox import showinfo

        def save_fsa_analysis_results():
            """Save as a new filename"""
            # print("save_fsa_analysis_results")
            ta = TablesApp(Frame)
            filename = filedialog.asksaveasfilename(parent=ta.tablesapp_win,
                                                    defaultextension='.txt',
                                                    initialdir=ta.defaultsavedir,
                                                    filetypes=[("Text file", "*.txt"),
                                                               ("All files", "*.*")])
            if not filename:
                print('Returning')
                return

            with open(filename, 'w') as fo:
                fo.write(text_content)
                fo.close()
            return

        width = 0

        for keymax in dict_max_chars_per_row_found:
            if dict_max_chars_per_row_found[keymax] > width:
                width = dict_max_chars_per_row_found[keymax]

        importButton = Button(win, text='Save on file', command=save_fsa_analysis_results, background="green",
                              foreground="white")
        importButton.grid(row=20, column=0, sticky='news', padx=2, pady=2)

        # Creating scrolled text area widget with Read only by disabling the state
        win.geometry()
        text_area = st.ScrolledText(win, width=width, height=30, font=("Times New Roman", 12))
        text_area.grid(column=0, pady=10, padx=10)

        # Inserting Text which is read only
        text_area.insert(tk.INSERT, text_content)

        # Making the text read only
        text_area.configure(state='disabled')
        win.mainloop()

    def import_file(self, filename=None):
        """Import and place on the current table the content of a file of extension .txt, .csv or .json"""
        # print("import_file")
        if filename == None:
            filename = filedialog.askopenfilename(defaultextension='.txt',
                                                  initialdir=os.getcwd(),
                                                  filetypes=[("Text files","*.txt"),
                                                             ("fsa files", "*.fsa"),
                                                             ("csv files","*.csv"),
                                                             ("json files","*.json"),
                                                             ("All files","*.*")],
                                                  parent=self.tablesapp_win)

        if os.path.isfile(filename):
            path_components = filename.split("/")
            sheet_name = path_components[-1]
            extension = os.path.splitext(filename)

            if ".txt" in extension or ".fsa" in extension:
                if ".txt" in extension:
                    sheet_name = sheet_name.replace(".txt", "")
                    GUI_Utils.last_extension = ".txt"
                if ".fsa" in extension:
                    sheet_name = sheet_name.replace(".fsa", "")
                    GUI_Utils.last_extension = ".fsa"
                GUI_Utils.last_sheet = sheet_name
                self.copy_Sheet(sheet_name)
                self.delete_Sheet()
                self.parse_txt_file_and_obtain_the_json(filename)
            elif ".json" in extension:
                sheet_name = sheet_name.replace(".json", "")
                GUI_Utils.last_sheet = sheet_name
                self.copy_Sheet(sheet_name)
                self.delete_Sheet()
                self.parse_json_file_and_populate_the_table(filename)
            elif ".csv" in extension:
                sheet_name = sheet_name.replace(".csv", "")
                GUI_Utils.last_sheet = sheet_name
                self.copy_Sheet(sheet_name)
                self.delete_Sheet()
                self.parse_csv_file_and_populate_the_table(filename)
            else:
                text_content = "\r\nThe file you selected has extension not allowed. \r\n Please insert only '.txt, '.fsa', '.csv' or '.json' files.\r\n"
                #print(text_content)
                win = Tk()
                # Set the geometry of Tkinter frame
                win.geometry()
                win['background'] = '#fc5a27'
                win.title("Error parsing the file")
                Label(win, text=text_content, font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
                # Create a button in the main Window to open the popup
                win.mainloop()
                return




    def parse_txt_file_and_obtain_the_json(self, filename=None):
        """Parse the .txt file describing the fsa and convert it to a json file"""
        # print("parse_txt_file_and_obtain_the_json")
        # print("****************************************************************************************************************************")
        # print("**                                                                                                                        **")
        # print("**                                                                                                                        **")
        # print("**                                                                                                                        **")
        # print("**                                          parse_txt_file_and_obtain_the_json                                            **")
        # print("**                                                                                                                        **")
        # print("**                                                                                                                        **")
        # print("****************************************************************************************************************************")

        
        print("\r\n\r\n" + time.ctime() + "\n" + chr(62) + "   Loading {}{} ...".format(GUI_Utils.last_sheet, GUI_Utils.last_extension))
        fd = open(filename, mode='rt')
        print("... successfully loaded {}{}.\r\n".format(GUI_Utils.last_sheet, GUI_Utils.last_extension))

        lines = fd.readlines()
        clean_lines = []

        counter_not_allowed_empty_lines = 0
        list_not_allowed_empty_lines = []
        for iter_list in range(len(lines)):
            clean_lines.append(lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")
            clean_lines[iter_list] = re.sub(" +", " ", clean_lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].split(" ")
            if clean_lines[iter_list][0] == '' and len(clean_lines[iter_list]) == 1:
                counter_not_allowed_empty_lines += 1
                if counter_not_allowed_empty_lines >= 2 or iter_list == len(lines) - 1:
                    list_not_allowed_empty_lines.append(iter_list + 1)
            else:
                counter_not_allowed_empty_lines = 0
                try:
                    while True:
                        clean_lines[iter_list].remove('')
                except ValueError:
                    pass
        fd.close()


        if len(clean_lines) == 0:
            print("Syntax error:\t\t\tThe file is empty. Please fill it.")
            win = Tk()
            # Set the geometry of Tkinter frame
            # win.geometry(win_geometry)
            win.geometry()
            win.title("Error parsing the file")
            win['background'] = '#fc5a27'
            Label(win,
                  text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + GUI_Utils.last_extension + "':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                                                       "(Look at the terminal to see all the errors)\r\n\n"
                                                                                                                       "Click the button below if you want to see an example on how to correctly populate the file.",
                  font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()
            win.mainloop()
            return



        flag_missing_num_states = 0
        if clean_lines[0][0] != '':
            if clean_lines[0][0].isnumeric() is not True:
                flag_missing_num_states = 1
                print(
                    "Syntax error in line 1:\t\t\t\tThe number of states specified at the beginning of the file ('{}') is not an 'integer', please modify it.".format(
                        clean_lines[0][0]))
        else:
            flag_missing_num_states = 1
            print(
                "Syntax error in line 1:\t\t\t\tThe number of states must be specified at the beginning of the file, please insert it.")




        if len(list_not_allowed_empty_lines) != 0 or flag_missing_num_states == 1:
            if len(list_not_allowed_empty_lines) != 0:
                for iter_lnael in range(len(list_not_allowed_empty_lines)):
                    if(list_not_allowed_empty_lines[iter_lnael]<10):
                        print("Syntax error in line " + str(
                        list_not_allowed_empty_lines[iter_lnael]) + ":\t\t\t\tEmpty line not allowed. Please correct the error to continue the parsing.")
                    else:
                        print("Syntax error in line " + str(
                        list_not_allowed_empty_lines[iter_lnael]) + ":\t\t\tEmpty line not allowed. Please correct the error to continue the parsing.")

            win = Tk()
            # Set the geometry of Tkinter frame
            # win.geometry(win_geometry)
            win.geometry()
            win.title("Error parsing the file")
            win['background'] = '#fc5a27'
            Label(win,
                  text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + GUI_Utils.last_extension + "':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                            "(Look at the terminal to see all the errors)\r\n\n"
                                                                                            "Click the button below if you want to see an example on how to correctly populate the file.",
                  font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()
            win.mainloop()
            return

        dict_start_states = {}  # to populate column 0 with keys (states), and for every key a dictionary of info on isInitial, isFinal, isFault
        list_start_states = []  # the indexes of the list represent the row of the related the start_state value
        list_events = []  # to populate columnlabels with keys (events), and for every key a dictionary of info on isObservable, isControllable
        dict_events = {}
        dict_deltas = {}

        # try:

        num_states = int(clean_lines[0][0])

        flag_syntax_error = 0
        num_corrupted_states = 0

        index_row_start_states = 0
        index_column_events = 1  # the index '0' is for the column "States", so the events start from column '1'
        index_delta_events = 0
        current_start_state = ""
        flag_the_next_line_is_a_state = 0
        iter_lines = 1


        while iter_lines < len(clean_lines):
            if clean_lines[iter_lines][0] == '' and flag_the_next_line_is_a_state == 0:
                if len(dict_start_states) < num_states:
                    flag_the_next_line_is_a_state = 1
                    iter_lines += 1
                else:
                    break  # all the states and their deltas have been parsed, but there are other blank lines after
            elif flag_the_next_line_is_a_state == 1:
                current_start_state = str(clean_lines[iter_lines][0])
                if current_start_state not in dict_start_states:
                    try:
                        bool_init = (clean_lines[iter_lines][1] == '1' or clean_lines[iter_lines][1] == '0')
                        bool_final = (clean_lines[iter_lines][2] == '1' or clean_lines[iter_lines][2] == '0')
                        bool_forbidden = (clean_lines[iter_lines][3] == '1' or clean_lines[iter_lines][3] == '0')
                        if bool_init and bool_final and bool_forbidden:
                            dict_start_states.update({current_start_state: {"row": index_row_start_states,
                                                                            "line": iter_lines+1,
                                                                            "isInitial": clean_lines[iter_lines][1],
                                                                            "isFinal": clean_lines[iter_lines][2],
                                                                            "isForbidden": clean_lines[iter_lines][3]}})
                            list_start_states.append(current_start_state)
                            index_row_start_states += 1
                        else:
                            num_corrupted_states += 1
                            str_bool_init = ""
                            str_bool_final = ""
                            str_bool_forbidden = ""
                            if bool_init == 0:
                                str_bool_init = "\t\t\tcol 2('"+str(clean_lines[iter_lines][1])+"') must be '1' or '0'"
                            if bool_final == 0:
                                str_bool_final = "\t\t\tcol 3('"+str(clean_lines[iter_lines][2])+"') must be '1' or '0'"
                            if bool_forbidden == 0:
                                str_bool_forbidden = "\t\t\tcol 4('"+str(clean_lines[iter_lines][3])+"') must be '1' or '0'"
                            flag_syntax_error = 1
                            print("Syntax error in state line " + str(iter_lines+1) + ':' + str(str_bool_init) + str(str_bool_final) + str(str_bool_forbidden)+'.')
                    except:
                        num_corrupted_states+=1
                        flag_syntax_error = 1
                        print("Syntax error in state line " + str(iter_lines + 1) + ":\t\t\tThe state properties of '{}' are not completely defined (insert in order Initial(1/0), Final(1/0), Forbidden(1/0) after the state)." .format(current_start_state))

                else:
                    flag_syntax_error = 1
                    print("Syntax error in state line " + str(iter_lines+1) + ":\t\t\tMultiple occurrence of the state '{}', already specified in line {}." .format(current_start_state, dict_start_states[current_start_state]["line"]))
                flag_the_next_line_is_a_state = 0
                iter_lines += 1
            elif clean_lines[iter_lines][0] != '' and flag_the_next_line_is_a_state == 0 and len(clean_lines[iter_lines]) >= 5:
                bool_c_uc = (clean_lines[iter_lines][2] == 'c' or clean_lines[iter_lines][2] == 'uc')
                bool_o_uo = (clean_lines[iter_lines][3] == 'o' or clean_lines[iter_lines][3] == 'uo')
                bool_f_uf = (clean_lines[iter_lines][4] == 'f' or clean_lines[iter_lines][4] == 'uf')
                if bool_c_uc and bool_o_uo and bool_f_uf:
                    flag_end_current_start_state = 0
                    current_iter_line = str(iter_lines + 1) + '-'
                    while flag_end_current_start_state == 0:
                        bool_event = 0
                        current_event = clean_lines[iter_lines][0]
                        if len(clean_lines[iter_lines]) >= 5:
                            bool_event = current_event in dict_events and \
                                         (clean_lines[iter_lines][2] != dict_events[current_event]["isControllable"] \
                                          or clean_lines[iter_lines][3] != dict_events[current_event]["isObservable"] \
                                          or clean_lines[iter_lines][4] != dict_events[current_event]["isFault"])

                            if clean_lines[iter_lines][0] not in dict_events:
                                current_iter_line += str(iter_lines + 1) + '-'
                                dict_events.update({clean_lines[iter_lines][0]: {"column": index_column_events,
                                                                                 "line": iter_lines + 1,
                                                                                 "isControllable": clean_lines[iter_lines][2],
                                                                                 "isObservable": clean_lines[iter_lines][3],
                                                                                 "isFault": clean_lines[iter_lines][4]}})
                                list_events.append(clean_lines[iter_lines][0])
                                dict_deltas.update({str(index_delta_events): {"line": current_iter_line,
                                                                              "start": current_start_state,
                                                                              "name": current_event,
                                                                              "ends": clean_lines[iter_lines][1]}})
                                index_column_events += 1
                                index_delta_events += 1
                            elif clean_lines[iter_lines][0] in dict_events:
                                current_end_state = clean_lines[iter_lines][1]
                                current_event_end_states = current_end_state
                                current_event = clean_lines[iter_lines][0]
                                current_iter_line += str(iter_lines + 1)+'-'
                                for key in range(index_delta_events):
                                    if (str(key) in dict_deltas) and dict_deltas[str(key)]["name"] == \
                                            clean_lines[iter_lines][0] and dict_deltas[str(key)]["start"] == current_start_state:
                                        current_event_end_states = current_event_end_states + "-" + dict_deltas[str(key)]["ends"]
                                        del dict_deltas[str(key)]

                                dict_deltas.update({str(index_delta_events): {"line": current_iter_line,
                                                                              "start": current_start_state,
                                                                              "name": current_event,
                                                                              "ends": current_event_end_states}})
                                index_delta_events += 1
                        else:
                            flag_syntax_error = 1
                            bool_event = 0
                            print("Syntax error in event line " + str(
                                iter_lines + 1) + ":\t\t\tFive column elements are required in this event line, or maybe it is needed a blank line above this line.")

                        if (iter_lines + 1) < len(clean_lines) and clean_lines[iter_lines + 1][0] != '':
                            iter_lines += 1  # reiteration of while flag_end_current_start_state == 0:
                            flag_the_next_line_is_a_state = 0
                        else:
                            iter_lines += 1  # reiteration of while iter_lines < len(clean_lines):
                            flag_end_current_start_state = 1  # exit from the while loop
                            flag_the_next_line_is_a_state = 0

                        if bool_event == 1:
                            flag_syntax_error = 1
                            print("Syntax error in event line " + str(iter_lines) + ":\t\t\tThe event in this line ('{}') has different properties respect to its first declaration in line {}." .format(current_event, dict_events[current_event]["line"]))

                else:
                    str_bool_c_uc = ""
                    str_bool_o_uo = ""
                    str_bool_f_uf = ""
                    if bool_c_uc == 0:
                        str_bool_c_uc = "\t\t\tcol 3('"+str(clean_lines[iter_lines][2])+"') must be 'c' or 'uc'"
                    if bool_o_uo == 0:
                        str_bool_o_uo = "\t\t\tcol 4('"+str(clean_lines[iter_lines][3])+"') must be 'o' or 'uo'"
                    if bool_f_uf == 0:
                        str_bool_f_uf = "\t\t\tcol 5('"+str(clean_lines[iter_lines][4])+"') must be 'f' or 'uf'"
                    flag_syntax_error = 1
                    print("Syntax error in event line " + str(iter_lines+1) + ':' + str(str_bool_c_uc) + str(str_bool_o_uo) + str(str_bool_f_uf)+ '.')
                    iter_lines += 1
            elif clean_lines[iter_lines][0] != '' and flag_the_next_line_is_a_state == 0 and len(clean_lines[iter_lines]) < 5:
                flag_syntax_error = 1
                print("Syntax error in event line " + str(iter_lines+1) + ":\t\t\tFive column elements are required in this event line.")
                iter_lines += 1
        if len(dict_start_states)+num_corrupted_states != num_states:
            flag_syntax_error = 1
            print("Syntax error in line 1:\t\t\t\tThe number of possible states found in the file ({}) does not correspond to the number of states specified at the beginning of the file ({})." .format(len(dict_start_states)+num_corrupted_states, num_states))

        for key_delta in dict_deltas:
            list_current_end_states = dict_deltas[key_delta]["ends"].split('-')
            list_current_lines = dict_deltas[key_delta]["line"].split('-')
            list_current_lines = list(reversed(list_current_lines))
            try:
                while True:
                    list_current_lines.remove('')
            except ValueError:
                pass
            del list_current_lines[-1]



            for i in range(len(list_current_end_states)):
                if list_current_end_states[i] not in dict_start_states:
                    flag_syntax_error = 1
                    print("Syntax error in event line " + str(
                        list_current_lines[i]) + ":\t\t\tThe end_state '{}' is not a defined state (or well defined).".format(
                        list_current_end_states[i]))
        for key_delta in dict_deltas:
            del dict_deltas[key_delta]["line"]


        # except
        if flag_syntax_error == 1:
            # Create an instance of Tkinter frame
            win = Tk()
            # Set the geometry of Tkinter frame
            # win.geometry("440x250")
            win.geometry()
            win.title("Error parsing the file")
            Label(win,
                  text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + str(GUI_Utils.last_extension) + "':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                            "(Look at the terminal to see all the errors)\r\n\n"
                                                                                            "Click the button below if you want to see an example on how to "
                                                                                            "correctly populate the file.",
                  font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
            win['background'] = '#fc5a27'
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()
            win.mainloop()
            return



        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        #print("before clear self.currenttable.model.columntypes: ", self.currenttable.model.columntypes)
        self.currenttable.model.columntypes.clear()
        #print("after clear self.currenttable.model.columntypes: ", self.currenttable.model.columntypes)
        GUI_Utils.dictcolControllableEvents.clear()
        GUI_Utils.dictcolObservableEvents.clear()
        GUI_Utils.dictcolFaultyEvents.clear()
        self.currenttable.model.addColumn("State")




        dict_event_suffixes = {}
        i = 1
        dict_col_label_widths = {}
        dict_col_label_widths.update({"0": len("State")})
        while len(self.currenttable.model.columnlabels) <= len(list_events):
            suffix_event = ""
            if "isObservable" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isObservable"] == "o":
                    GUI_Utils.setEventAsObservable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isObservable"] == "uo":
                    suffix_event += "_uo"
                    GUI_Utils.setEventAsUnobservable(self.currenttable, list_events[i - 1])
            else:
                GUI_Utils.setEventAsObservable(self.currenttable, list_events[i - 1])

            if "isControllable" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isControllable"] == "c":
                    GUI_Utils.setEventAsControllable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isControllable"] == "uc":
                    suffix_event += "_uc"
                    GUI_Utils.setEventAsUncontrollable(self.currenttable, list_events[i - 1])
            else:
                GUI_Utils.setEventAsControllable(self.currenttable, list_events[i - 1])

            if "isFault" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isFault"] == "f":
                    suffix_event += "_f"
                    GUI_Utils.setEventAsFaulty(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isFault"] == "uf":
                    GUI_Utils.setEventAsUnfaulty(self.currenttable, list_events[i - 1])
            else:
                GUI_Utils.setEventAsUnfaulty(self.currenttable, list_events[i - 1])


            dict_events[list_events[i - 1]]["label"] = list_events[i - 1] + suffix_event  # added now *************************************************


            dict_event_suffixes.update({list_events[i - 1]: suffix_event})
            self.currenttable.model.addColumn(list_events[i - 1]+suffix_event)
            num_chars = len(list_events[i - 1]+suffix_event)
            dict_col_label_widths.update({str(i): num_chars})
            i += 1

        while self.currenttable.model.getRowCount() < len(list_start_states):
            self.currenttable.model.addRow()

        while self.currenttable.model.getRowCount() > len(list_start_states):
            self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)

        # naming the rows of the column "States" with the start_states
        for i in range(len(list_start_states)):
            str_check = ""
            if "isInitial" in dict_start_states[list_start_states[i]]:
                str_check += "_i"
            if "isFinal" in dict_start_states[list_start_states[i]]:
                str_check += "_f"
            if "isForbidden" in dict_start_states[list_start_states[i]]:
                str_check += "_p"

            def return_suffix(str_check):
                suffix = ""
                if str_check == "_i_f_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                elif str_check == "_i_f":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                elif str_check == "_i_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                elif str_check == "_f_p":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                elif str_check == "_i":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                elif str_check == "_f":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                elif str_check == "_p":
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                return suffix

            self.currenttable.model.setValueAt(list_start_states[i]+return_suffix(str_check), i, 0)
            num_chars = len(list_start_states[i]+return_suffix(str_check))
            if num_chars > dict_col_label_widths["0"]:
                dict_col_label_widths.update({"0": num_chars})


        key_dict_deltas = 0
        counter_macro_deltas = 0
        # inserting records in the table cells
        while counter_macro_deltas < len(dict_deltas):
            if counter_macro_deltas >= len(dict_deltas):
                break
            if str(key_dict_deltas) in dict_deltas:
                column_index = self.currenttable.model.getColumnIndex(dict_deltas[str(key_dict_deltas)]["name"]+dict_event_suffixes[dict_deltas[str(key_dict_deltas)]["name"]])
                row_index = dict_start_states[dict_deltas[str(key_dict_deltas)]["start"]]["row"]
                list_cell_value_end_states = dict_deltas[str(key_dict_deltas)]["ends"].split("-")
                i = 0
                while i < len(list_cell_value_end_states):
                    current_value = list_cell_value_end_states[i]
                    num_occurrences = list_cell_value_end_states.count(current_value)
                    while num_occurrences > 1:
                        list_cell_value_end_states.remove(current_value)
                        num_occurrences = list_cell_value_end_states.count(current_value)
                        i += 1
                    i += 1

                string_cell_value_end_states = " ".join(map(str, list_cell_value_end_states))
                string_cell_value_end_states = re.sub(" +", "-", string_cell_value_end_states)
                self.currenttable.model.setValueAt(string_cell_value_end_states, row_index, column_index)

                num_chars = len(string_cell_value_end_states)
                if num_chars > dict_col_label_widths[str(column_index)]:
                    dict_col_label_widths.update({str(column_index): num_chars})
                counter_macro_deltas += 1
                key_dict_deltas += 1
            else:
                key_dict_deltas += 1
                pass

        # resize every column based on the max number of chars of each column
        for i in range(0, len(self.currenttable.model.columnlabels)):
            if dict_col_label_widths[str(i)] >= 10:
                width_col = 120 + (dict_col_label_widths[str(i)] - 10) * 10
                self.currenttable.resizeColumn(i, width_col)

        self.currenttable.redrawVisible()


        #print("dict_events: ", dict_events)
        #print("list_events: ", list_events)


        #print("before clear self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)
        self.currenttable.model.columnOrder.clear()
        #print("after clear self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)

        #print("after update self.currenttable.model.columntypes: ", self.currenttable.model.columntypes)

        self.currenttable.model.columnOrder.update({0: "State"})
        for i in range(1, len(self.currenttable.model.columnlabels)):
            self.currenttable.model.columnOrder.update({i: dict_events[list_events[i-1]]["label"]})
        #print("after update self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)
        '''
        for keyE in dict_events:
            print("dict_events[{}][column] = {}" .format(keyE, dict_events[keyE]["column"]))
        '''

        return





    def parse_json_file_and_populate_the_table(self, filename=None):
        """Parse the .json file describing the fsa and populate the current table with its data"""
        #print("parse_json_file_and_populate_the_table")
        #print("****************************************************************************************************************************")
        #print("**                                                                                                                        **")
        #print("**                                                                                                                        **")
        #print("**                                                                                                                        **")
        #print("**                                          parse_json_file_and_populate_the_table                                        **")
        #print("**                                                                                                                        **")
        #print("**                                                                                                                        **")
        #print("****************************************************************************************************************************")
        time.ctime()
        print("\r\n\r\n" + time.ctime() + "\n" + chr(62) + "   Loading {}.json ...".format(GUI_Utils.last_sheet))
        with open(filename) as json_file:
            data = json.load(json_file)
        print("... successfully loaded {}.json.\r\n".format(GUI_Utils.last_sheet))


        # ////////////////////////////////////checking syntax errors in the file///////////////////////////////////////
        flag_syntax_error = 0
        # check if the .json the 3 elements 'X', 'E' and 'delta'
        dict_events = {}
        if 'E' in data:
            dict_events = data["E"].copy()
            iter = 0
            for key in dict_events:
                dict_events[key].update({"column": iter})
                iter += 1

            # check if there are event properties of values different from 0 or 1
            list_events_without_all_3_properties = []
            list_events_without_right_prop_values = []
            flag_event_prop_not_complete = 0
            flag_event_prop_not_allowed = 0
            for keyE in dict_events:
                if "isControllable" not in dict_events[keyE] or "isObservable" not in dict_events[keyE] or "isFault" not in dict_events[keyE]:
                    list_events_without_all_3_properties.append(keyE)
                    flag_event_prop_not_complete = 1
                if "isControllable" in dict_events[keyE]:
                    bool_cont = (dict_events[keyE]["isControllable"] == 1 or dict_events[keyE]["isControllable"] == 0)
                    if bool_cont == 0:
                        list_events_without_right_prop_values.append(keyE)
                        flag_event_prop_not_allowed = 1
                if "isObservable" in dict_events[keyE]:
                    bool_obs = (dict_events[keyE]["isObservable"] == 1 or dict_events[keyE]["isObservable"] == 0)
                    if bool_obs == 0:
                        list_events_without_right_prop_values.append(keyE)
                        flag_event_prop_not_allowed = 1
                if "isFault" in dict_events[keyE]:
                    bool_fault = (dict_events[keyE]["isFault"] == 1 or dict_events[keyE]["isFault"] == 0)
                    if bool_fault == 0:
                        list_events_without_right_prop_values.append(keyE)
                        flag_event_prop_not_allowed = 1

            if flag_event_prop_not_complete == 1:
                flag_syntax_error = 1
                for i in range(len(list_events_without_all_3_properties)):
                    print("Syntax error:\t\t\tThe event '{}' has not all the properties declared ('isControllable', 'isObservable', 'isFault')." .format(list_events_without_all_3_properties[i]))
            if flag_event_prop_not_allowed == 1:
                flag_syntax_error = 1
                for i in range(len(list_events_without_right_prop_values)):
                    print("Syntax error:\t\t\tThe event '{}' has not all the properties of allowed values (only 1 or 0)." .format(list_events_without_right_prop_values[i]))
        else:
            print("Syntax error:\t\tElement 'E' (dictionary of the events) not found in the .json file. Please insert it.")
            flag_syntax_error = 1



        dict_start_states = {}
        if 'X' in data:
            dict_start_states = data["X"].copy()
            iter = 0
            for key in dict_start_states:
                dict_start_states[key].update({"row": iter})
                iter += 1

            # check if there are state properties of values different from 0 or 1
            list_states_without_all_3_properties = []
            list_states_without_right_prop_values = []
            flag_state_prop_not_complete = 0
            flag_state_prop_not_allowed = 0
            for keyX in dict_start_states:
                if "isInitial" not in dict_start_states[keyX] or "isFinal" not in dict_start_states[
                    keyX] or "isForbidden" not in dict_start_states[keyX]:
                    list_states_without_all_3_properties.append(keyX)
                    flag_state_prop_not_complete = 1
                if "isInitial" in dict_start_states[keyX]:
                    bool_init = (dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX]["isInitial"] == 0)
                    if bool_init == 0:
                        list_states_without_right_prop_values.append(keyX)
                        flag_state_prop_not_allowed = 1
                if "isFinal" in dict_start_states[keyX]:
                    bool_final = (dict_start_states[keyX]["isFinal"] == 1 or dict_start_states[keyX]["isFinal"] == 0)
                    if bool_final == 0:
                        list_states_without_right_prop_values.append(keyX)
                        flag_state_prop_not_allowed = 1
                if "isForbidden" in dict_start_states[keyX]:
                    bool_forb = (dict_start_states[keyX]["isForbidden"] == 1 or dict_start_states[keyX]["isForbidden"] == 0)
                    if bool_forb == 0:
                        list_states_without_right_prop_values.append(keyX)
                        flag_state_prop_not_allowed = 1

            if flag_state_prop_not_complete == 1:
                flag_syntax_error = 1
                for i in range(len(list_states_without_all_3_properties)):
                    print("Syntax error:\t\t\tThe state '{}' has not all the properties declared ('isInitial', 'isFinal', 'isForbidden')." .format(list_states_without_all_3_properties[i]))
            if flag_state_prop_not_allowed == 1:
                flag_syntax_error = 1
                for i in range(len(list_states_without_right_prop_values)):
                    print("Syntax error:\t\t\tThe state '{}' has not all the properties of allowed values (only 1 or 0)." .format(list_states_without_right_prop_values[i]))


            # check if there are more initial states
            flag_first_init_state = 0
            flag_more_init_states = 0
            list_other_initial_states = []
            initial_state = ""
            for keyX in dict_start_states:
                if "isInitial" in dict_start_states[keyX] and flag_first_init_state == 0 and (
                        dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX]["isInitial"] == "1"):
                    flag_first_init_state = 1
                    initial_state = keyX
                elif "isInitial" in dict_start_states[keyX] and flag_first_init_state == 1 and (
                        dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX]["isInitial"] == "1"):
                    list_other_initial_states.append(keyX)
                    flag_more_init_states = 1
                else:
                    pass
            if flag_more_init_states == 1:
                flag_syntax_error = 1
                for i in range(len(list_other_initial_states)):
                    print("Syntax error:\t\t\tThe state '{}' is set as Initial, but only the first initial state specified ('{}') can be considered as the Initial one." .format(list_other_initial_states[i], initial_state))
        else:
            print("Syntax error:\t\tElement 'X' (dictionary of the states) not found in the .json file. Please insert it.")
            flag_syntax_error = 1



        list_start_states = []
        list_start_states = list(dict_start_states.keys())
        list_events = list(dict_events.keys())
        dict_deltas = {}

        if 'delta' in data:
            iter = 0
            for key in data["delta"]:
                dict_deltas.update({str(iter): data["delta"][key]})
                iter += 1
        else:
            print("Syntax error:\t\tElement 'delta' (dictionary of deltas) not found in the .json file. Please insert it.")
            flag_syntax_error = 1

        # check if there are more states with the same label
        # not possible, since if there are more equal keys, only the last will be taken into account

        # check if there are more events with the same label
        # not possible, since if there are more equal keys, only the last will be taken into account

        flag_syntax_warning = 0
        # check if there are events with the same name as a state (Warning)
        if 'X' in data and 'E' in data:
            list_events_named_as_states = []
            flag_events_named_as_states = 0
            for keyX in dict_start_states:
                for keyE in dict_events:
                    if keyE == keyX:
                        flag_events_named_as_states = 1
                        list_events_named_as_states.append(keyE)
            if flag_events_named_as_states == 1:
                flag_syntax_warning = 1
                for i in range(len(list_events_named_as_states)):
                    print("Syntax warning:\t\t\tThe event '{}' has the same name as the state '{}'. Please ignore this warning if this is the correct set-up.".format(list_events_named_as_states[i], list_events_named_as_states[i]))

        # check if there are start-states or end-states of a delta transition not specified as states
        if 'X' in data and 'delta' in data:
            list_start_states_not_in_states = []
            list_end_states_not_in_states = []
            flag_start_states_not_in_states = 0
            flag_end_states_not_in_states = 0
            for keyDelta in dict_deltas:
                if "start" in dict_deltas[keyDelta] and dict_deltas[keyDelta]["start"] not in dict_start_states:
                    flag_start_states_not_in_states = 1
                    list_start_states_not_in_states.append({"key":keyDelta, "start": dict_deltas[keyDelta]["start"]})
                if "ends" in dict_deltas[keyDelta] and dict_deltas[keyDelta]["ends"] not in dict_start_states:
                    flag_end_states_not_in_states = 1
                    list_end_states_not_in_states.append({"key":keyDelta, "ends": dict_deltas[keyDelta]["ends"]})
            if flag_start_states_not_in_states == 1:
                flag_syntax_error = 1
                for i in range(len(list_start_states_not_in_states)):
                    print("Syntax error:\t\t\tThe start-state '{}' of the delta transition '{}' is not defined as a state in 'X'.".format(list_start_states_not_in_states[i]["start"], list_start_states_not_in_states[i]["key"]))
            if flag_end_states_not_in_states == 1:
                flag_syntax_error = 1
                for i in range(len(list_end_states_not_in_states)):
                    print("Syntax error:\t\t\tThe end-state '{}' of the delta transition '{}' is not defined as a state in 'X'.".format(list_end_states_not_in_states[i]["ends"], list_end_states_not_in_states[i]["key"]))


        # check if there are events of a delta transition not specified as events
        if 'E' in data and 'delta' in data:
            list_delta_events_not_in_events = []
            flag_delta_events_not_in_events = 0
            for keyDelta in dict_deltas:
                if "name" in dict_deltas[keyDelta] and dict_deltas[keyDelta]["name"] not in dict_events:
                    flag_delta_events_not_in_events = 1
                    list_delta_events_not_in_events.append({"key": keyDelta, "name": dict_deltas[keyDelta]["name"]})
            if flag_delta_events_not_in_events == 1:
                flag_syntax_error = 1
                for i in range(len(list_delta_events_not_in_events)):
                    print("Syntax error:\t\t\tThe event name '{}' of the delta transition '{}' is not defined as an event in 'E'.".format(list_delta_events_not_in_events[i]["name"], list_delta_events_not_in_events[i]["key"]))



        if flag_syntax_error == 1 or flag_syntax_warning == 1:
            win = Tk()
            # Set the geometry of Tkinter frame
            # win.geometry(win_geometry)
            win.geometry()
            win.title("Error parsing the file")
            win['background'] = '#fc5a27'
            Label(win,
                  text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + ".json':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                            "(Look at the terminal to see all the errors)\r\n\n"
                                                                                            "Click the button below if you want to see an example on how to "
                                                                                            "correctly populate the file.",
                  font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=open_popup_errors_on_json_file).pack()
            win.mainloop()

            if flag_syntax_error == 1:
                return

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////




        list_keys_already_done = []
        dict_start_state_events_already_done = {}
        for current_key in range(len(dict_deltas)):
            if str(current_key) in dict_deltas:
                current_start_state = dict_deltas[str(current_key)]["start"]
                current_event = dict_deltas[str(current_key)]["name"]
                current_ends = dict_deltas[str(current_key)]["ends"]
                list_keys_already_done.clear()
                flag_times_to_delete = 0
                for key in dict_deltas:
                    if dict_deltas[str(key)]["start"] == current_start_state and dict_deltas[str(key)]["name"] == current_event and key != str(current_key) and key not in list_keys_already_done and (dict_deltas[str(current_key)]["start"] not in dict_start_state_events_already_done and dict_deltas[str(current_key)]["name"] not in dict_start_state_events_already_done):
                        current_ends = current_ends + "-" + dict_deltas[str(key)]["ends"]
                        list_keys_already_done.append(key)
                        dict_start_state_events_already_done.update(dict_deltas[str(key)])
                        flag_times_to_delete = 1
                if flag_times_to_delete == 1:
                    dict_deltas[str(current_key)]["ends"] = current_ends
                    for i in range(len(list_keys_already_done)):
                        del dict_deltas[list_keys_already_done[i]]

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        self.currenttable.model.columntypes.clear()
        GUI_Utils.dictcolControllableEvents.clear()
        GUI_Utils.dictcolObservableEvents.clear()
        GUI_Utils.dictcolFaultyEvents.clear()
        self.currenttable.model.addColumn("State")
        i = 1

        dict_event_suffixes = {}
        dict_col_label_widths = {}
        dict_col_label_widths.update({"0": len("State")})

        while len(self.currenttable.model.columnlabels) <= len(list_events):
            suffix_event = ""
            if "isObservable" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isObservable"] == "1" or dict_events[list_events[i - 1]]["isObservable"] == 1:
                    GUI_Utils.setEventAsObservable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isObservable"] == "0" or dict_events[list_events[i - 1]]["isObservable"] == 0:
                    suffix_event += "_uo"
                    GUI_Utils.setEventAsUnobservable(self.currenttable, list_events[i - 1])
            else:
                GUI_Utils.setEventAsObservable(self.currenttable, list_events[i - 1])

            if "isControllable" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isControllable"] == "1" or dict_events[list_events[i - 1]]["isControllable"] == 1:
                    GUI_Utils.setEventAsControllable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isControllable"] == "0" or dict_events[list_events[i - 1]]["isControllable"] == 0:
                    suffix_event += "_uc"
                    GUI_Utils.setEventAsUncontrollable(self.currenttable, list_events[i - 1])
            else:
                GUI_Utils.setEventAsControllable(self.currenttable, list_events[i - 1])

            if "isFault" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isFault"] == "1" or dict_events[list_events[i - 1]]["isFault"] == 1:
                    suffix_event += "_f"
                    GUI_Utils.setEventAsFaulty(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isFault"] == "0" or dict_events[list_events[i - 1]]["isFault"] == 0:
                    GUI_Utils.setEventAsUnfaulty(self.currenttable, list_events[i - 1])
            else:
                GUI_Utils.setEventAsUnfaulty(self.currenttable, list_events[i - 1])

            dict_events[list_events[i - 1]]["label"] = list_events[i - 1] + suffix_event  # added now *************************************************

            dict_event_suffixes.update({list_events[i - 1]: suffix_event})
            num_chars = len(list_events[i - 1] + suffix_event)
            dict_col_label_widths.update({str(i): num_chars})
            self.currenttable.model.addColumn(list_events[i - 1]+dict_event_suffixes[list_events[i - 1]])
            i += 1

        while self.currenttable.model.getRowCount() < len(list_start_states):
            self.currenttable.model.addRow()

        while self.currenttable.model.getRowCount() > len(list_start_states):
            self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)

        # naming the rows of the column "States" with the start_states
        for i in range(len(list_start_states)):
            str_check = ""
            if "isInitial" in dict_start_states[list_start_states[i]]:
                str_check += "_i"
            if "isFinal" in dict_start_states[list_start_states[i]]:
                str_check += "_f"
            if "isForbidden" in dict_start_states[list_start_states[i]]:
                str_check += "_p"

            def return_suffix(str_check):
                suffix = ""
                if str_check == "_i_f_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                elif str_check == "_i_f":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                elif str_check == "_i_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                elif str_check == "_f_p":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                elif str_check == "_i":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                elif str_check == "_f":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                elif str_check == "_p":
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                return suffix

            self.currenttable.model.setValueAt(list_start_states[i]+return_suffix(str_check), i, 0)
            num_chars = len(list_start_states[i]+return_suffix(str_check))
            if num_chars > dict_col_label_widths["0"]:
                dict_col_label_widths.update({"0": num_chars})

        key_dict_deltas = 0
        counter_macro_deltas = 0
        # inserting records in the cells
        while counter_macro_deltas < len(dict_deltas):
            if counter_macro_deltas >= len(dict_deltas):
                break
            if str(key_dict_deltas) in dict_deltas:

                column_index = self.currenttable.model.getColumnIndex(dict_deltas[str(key_dict_deltas)]["name"]+dict_event_suffixes[dict_deltas[str(key_dict_deltas)]["name"]])
                row_index = dict_start_states[dict_deltas[str(key_dict_deltas)]["start"]]["row"]
                list_cell_value_end_states = dict_deltas[str(key_dict_deltas)]["ends"].split("-")
                i = 0
                while i < len(list_cell_value_end_states):
                    current_value = list_cell_value_end_states[i]
                    num_occurrences = list_cell_value_end_states.count(current_value)
                    while num_occurrences > 1:
                        list_cell_value_end_states.remove(current_value)
                        num_occurrences = list_cell_value_end_states.count(current_value)
                        i += 1
                    i += 1

                string_cell_value_end_states = " ".join(map(str, list_cell_value_end_states))
                string_cell_value_end_states = re.sub(" +", "-", string_cell_value_end_states)
                self.currenttable.model.setValueAt(string_cell_value_end_states, row_index, column_index)
                num_chars = len(string_cell_value_end_states)
                if num_chars > dict_col_label_widths[str(column_index)]:
                    dict_col_label_widths.update({str(column_index): num_chars})
                counter_macro_deltas += 1
                key_dict_deltas += 1
            else:
                key_dict_deltas += 1
                pass

        # resize every column based on the max number of chars of each column
        for i in range(0, len(self.currenttable.model.columnlabels)):
            if dict_col_label_widths[str(i)] >= 10:
                width_col = 120 + (dict_col_label_widths[str(i)] - 10) * 10
                self.currenttable.resizeColumn(i, width_col)

        self.currenttable.redrawVisible()

        #print("dict_events: ", dict_events)
        #print("list_events: ", list_events)


        #print("before clear self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)
        self.currenttable.model.columnOrder.clear()
        #print("after clear self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)

        #print("after update self.currenttable.model.columntypes: ", self.currenttable.model.columntypes)

        self.currenttable.model.columnOrder.update({0: "State"})
        for i in range(1, len(self.currenttable.model.columnlabels)):
            self.currenttable.model.columnOrder.update({i: dict_events[list_events[i-1]]["label"]})
        #print("after update self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)
        '''
        for keyE in dict_events:
            print("dict_events[{}][column] = {}" .format(keyE, dict_events[keyE]["column"]))
        '''

        json_file.close()
        return

    def parse_csv_file_and_populate_the_table(self, filename=None):
        """Parse the .csv file describing the fsa and populate the current table"""
        # print("parse_csv_file_and_populate_the_table")
        # print("****************************************************************************************************************************")
        # print("**                                                                                                                        **")
        # print("**                                                                                                                        **")
        # print("**                                          parse_csv_file_and_populate_the_table                                         **")
        # print("**                                                                                                                        **")
        # print("**                                                                                                                        **")
        # print("****************************************************************************************************************************")
        
        print("\r\n\r\n" + time.ctime() + "\n" + chr(62) + "   Loading {}.csv ...".format(GUI_Utils.last_sheet))
        with open(filename, encoding='utf-8') as csvf:
            fd = open(filename, mode='rt')
            print("... successfully loaded {}.csv.\r\n".format(GUI_Utils.last_sheet))
            lines = fd.readlines()
        clean_lines = []

        for iter_list in range(len(lines)):
            clean_lines.append(lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")
            clean_lines[iter_list] = re.sub(" +", "", clean_lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].split(",")
        fd.close()




        # Assigning a csv label to every column, like:
        # A ... Z      AA, AB, AC ... AZ      BA, BB, BC ... BZ     CA, CB, CC ... CZ     ZA, ZB, ZC ... ZZ     AAA, AAB, AAC ... AAZ   ABA, ABB, ABC ... ABZ
        csv_col_label = ['A']
        str_csv_col_label = ""
        current_iterating_csv_col_label = 0
        index_to_change = 0
        last_char_csv_col_label = ""
        dict_csv_col_label = {}
        for iter_col in range(len(clean_lines[0])):
            ascii_counter = 65 + iter_col % 26
            current_iterating_csv_col_label = chr(ascii_counter)
            csv_col_label[index_to_change] = current_iterating_csv_col_label

            str_csv_col_label = ''.join(csv_col_label)
            dict_csv_col_label.update({str(iter_col): str_csv_col_label})
            if ascii_counter >= 90:

                # ascii_counter_prev = 65 + iter_col % 26
                # current_iterating_csv_col_label += 1
                bool_all_Zs = all(element == 'Z' for element in csv_col_label)

                if bool_all_Zs:
                    num_current_chars_on_label = len(csv_col_label)
                    for i in range(num_current_chars_on_label):
                        csv_col_label[i] = 'A'
                    index_to_change = len(csv_col_label)
                    csv_col_label.insert(len(csv_col_label), 'A')
                    # index_to_change = num_current_chars_on_label

                else:
                    current_iterating_index = index_to_change
                    for j in range(current_iterating_index, 0, -1):
                        if csv_col_label[j] == 'Z' and csv_col_label[j - 1] != 'Z':
                            # index_to_change -= 1
                            index_to_change = current_iterating_index
                            csv_col_label[j] = 'A'
                            csv_col_label[j - 1] = chr(ord(csv_col_label[j - 1]) + 1)

        # check missing event name (empty event name but not empty column)
        flag_empty_event = 0
        for i in range(len(clean_lines[0])):
            temp_clean_lines_row0 = clean_lines[0][i]
            if temp_clean_lines_row0 == '':
                flag_empty_event = 1
                print("Syntax error in event col {}:\t\tEvent name not specified, please insert it.".format(
                    dict_csv_col_label[str(i)]))

        # check missing state name (empty state name but not empty row)
        flag_empty_state = 0
        for j in range(len(clean_lines)):
            if clean_lines[j][0] == '':
                flag_empty_state = 1
                print("Syntax error in row {}, col A:\t\tState name not specified, please insert it.".format(str(j+1)))

        if flag_empty_state == 1 or flag_empty_event == 1:
            win = Tk()
            # Set the geometry of Tkinter frame
            # win.geometry(win_geometry)
            text_cntnt = ""
            text_cntnt += "Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + ".csv':\r\n"
            if flag_empty_state == 1:
                text_cntnt += "- One or more of the State names are not specified (empty), please insert it/them.\r\n"
            if flag_empty_event == 1:
                text_cntnt += "- One or more of the event names are not specified (empty), please insert it/them.\r\n"
            text_cntnt += "\nPlease look at the terminal for more accurate info, and correct the content of the file.\n\n\nAlso click the button below if you want to see an example on how to correctly populate the file."
            win.geometry()
            win['background'] = '#fc5a27'
            win.title("Error parsing the file")
            Label(win, text=text_cntnt, font=('Helvetica 10 bold'), background='#fc9150', justify="left").pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
            win.mainloop()
            return

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        self.currenttable.model.columntypes.clear()
        GUI_Utils.dictcolControllableEvents.clear()
        GUI_Utils.dictcolObservableEvents.clear()
        GUI_Utils.dictcolFaultyEvents.clear()
        self.currenttable.model.addColumn("State")

        dict_events = {}
        dict_X = {}
        dict_delta = {}
        list_events = []
        dict_event_suffixes = {}
        dict_col_label_widths = {}
        dict_col_label_widths.update({"0": len("State")})

        flag_more_than_one_same_state = 0  # when in the column of states has been specified the same state more times
        flag_more_than_one_same_event = 0  # when has been specified the same event more times
        dict_events_first_csv_col = {}

        for i in range(1, len(clean_lines[0])):
            current_event = clean_lines[0][i]
            if clean_lines[0][i] and clean_lines[0][i] != '_':
                if current_event.endswith("_uc_f_uo") or current_event.endswith("_uc_uo_f") or current_event.endswith(
                        "_f_uc_uo") or current_event.endswith("_f_uo_uc") or current_event.endswith(
                    "_uo_f_uc") or current_event.endswith("_uo_uc_f"):
                    substring_to_remove = current_event[-8:]
                    current_event = current_event.replace(str(substring_to_remove), "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 0, "isControllable": 0, "isFault": 1}})
                elif current_event.endswith("_uc_f"):
                    current_event = current_event.replace("_uc_f", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 1, "isControllable": 0, "isFault": 1}})
                elif current_event.endswith("_f_uc"):
                    current_event = current_event.replace("_f_uc", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 1, "isControllable": 0, "isFault": 1}})
                elif current_event.endswith("_uc_uo"):
                    current_event = current_event.replace("_uc_uo", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 0, "isControllable": 0, "isFault": 0}})
                elif current_event.endswith("_uo_uc"):
                    current_event = current_event.replace("_uo_uc", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 0, "isControllable": 0, "isFault": 0}})
                elif current_event.endswith("_uo_f"):
                    current_event = current_event.replace("_uo_f", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 0, "isControllable": 1, "isFault": 1}})
                elif current_event.endswith("_f_uo"):
                    current_event = current_event.replace("_f_uo", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 0, "isControllable": 1, "isFault": 1}})
                elif current_event.endswith("_uc"):
                    current_event = current_event.replace("_uc", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 1, "isControllable": 0, "isFault": 0}})
                elif current_event.endswith("_f"):
                    current_event = current_event.replace("_f", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 1, "isControllable": 1, "isFault": 1}})
                elif current_event.endswith("_uo"):
                    current_event = current_event.replace("_uo", "")
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 0, "isControllable": 1, "isFault": 0}})
                else:
                    current_event = re.sub(" +", "", current_event)
                    if current_event not in dict_events:
                        dict_events_first_csv_col.update({current_event: i})
                    else:
                        flag_more_than_one_same_event = 1
                        print(
                            "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                                dict_csv_col_label[
                                    str(i)], current_event,
                                dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                    dict_events.update({current_event: {"col": i, "isObservable": 1, "isControllable": 1, "isFault": 0}})
                list_events.append(current_event)

                suffix_event = ""
                if "isObservable" in dict_events[current_event]:
                    if dict_events[current_event]["isObservable"] == 1:
                        GUI_Utils.setEventAsObservable(self.currenttable, current_event)
                    elif dict_events[current_event]["isObservable"] == 0:
                        suffix_event += "_uo"
                        GUI_Utils.setEventAsUnobservable(self.currenttable, current_event)
                else:
                    GUI_Utils.setEventAsUnobservable(self.currenttable, current_event)

                if "isControllable" in dict_events[current_event]:
                    if dict_events[current_event]["isControllable"] == 1:
                        GUI_Utils.setEventAsControllable(self.currenttable, current_event)
                    elif dict_events[current_event]["isControllable"] == 0:
                        suffix_event += "_uc"
                        GUI_Utils.setEventAsUncontrollable(self.currenttable, current_event)
                else:
                    GUI_Utils.setEventAsUncontrollable(self.currenttable, current_event)

                if "isFault" in dict_events[current_event]:
                    if dict_events[current_event]["isFault"] == 1:
                        suffix_event += "_f"
                        GUI_Utils.setEventAsFaulty(self.currenttable, current_event)
                    elif dict_events[current_event]["isFault"] == 0:
                        GUI_Utils.setEventAsUnfaulty(self.currenttable, current_event)
                else:
                    GUI_Utils.setEventAsUnfaulty(self.currenttable, current_event)

                dict_events[list_events[i - 1]]["label"] = list_events[i - 1] + suffix_event  # added now *************************************************

                dict_event_suffixes.update({current_event: suffix_event})
                self.currenttable.model.addColumn(current_event + suffix_event)
                num_chars = len(current_event + suffix_event)
                dict_col_label_widths.update({str(i): num_chars})

        dict_states_first_csv_row = {}
        # parsing states
        current_state = ""
        iter_delta_key = 0
        num_rows = len(clean_lines)
        num_cols = len(clean_lines[0])
        # ascii_counter = 65  # char A
        initial_state = ""
        flag_initial_state_found = 0
        dict_initial_states_found = {}
        iter_col = 0
        iter_row_ = 1
        for iter_row in range(1, num_rows):
            for iter_col in range(num_cols):
                if clean_lines[iter_row][iter_col] != None:
                    current_cell = clean_lines[iter_row][iter_col]
                    if iter_col == 0:
                        if current_cell[0] and current_cell[0] != '_':
                            if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                    "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                                "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith("_p_i_f"):
                                substring_to_remove = current_cell[-6:]
                                current_state = current_cell.replace(str(substring_to_remove), "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 1,
                                                          "isForbidden": 1}})
                                dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                                if flag_initial_state_found == 0:
                                    initial_state = str(current_state)
                                    flag_initial_state_found = 1

                            elif current_cell.endswith("_i_f"):
                                current_state = current_cell.replace("_i_f", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 1,
                                                          "isForbidden": 0}})
                                dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                                if flag_initial_state_found == 0:
                                    initial_state = str(current_state)
                                    flag_initial_state_found = 1

                            elif current_cell.endswith("_f_i"):
                                current_state = current_cell.replace("_f_i", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 1,
                                                          "isForbidden": 0}})
                                dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                                if flag_initial_state_found == 0:
                                    initial_state = str(current_state)
                                    flag_initial_state_found = 1

                            elif current_cell.endswith("_i_p"):
                                current_state = current_cell.replace("_i_p", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 0,
                                                          "isForbidden": 1}})
                                dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                                if flag_initial_state_found == 0:
                                    initial_state = str(current_state)
                                    flag_initial_state_found = 1

                            elif current_cell.endswith("_p_i"):
                                current_state = current_cell.replace("_p_i", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 0,
                                                          "isForbidden": 1}})
                                dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                                if flag_initial_state_found == 0:
                                    initial_state = str(current_state)
                                    flag_initial_state_found = 1

                            elif current_cell.endswith("_p_f"):
                                current_state = current_cell.replace("_p_f", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 1,
                                                          "isForbidden": 1}})

                            elif current_cell.endswith("_f_p"):
                                current_state = current_cell.replace("_f_p", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 1,
                                                          "isForbidden": 1}})

                            elif current_cell.endswith("_i"):
                                current_state = current_cell.replace("_i", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 0,
                                                          "isForbidden": 0}})
                                dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                                if flag_initial_state_found == 0:
                                    initial_state = str(current_state)
                                    flag_initial_state_found = 1

                            elif current_cell.endswith("_f"):
                                current_state = current_cell.replace("_f", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 1,
                                                          "isForbidden": 0}})

                            elif current_cell.endswith("_p"):
                                current_state = current_cell.replace("_p", "")
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 0,
                                                          "isForbidden": 1}})

                            else:
                                current_state = current_cell
                                current_state = re.sub(" +", " ", current_state)
                                if str(current_state) not in dict_X:
                                    dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                                else:
                                    flag_more_than_one_same_state = 1
                                    print(
                                        "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                            str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                            dict_states_first_csv_row[str(current_state)],
                                            dict_csv_col_label[str(iter_col)]))
                                dict_X.update(
                                    {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 0,
                                                          "isForbidden": 0}})
                        else:
                            # TODO: make a try except in this if-else
                            print("cell(" + str(iter_row) + "," + str(
                                iter_col) + " is not a valid name for a state.\nPlease insert a valid one.")
                    else:
                        current_delta_ends = current_cell.split("-")
                        flag_end_while = 0
                        while (flag_end_while == 0):
                            if '' in current_delta_ends:
                                current_delta_ends.remove('')
                            else:
                                flag_end_while = 1

                        for i in range(len(current_delta_ends)):
                            dict_delta.update({str(iter_delta_key): {"start": str(current_state),
                                                                     "name": list_events[iter_col - 1],
                                                                     "ends": str(current_delta_ends[i])}})
                            current_key_event = clean_lines[iter_row][iter_col]
                            iter_delta_key += 1
                else:
                    pass

        flag_zero_initial_states = 0
        flag_more_than_one_initial_state = 0
        counter_initial_states = 0

        for key_init in dict_initial_states_found:
            counter_initial_states += 1
            if dict_initial_states_found[key_init]["state"] != initial_state:
                print(
                    "Syntax error in row {}, col {}:\t\tAnother initial state has been specified ('{}'), while the first defined was already specified in row {} as '{}'.".format(
                        key_init,dict_csv_col_label[str(0)],
                        dict_initial_states_found[key_init]["state"], dict_states_first_csv_row[initial_state],
                        initial_state))

        if counter_initial_states > 1:
            flag_more_than_one_initial_state = 1
        elif counter_initial_states == 0:
            flag_zero_initial_states = 1

        flag_event_state = 0
        list_E = list(dict_events.keys())
        for keyX in dict_X:
            if keyX in list_E:
                flag_event_state = 1
                print(
                    "Warning shared names:\t\t\t\tThe event '{}' of col {} is named as the state '{}' of row {}. Please ignore this warning if this is the correct behaviour.".format(
                        keyX, dict_csv_col_label[str(dict_events[keyX]["col"])], keyX, dict_X[keyX]["row"]))

        flag_end_state_not_a_state = 0
        list_X = list(dict_X.keys())
        for keydelta in dict_delta:
            if dict_delta[keydelta]["ends"] not in list_X:
                flag_end_state_not_a_state = 1
                if flag_more_than_one_same_event == 0:
                    print(
                        "Syntax error in row {}, col {}:\t\tThe end state {} is not a valid state (not defined in the column 'State').".format(
                            dict_X[dict_delta[keydelta]["start"]]["row"],
                            dict_csv_col_label[str(dict_events[dict_delta[keydelta]["name"]]["col"])],
                            dict_delta[keydelta]["ends"]))

        flag_error = flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1

        if flag_event_state == 1 or flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
            title_content = "Error parsing the file"
            text_content = "Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + ".csv':\r\n"
            statements_counter = 0
            width_list = []
            if flag_zero_initial_states == 1:
                if flag_more_than_one_same_state == 1:
                    statements_counter += 1
                    text_content += str(
                        statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified or it could have been overwritten by the same 'state' specified more than once.\n"
                    width_list.append(950)
                else:
                    statements_counter += 1
                    text_content += str(
                        statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified.\n"
                    width_list.append(500)
            if flag_more_than_one_initial_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: only one 'state' can be specified as an 'initial state' (_i).\n"
                width_list.append(600)
            if flag_end_state_not_a_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: only 'states' specified in the column 'State' are allowed as 'end states' of a transition.\n"
                width_list.append(800)
            if flag_event_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".WARNING: one or many 'events' is/are named as a 'state' like those in the first column (ignore this warning if it is the desired behaviour).\n"
                width_list.append(1000)
            if flag_more_than_one_same_event == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: an 'event' can be defined only once (only one column per 'event').\n"
                width_list.append(600)
            if flag_more_than_one_same_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: a 'state' can be defined only once (only one row per 'state').\n"
                width_list.append(600)
            if flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                    or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
                text_content += "\nPlease look at the terminal for more accurate info, and correct the content of the file.\n\n\nAlso click the button below if you want to see an example on how to correctly populate the file."

            # auto-adapative height of the popup
            win_geometry_height = 100 + 52 * statements_counter
            width_popup = str(max(width_list)) + "x"
            win_geometry = width_popup + str(win_geometry_height)
            win = Tk()
            # Set the geometry of Tkinter frame
            # win.geometry(win_geometry)
            win.geometry()
            win.title(title_content)
            win['background'] = '#fc5a27'
            Label(win, text=text_content, font=('Helvetica 10 bold'), background='#fc9150', justify="left").pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
            win.mainloop()
            if flag_error == 1:
                return

        # adding or deleting rows
        while self.currenttable.model.getRowCount() < len(clean_lines) - 1:
            self.currenttable.model.addRow()

        while self.currenttable.model.getRowCount() > len(clean_lines) - 1:
            self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)

        # populating the table
        for row in range(1, len(clean_lines)):
            for col in range(0, len(clean_lines[0])):
                self.currenttable.model.setValueAt(clean_lines[row][col], row - 1, col)
                num_chars = len(clean_lines[row][col])
                if num_chars > dict_col_label_widths[str(col)]:
                    dict_col_label_widths.update({str(col): num_chars})
                if dict_col_label_widths[str(col)] >= 10:
                    width_col = 120 + (dict_col_label_widths[str(col)] - 10) * 10
                    self.currenttable.resizeColumn(col, width_col)

        self.currenttable.redrawVisible()


        #print("dict_events: ", dict_events)
        #print("list_events: ", list_events)


        #print("before clear self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)
        self.currenttable.model.columnOrder.clear()
        #print("after clear self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)

        #print("after update self.currenttable.model.columntypes: ", self.currenttable.model.columntypes)

        self.currenttable.model.columnOrder.update({0: "State"})
        for i in range(1, len(self.currenttable.model.columnlabels)):
            self.currenttable.model.columnOrder.update({i: dict_events[list_events[i-1]]["label"]})
        #print("after update self.currenttable.model.columnOrder: ", self.currenttable.model.columnOrder)
        '''
        for keyE in dict_events:
            print("dict_events[{}][column] = {}" .format(keyE, dict_events[keyE]["column"]))
        '''



        return

    def open_popup_errors_on_txt_file(self, win=None):
        """Open popup if some errors are present on the .txt file describing the fsa"""
        #print("open_popup_errors_on_txt_file")
        # Create an instance of tkinter frame
        self.example_win = Toplevel(win)
        # Set the geometry of tkinter frame
        self.example_win.geometry("1030x670")
        self.example_win.title("Example: how to populate a .txt of .fsa description file of the FSA")
        # Create a canvas
        canvas = Canvas(self.example_win, width=1000, height=670)
        # Load an image in the script
        img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_txt_file.png')
        # Add image to the Canvas Items
        canvas.create_image(10, 10, anchor=NW, image=img)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # adding the scrollbar on the right
        my_scrollbar = ttk.Scrollbar(self.example_win, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.example_win.mainloop()

        return

    def open_popup_errors_on_csv_file(self, win=None):
        """Open popup if some errors are present on the .csv file describing the fsa"""
        #print("open_popup_errors_on_csv_file")
        # Create an instance of tkinter frame
        self.example_win = Toplevel(win)
        # Set the geometry of tkinter frame
        self.example_win.geometry("770x755")
        self.example_win.title("Example: how to populate a .csv description file of the FSA")
        # Create a canvas
        canvas = Canvas(self.example_win, width=750, height=750)
        img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_csv_file.png')
        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(self.example_win, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.example_win.mainloop()
        return

    def open_popup_errors_on_json_file(self, win=None):
        """Open popup if some errors are present on the .json file describing the fsa"""
        from GUI_Utils import TablesApp
        # Create an instance of tkinter frame
        TablesApp.example_win = Toplevel()
        # Set the geometry of tkinter frame
        TablesApp.example_win.geometry("955x765")
        TablesApp.example_win.title("Example: how to populate a .json description file of the FSA")
        # Create a canvas
        canvas = Canvas(TablesApp.example_win, width=930, height=755)
        # Load an image in the script
        img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_json_file.png')
        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Adding a scrollbar on the right
        my_scrollbar = ttk.Scrollbar(TablesApp.example_win, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        TablesApp.example_win.mainloop()
        return



    def close_project(self):
        #print("close_project")
        if hasattr(self,'currenttable'):
            self.currenttable.destroy()
        return

    def import_csv(self):
        #print("import_csv")
        importer = TableImporter()
        #just use the dialog to load and import the file
        importdialog = importer.import_Dialog(self.tablesapp_win)
        self.tablesapp_win.wait_window(importdialog)
        model = TableModel()
        model.importDict(importer.data)
        sheetdata = {}
        sheetdata['sheet1'] = model.getData()
        self.new_project(sheetdata)
        return

    def export_csv(self):
        #print("export_csv")
        from tkintertable.Tables_IO import TableExporter
        exporter = TableExporter()
        exporter.ExportTableData(self.currenttable)
        return

    def add_Sheet(self, sheetname=None, sheetdata=None):
        """Add a new sheet - handles all the table creation stuff"""
        #print("add_Sheet")
        def checksheet_name(name):
            if name == '':
                messagebox.showwarning("Whoops", "Name should not be blank.")
                return 0
            if name in self.sheets:
                messagebox.showwarning("Name exists", "Sheet name already exists!")
                return 0
        names = [self.notebook.tab(i, "text") for i in self.notebook.tabs()]
        noshts = len(names)
        if sheetname == None:
            sheetname = simpledialog.askstring("New sheet name?", "Enter sheet name:",
                                                initialvalue='sheet'+str(noshts+1))
        checksheet_name(sheetname)
        page = Frame(self.notebook)
        self.notebook.add(page, text=sheetname)
        #Create the table and model if data present
        if sheetdata != None:
            model = TableModel(sheetdata)
            self.currenttable = MyTable(page, model)
        else:
            self.currenttable = MyTable(page)

        #Load preferences into table
        self.currenttable.loadPrefs(self.preferences)
        #This handles all the canvas and header in the frame passed to constructor
        self.currenttable.createTableFrame()
        #add the table to the sheet dict
        self.sheets[sheetname] = self.currenttable
        self.saved = 0
        return sheetname

    def delete_Sheet(self):
        """Delete a sheet"""
        #print("delete_Sheet")
        s = self.notebook.index(self.notebook.select())
        name = self.notebook.tab(s, 'text')
        #self.notebook.delete(s)
        self.notebook.forget(s)
        del self.sheets[name]
        return

    def copy_Sheet(self, newname=None):
        """Copy a sheet"""
        #print("copy_Sheet")
        newdata = self.currenttable.getModel().getData().copy()
        if newname==None:
            return
            # self.add_Sheet(None, newdata)
        else:
            self.add_Sheet(newname, newdata)
        return

    def rename_Sheet(self):
        """Rename a sheet"""
        #print("rename_Sheet")
        #s = self.notebook.getcurselection()
        s = self.notebook.index(self.notebook.select())
        newname = simpledialog.askstring("New sheet name?", "Enter new sheet name:",
                                                initialvalue=s)
        if newname == None:
            return
        GUI_Utils.last_sheet = newname
        self.copy_Sheet(newname)
        self.delete_Sheet()
        return

    def setcurrenttable(self, event):
        """Set the currenttable so that menu items work with visible sheet"""
        #print("setcurrenttable")
        try:
            #s = self.notebook.getcurselection()
            s = self.notebook.index(self.notebook.select())
            self.currenttable = self.sheets[s]
        except:
            pass
        return

    def add_Row(self):
        """Add a new row"""
        #print("add_Row")
        self.currenttable.addRow()
        self.saved = 0
        return

    def delete_Row(self):
        """Delete currently selected row"""
        #print("delete_Row")
        self.currenttable.deleteRow()
        self.saved = 0
        return

    def add_Column(self):
        """Add a new column"""
        #print("add_Column")
        self.currenttable.addColumn()
        self.saved = 0
        return

    def delete_Column(self):
        """Delete currently selected column in table"""
        #print("delete_Column")
        self.currenttable.deleteColumn()
        self.saved = 0
        return

    def from_Table_To_Json(self):
        """Convert the current table content into an FSA Json file description"""
        #print("from_Table_To_Json")
        # GUI_Utils.fromTableToJson(self.currenttable)
        GUI_Utils.fromTableToJson(self)
        self.saved = 0
        return

    def analyze_FSA(self):
        """Convert the current table content into a Json file"""
        #print("analyze_FSA")
        self.from_Table_To_Json()
        GUI_Utils.analyzeFsa(self.currenttable)
        self.saved = 0
        return

    def autoAdd_Rows(self):
        """Auto add x rows"""
        #print("autoAdd_Rows")
        # self.currenttable.autoAddRows()
        self.currenttable.addRows()

        self.saved = 0
        return

    def autoAdd_Columns(self):
        """Auto add x rows"""
        #print("autoAdd_Columns")
        self.currenttable.autoAddColumns()
        self.saved = 0
        return

    def findValue(self):
        #print("findValue")
        self.currenttable.findValue()
        return

    def do_find_text(self, event=None):
        """Find the text in the table"""
        #print("do_find_text")
        if not hasattr(self,'currenttable'):
            return
        import string
        if string.strip(self.findtext.get()) == '':
            return
        searchstring=self.findtext.get()
        if self.currenttable is not None:
            self.currenttable.findValue(searchstring)
        return

    def do_find_again(self, event=None):
        """Find again"""
        #print("do_find_again")
        if not hasattr(self,'currenttable'):
            return
        searchstring=self.findtext.get()
        if self.currenttable is not None:
            self.currenttable.findValue(searchstring, findagain=1)
        return

    def plot(self, event=None):
        #print("plot")
        self.currenttable.plotSelected()
        return

    def plotSetup(self, event=None):
        #print("plotSetup")
        self.currenttable.plotSetup()
        return

    def about_Tables(self):
        #print("about_Tables")
        self.ab_win=Toplevel()
        self.ab_win.geometry('+100+350')
        self.ab_win.title('About TablesApp')

        from tkintertable import Table_images
        logo = Table_images.tableapp_logo()
        label = Label(self.ab_win,image=logo)
        label.image = logo
        label.grid(row=0,column=0,sticky='news',padx=5,pady=5)

        text=['Tables Sample App ','Shows the use of Tablecanvas class for tkinter',
                'Copyright (C) Damien Farrell 2008-', 'This program is free software; you can redistribute it and/or',
                'modify it under the terms of the GNU General Public License',
                'as published by the Free Software Foundation; either version 2',
                'of the License, or (at your option) any later version.']
        row=1
        for line in text:
            tmp=Label(self.ab_win,text=line)
            tmp.grid(row=row,column=0,sticky='news',padx=4)
            row=row+1
        return

    def online_documentation(self,event=None):
        """Open the online documentation"""
        #print("online_documentation")
        import webbrowser
        link='http://sourceforge.net/projects/tkintertable/'
        webbrowser.open(link,autoraise=bool(1))
        return

    def help_how_populate_txt_or_fsa(self):
        """Open a popup showing an image describing how to populate a .txt or .fsa file to define an fsa"""
        #print("help_how_populate_txt_or_fsa")
        self.example_win = Toplevel()
        # Set the geometry of tkinter frame
        self.example_win.geometry("1020x670")
        self.example_win.title("Example: how to populate a .txt description file of the FSA")
        # Create a canvas
        canvas = Canvas(self.example_win, width=1000, height=670)
        # Load an image in the script
        img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_txt_file.png')
        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Adding a scrollbar on the right
        my_scrollbar = ttk.Scrollbar(self.example_win, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.example_win.mainloop()
        return

    def help_how_populate_csv(self):
        """Open a popup showing an image describing how to populate a .csv file to define an fsa"""
        #print("help_how_populate_csv")
        self.example_win = Toplevel()
        # Set the geometry of tkinter frame
        self.example_win.geometry("780x760")
        self.example_win.title("Example: how to populate a .csv description file of the FSA")
        # Create a canvas
        canvas = Canvas(self.example_win, width=755, height=755)
        # Load an image in the script
        img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_csv_file.png')
        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Adding a scrollbar on the right
        my_scrollbar = ttk.Scrollbar(self.example_win, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.example_win.mainloop()
        return

    def help_how_populate_json(self):
        """Open a popup showing an image describing how to populate a .json file to define an fsa"""
        #print("help_how_populate_json")
        self.example_win = Toplevel()
        # Set the geometry of tkinter frame
        self.example_win.geometry("980x765")
        self.example_win.title("Example: how to populate a .csv description file of the FSA")
        # Create a canvas
        canvas = Canvas(self.example_win, width=940, height=760)
        # Load an image in the script
        img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_json_file.png')
        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor=NW, image=img)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # Adding a scrollbar on the right
        my_scrollbar = ttk.Scrollbar(self.example_win, orient=VERTICAL, command=canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=my_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.example_win.mainloop()
        return

    def quit(self):
        #print("quit")
        self.tablesapp_win.destroy()
        return

class ToolBar(Frame):
    """Uses the parent instance to provide the functions"""
    def __init__(self, parent=None, parentapp=None):
        #print("ToolBar__init__")
        Frame.__init__(self, parent, width=600, height=40)
        from tkintertable import Table_images
        self.parentframe = parent
        self.parentapp = parentapp
        #add buttons
        '''
        img = Table_images.new_proj()
        self.add_button('New Project', self.parentapp.new_project, img)
        img = Table_images.open_proj()
        self.add_button('Open Project', self.parentapp.open_project, img)
        img = Table_images.open_proj()
        self.add_button('Import file', self.parentapp.import_file, img)
        img = Table_images.save_proj()
        self.add_button('Save Project', self.parentapp.save_project, img)
        img = Table_images.add_row()
        self.add_button('Add record', self.parentapp.add_Row, img)
        img = Table_images.add_col()
        self.add_button('Add col', self.parentapp.add_Column, img)
        img = Table_images.del_row()
        self.add_button('Delete record', self.parentapp.delete_Row, img)
        img = Table_images.del_col()
        self.add_button('Delete col', self.parentapp.delete_Column, img)
        img = Table_images.plot()
        self.add_button('Plot', self.parentapp.plot, img)
        img = Table_images.plotprefs()
        self.add_button('Plot Prefs', self.parentapp.plotSetup, img)
        '''

        #img = GUI_Utils.from_table_to_json()
        #self.add_button('From table to json', self.parentapp.from_Table_To_Json, img)
        img = GUI_Utils.analyze_fsa()
        self.add_button('Analyze FSA', self.parentapp.analyze_FSA, img)
        return

    def add_button(self, name, callback, img=None):
        #print("add_button")
        if img==None:
            b = Button(self, text=name, command=callback)
        else:
            b = Button(self, text=name, command=callback,
                             image=img)
        b.image = img
        b.pack(side=LEFT, padx=2, pady=2, ipadx=1, ipady=1)

        return





# Main function, run when invoked as a stand-alone Python program.

def main():
    "Run the application"
    #print("main")
    import sys, os
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="tablefile",
                        help="Open a table file", metavar="FILE")
    opts, remainder = parser.parse_args()
    if opts.tablefile is not None:
        app=TablesApp(datafile=opts.tablefile)
    else:
        app=TablesApp()


    app.mainloop()
    return

if __name__ == '__main__':
    # GUI_Utils.initialize()

    '''
    print(" ________   _____    ________    __    __    __    __   __        __        __     ")
    print("|__    __| |  ___|  |   __   |  |  \  /  |  |__|  |  \ |  |      /  \      |  |    ")
    print("   |  |    | |___   |  |__|  |  |   \/   |  |''|  |   \|  |     / /\ \     |  |    ")
    print("   |  |    |  ___|  |      _/   |  |\/|  |  |  |  |  |\   |    / /__\ \    |  |    ")
    print("   |  |    | |___   |  | \  \   |  |  |  |  |  |  |  | \  |   /  ____  \   |  |___ ")
    print("   |__|    |_____|  |__|  \__|  |__|  |__|  |__|  |__|  \_|  /_/      \_\  |______|")
    print("                                                                                   ")
    print(" __     __     __    __    __   __    _______         ____     __     __     __    ")
    print(" \ \   /  \   / /   |__|  |  \ |  |  |   ___  \     /  __  \   \ \   /  \   / /    ")
    print("  \ \ /    \ / /    |''|  |   \|  |  |  |   \  |   |  /  \  |   \ \ /    \ / /     ")
    print("   \ '  /\  ' /     |  |  |  |\   |  |  |   |  |   |  |  |  |    \ '  /\  ' /      ")
    print("    \  /  \  /      |  |  |  | \  |  |  |___/  |   \  \__/  /     \  /  \  /       ")
    print("     \/    \/       |__|  |__|  \_|  |_______ /     \ ____ /       \/    \/        ")
    '''

    print("\n\n")

    print(" .^^^^^^^   .^~~:.     .^^:        ^^^^^^^^^          .^^.      :^:                                                                                   \n\
 !@@#PGGP..P&#5G&B~   :B@@@!      .G##@@@##B.  .::.   ^@@J .    G@B    .:.          .::.    .. ..    .. ...                                           \n\
 !@@B?    :B@&PP      G@PJ@&^       .:#@&:.  :!??7!:  ^@@#P##5. B@B  ?BB5G#5:     ~PB5P#G~ 7&#PG#B? ^##PP##5.                                         \n\
 !@@BJJJ^     ?5@@B. Y@@  @@#.       .#@&.    .PY :@B ^@@5  @@7 B@B ~@@G  #&J      .PY :@B ?@@  :@@:^@@P  :@@?                                         \n\
 !@@5     ~_@BY5@&Y ?@@PJYY@@G       .#@&:   B@&  @@5 ^@@BYB@#^ B@B .G@BJ5G:     .B@&  @@5 ?@@ 5#@G ^@@# B@#^                                         \n\
 .~~^     ':^!7!:   ~~~    ^~~.       ~~~   :P#GJYGB! .~~:~!~.  ^~^   ^!7!~.      .~!!^^~^ ?@@7!!   ^@@5~!                                            \n\
                                                                                           ^??:     .??~                                              \n\
    \n\
    \n\
.JYYYYYYYJ.  ...                        .JY!                    7YJ.                  7Y?               .JY!                                          \n\
.YY5@@@55J. :!??7^  .77~77.!7~~?7^:7?!.  ... :7!^!?7:  :!??7!:  P@&.    ^7!  ~7!  ~7! ...  !7^~?7^   ~777@@5  .~??7^  ~7~  !7~  !7^                   \n\
   .&@#    ?&@  #@J ^@@#5?.#@&5B@@G5@@P :&@Y !@@GY&@B.  .PY :@B 5@&.    :#@7:&@@?.&@7 G@B .&@#YB@@^ P@&YP@@Y !&@  #@P ~@@^7@@@^~@&^                   \n\
   .&@&.   G@@:/5J  ^@@Y   #@B !@@! B@B :@@5 !@@7 P@&.:B@&  @@5 P@&.     ^@&#@7B@B@J  B@B .&@P 7@@! #@G  @@5 5@@^ 5@@: 7@B&#!@##@!                    \n\
   .GBP.    ^!7!~.  ^BB7   PB5 ~BB~ 5B5 .GB? ~BB~ YBG.:P#GJYGB! JBG.      !B#J ^B#5   5BP .GBJ !BB~ ~G#G5GB? .JGBGB5~   J#B! 7BB?                     \n\
              ''                                          .                                                      ..               \n")



    print("\n________________________________________________________________________________________________\n")
    print("                                 FSA Table app - Terminal window                                 \n")
    print("   Here will be reported the eventual syntax errors found in the FSA description files you load,\n")
    print("   or the eventual errors found in the FSA Table after you fill it and start the FSA analysis.\n")
    print("   Click the 'Help' button on the toolbar to see how to populate the files and the table.")
    print("________________________________________________________________________________________________\n")


    main()

