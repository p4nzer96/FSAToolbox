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
        # print("TablesApp__init__")
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
        # print("createMenuBar")
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
                        '02Import file on table(.txt,.fsa,.csv,.json)': {'cmd':self.import_file},
                        '03Analyze file(.txt,.fsa,.csv,.json)': {'cmd': self.just_analyze_file},
                        '04Close':{'cmd':self.close_project},
                        '05Preferences..':{'cmd':self.showPrefsDialog},
                        '06Quit':{'cmd':self.quit}}

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
        self.records_menu={'01Add Row':{'cmd':self.add_Row},
                         '02Delete Row':{'cmd':self.delete_Row},
                         '03Add Column':{'cmd':self.add_Column},
                         '04Delete Column':{'cmd':self.delete_Column},
                         '05Auto Add Rows':{'cmd':self.autoAdd_Rows},
                         '06Auto Add Columns':{'cmd':self.autoAdd_Columns},
                         '07From table to Json': {'cmd': self.from_Table_To_Json},
                         '08Analyze FSA': {'cmd': self.analyze_FSA},
                         }

        self.records_menu=self.create_pulldown(self.menu,self.records_menu)
        self.menu.add_cascade(label='Records',menu=self.records_menu['var'])

        #self.sheet_menu={'01Add Sheet':{'cmd':self.add_Sheet}, '02Remove Sheet':{'cmd':self.delete_Sheet}, '03Copy Sheet':{'cmd':self.copy_Sheet}, '04Rename Sheet':{'cmd':self.rename_Sheet} }
        self.sheet_menu = {'01Rename Sheet': {'cmd': self.rename_Sheet},}
        self.sheet_menu=self.create_pulldown(self.menu,self.sheet_menu)
        # self.menu.add_cascade(label='Sheet',menu=self.sheet_menu['var'])
        self.menu.add_cascade(label='Sheet name', menu=self.sheet_menu['var'])
        self.IO_menu={'01Import from csv file':{'cmd':self.import_csv},
                      '02Export to csv file':{'cmd':self.export_csv},
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
        # print("create_pulldown")
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
        # print("createSearchBar")
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
        # print("loadprefs")
        defaultprefs = {'textsize':14,
                         'windowwidth': 800 ,'windowheight':600}
        for prop in defaultprefs.keys():
            try:
                self.preferences.get(prop)
            except:
                self.preferences.set(prop, defaultprefs[prop])
        return

    def showPrefsDialog(self):
        # print("showPrefsDialog")
        self.prefswindow = self.currenttable.showtablePrefs()
        return

    def new_project(self, data=None):
        """Create a new table, with model and add the frame"""
        # print("new_project")
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
        # print("open_project")
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
        # print("save_project")
        if not hasattr(self, 'filename'):
            self.save_as_project()
        elif self.filename == None:
            self.save_as_project()
        else:
            self.do_save_project(self.filename)
        return

    def save_as_project(self):
        """Save as a new filename"""
        # print("save_as_project")
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
        # print("do_save_project")
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
        # print("just_analyze_file")
        if filename == None:
            filename = filedialog.askopenfilename(defaultextension='.txt',
                                                  initialdir=os.getcwd(),
                                                  filetypes=[("Text files","*.txt"),
                                                             ("fsa files", "*.fsa"),
                                                             ("csv files","*.csv"),
                                                             ("json files","*.json"),
                                                             ("All files","*.*")],
                                                  parent=self.tablesapp_win)
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

        num_chars_per_line = 50
        text_content = "FSA name: " + GUI_Utils.last_sheet + "\n"
        text_content += "______________________________________\n"

        if x0:
            # states
            text_states = ""
            text_states += "States: ["
            chars_count = len(text_states)
            for i in range(len(X) - 1):
                current_text = str(X[i].label) + ", "
                text_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_states += "\n            "
                    chars_count = 0
            text_states += str(X[len(X) - 1].label) + "]\n"
            text_content += text_states

            # initial states
            text_initial_states = ""
            text_initial_states += "Initial states: ["
            chars_count = len(text_initial_states)
            for i in range(len(x0) - 1):
                current_text = str(x0[i].label) + ", "
                text_initial_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_initial_states += "\n                    "
                    chars_count = 0
            text_initial_states += str(x0[len(x0) - 1].label) + "]\n"
            text_content += text_initial_states

            # final states
            if Xm:
                text_final_states = ""
                text_final_states += "Final states: ["
                chars_count = len(text_final_states)
                for i in range(len(Xm) - 1):
                    current_text = str(Xm[i].label) + ", "
                    text_final_states += current_text
                    chars_count += len(current_text)
                    if chars_count >= num_chars_per_line:
                        text_final_states += "\n                   "
                        chars_count = 0
                text_final_states += str(Xm[len(Xm) - 1].label) + "]\n"
                text_content += text_final_states
            else:
                text_content += "Final states: []\n"

            # forbidden states
            num_forbidden_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].isForbidden == 1:
                    num_forbidden_states += 1
            if num_forbidden_states != 0:
                counter_forbidden_states = 0
                text_forbidden_states = ""
                text_forbidden_states += "Forbidden states: ["
                chars_count = len(text_forbidden_states)
                for i in range(len(X)):
                    if X[i].isForbidden == 1:
                        if counter_forbidden_states < num_forbidden_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_forbidden_states += 1
                        text_forbidden_states += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_forbidden_states += "\n                        "
                            chars_count = 0
                text_content += text_forbidden_states + "\n"
            else:
                text_content += "Forbidden states: []\n"

            text_content += "______________________________________\n"

            # alphabet
            if E:
                text_alphabet = ""
                text_alphabet += "Alphabet: ["
                chars_count = len(text_alphabet)
                for i in range(len(E) - 1):
                    current_text = str(E[i].label) + ", "
                    text_alphabet += current_text
                    chars_count += len(current_text)
                    if chars_count >= num_chars_per_line:
                        text_alphabet += "\n                "
                        chars_count = 0
                text_alphabet += str(E[len(E) - 1].label) + "]\n"
                text_content += text_alphabet
            else:
                text_content += "Alphabet: []\n"

            # unobservable events
            num_unobservable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isObservable == 0:
                    num_unobservable_events += 1
            if num_unobservable_events != 0:
                counter_unobservable_events = 0
                text_alphabet = ""
                text_alphabet += "Unobservable events: ["
                chars_count = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isObservable == 0:
                        if counter_unobservable_events < num_unobservable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_unobservable_events += 1
                        text_alphabet += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Unobservable events: []\n"

            # uncontrollable events
            num_uncontrollable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isControllable == 0:
                    num_uncontrollable_events += 1
            if num_uncontrollable_events != 0:
                counter_uncontrollable_events = 0
                text_alphabet = ""
                text_alphabet += "Uncontrollable events: ["
                chars_count = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isControllable == 0:
                        if counter_uncontrollable_events < num_uncontrollable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_uncontrollable_events += 1
                        text_alphabet += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                                   "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Uncontrollable events: []\n"

            # fault events
            num_fault_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isFault == 1:
                    num_fault_events += 1
            if num_fault_events != 0:
                counter_fault_events = 0
                text_alphabet = ""
                text_alphabet += "Fault events: ["
                chars_count = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isFault == 1:
                        if counter_fault_events < num_fault_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_fault_events += 1
                        text_alphabet += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                            "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Fault events: []\n"

            text_content += "______________________________________\n"

            # delta transitions
            num_chars_per_line = 50
            text_content += "Delta transitions:\n"
            text_delta = ""
            if len(delta) != 0:
                for iter_X in range(len(X)):
                    current_start_filtered_deltas = f.filter_delta(start=str(X[iter_X].label), transition=None, end=None)
                    if len(current_start_filtered_deltas) == 0:
                        pass
                    else:
                        for iter_delta_row in range(len(current_start_filtered_deltas)):
                            if current_start_filtered_deltas.index[iter_delta_row] is not None:
                                current_text = "(" + str(current_start_filtered_deltas.iloc[iter_delta_row]["start"]) + ", " + str(current_start_filtered_deltas.iloc[iter_delta_row]["transition"]) + ", " + str(current_start_filtered_deltas.iloc[iter_delta_row]["end"]) + ")  "
                                text_delta += current_text
                                chars_count += len(current_text)
                                if chars_count >= num_chars_per_line:
                                    text_delta += "\n"
                                    chars_count = 0
                            else:
                                pass
                text_content += text_delta + "\n"
            else:
                text_content += " []\n"

            # Reachability
            is_reachable = analysis.get_reachability_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nREACHABLE STATES\n"
            text_content += "Reachable: ["
            chars_count = len("Reachable: [")
            text_reachability = ""
            num_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 1:
                    num_reachable_states += 1
            if num_reachable_states != 0:
                counter_reachable_states = 0
                for i in range(len(X)):
                    if X[i].is_Reachable:
                        if counter_reachable_states < num_reachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_reachable_states += 1
                        text_reachability += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_reachability += "\n                   "
                            chars_count = 0
            else:
                text_reachability += "]"
            text_content += text_reachability + "\n"

            # Unreachability
            text_content += "Not reachable: ["
            chars_count = len("Not reachable: [")
            text_unreachability = ""
            num_unreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 0:
                    num_unreachable_states += 1
            counter_unreachable_states = 0
            if num_unreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_Reachable == 0:
                        if counter_unreachable_states < num_unreachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unreachable_states += 1
                        text_unreachability += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_unreachability += "\n                           "
                            chars_count = 0
            else:
                text_unreachability += "]"
            text_content += text_unreachability + "\n"

            text_content += "FSA is reachable? "
            if is_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"

            # Co-Reachability
            is_co_reachable = analysis.get_co_reachability_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nCO-REACHABLE STATES\n"
            text_content += "Co-reachable: ["
            chars_count = len("Co-reachable: [")
            text_co_reachability = ""
            num_co_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 1:
                    num_co_reachable_states += 1
            counter_co_reachable_states = 0
            if num_co_reachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable:
                        if counter_co_reachable_states < num_co_reachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_co_reachable_states += 1
                        text_co_reachability += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_co_reachability += "\n                        "
                            chars_count = 0
            else:
                text_co_reachability += "]"
            text_content += text_co_reachability + "\n"

            # Not Co-Reachability
            text_content += "Not co-reachable: ["
            chars_count = len("Not co-reachable: [")
            text_uncoreachability = ""
            num_uncoreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 0:
                    num_uncoreachable_states += 1
            counter_uncoreachable_states = 0
            if num_uncoreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable == 0:
                        if counter_uncoreachable_states < num_uncoreachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_uncoreachable_states += 1
                        text_uncoreachability += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_uncoreachability += "\n                                "
                            chars_count = 0
            else:
                text_uncoreachability += "]"
            text_content += text_uncoreachability + "\n"

            text_content += "FSA is co-reachable? "
            if is_co_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"

            # Blocking
            is_blocking = analysis.get_blockingness_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nBLOCKING STATES\n"
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
                        if counter_blocking_states < num_blocking_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_blocking_states += 1
                        text_blocking += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_blocking += "\n               "
                            chars_count = 0
            else:
                text_blocking += "]"
            text_content += text_blocking + "\n"

            # Not blocking
            text_content += "Not blocking: ["
            chars_count = len("Not blocking: [")
            text_unblocking = ""
            num_unblocking_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Blocking == 0:
                    num_unblocking_states += 1
            counter_unblocking_states = 0
            if num_unblocking_states != 0:
                for i in range(len(X)):
                    if X[i].is_Blocking == 0:
                        if counter_unblocking_states < num_unblocking_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unblocking_states += 1
                        text_unblocking += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_unblocking += "\n                       "
                            chars_count = 0
            else:
                text_unblocking += "]"
            text_content += text_unblocking + "\n"

            text_content += "FSA is blocking? "
            if is_blocking == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"

            # Dead
            analysis.get_deadness_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nDEAD STATES\n"
            text_content += "Dead: ["
            chars_count = len("Dead: [")
            text_dead = ""
            num_dead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 1:
                    num_dead_states += 1
            counter_dead_states = 0
            if num_dead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead:
                        if counter_dead_states < num_dead_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_dead_states += 1
                        text_dead += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_dead += "\n                    "
                            chars_count = 0
            else:
                text_dead += "]"
            text_content += text_dead + "\n"

            # Not dead
            text_content += "Not dead: ["
            chars_count = len("Not dead: [")
            text_undead = ""
            num_undead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 0:
                    num_undead_states += 1
            counter_undead_states = 0
            if num_undead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead == 0:
                        if counter_undead_states < num_undead_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_undead_states += 1
                        text_undead += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_undead += "\n                  "
                            chars_count = 0
            else:
                text_undead += "]"
            text_content += text_undead + "\n"

            # Trim
            is_trim = analysis.get_trim_info(f)
            text_content += "______________________________________"
            text_content += "\nTRIM\n"
            if is_trim == 1:
                text_content += "FSA is trim? YES\n"
            else:
                text_content += "FSA is trim? NO\n"

            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "______________________________________"
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

        # Save on file button
        def save_fsa_analysis_results():
            """Save as a new filename"""
            # print("save_fsa_analysis_results")
            ta = TablesApp(Frame)
            filename = filedialog.asksaveasfilename(parent=ta.tablesapp_win,
                                                    defaultextension='.txt',
                                                    initialdir=ta.defaultsavedir,
                                                    filetypes=[("Text file","*.txt"),
                                                               ("All files","*.*")])
            if not filename:
                print('Returning')
                return

            with open(filename, 'w') as f:
                f.write(text_content)
            return

        importButton = Button(win, text='Save on file', command=save_fsa_analysis_results, background="green", foreground="white")
        importButton.grid(row=20, column=0, sticky='news', padx=2, pady=2)

        # Creating scrolled text area widget with Read only by disabling the state
        text_area = st.ScrolledText(win, width=50, height=30, font=("Times New Roman", 12))
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
            extension = os.path.splitext(filename)
            if ".txt" in extension or ".fsa" in extension:
                self.parse_txt_file_and_obtain_the_json(filename)
            elif ".json" in extension:
                self.parse_json_file_and_populate_the_table(filename)
            elif ".csv" in extension:
                self.parse_csv_file_and_populate_the_table(filename)


    def parse_txt_file_and_obtain_the_json(self, filename=None):
        """Parse the .txt file describing the fsa and convert it to a json file"""
        # print("parse_txt_file_and_obtain_the_json")
        # # print("****************************************************************************************************************************")
        # # print("**                                                                                                                        **")
        # # print("**                                                                                                                        **")
        # # print("**                                                                                                                        **")
        # # print("**                                          parse_txt_file_and_obtain_the_json                                            **")
        # # print("**                                                                                                                        **")
        # # print("**                                                                                                                        **")
        # # print("****************************************************************************************************************************")

        fd = open(filename, mode='rt')

        lines = fd.readlines()
        clean_lines = []

        for iter_list in range(len(lines)):
            clean_lines.append(lines[iter_list])

            clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")
            clean_lines[iter_list] = re.sub(" +", " ", clean_lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].split(" ")
        fd.close()

        dict_start_states = {}  # to populate column 0 with keys (states), and for every key a dictionary of info on isInitial, isFinal, isFault
        list_start_states = []  # the indexes of the list represent the row of the related the start_state value
        list_events = []  # to populate columnlabels with keys (events), and for every key a dictionary of info on isObservable, isControllable
        dict_events = {}
        dict_deltas = {}
        try:
            num_states = int(clean_lines[0][0])

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
                    dict_start_states.update({current_start_state: {"row": index_row_start_states,
                                                                    "isInitial": clean_lines[iter_lines][1],
                                                                    "isFinal": clean_lines[iter_lines][2],
                                                                    "isForbidden": clean_lines[iter_lines][3]}})
                    list_start_states.append(current_start_state)
                    index_row_start_states += 1
                    flag_the_next_line_is_a_state = 0
                    iter_lines += 1
                elif clean_lines[iter_lines][0] != '' and flag_the_next_line_is_a_state == 0:
                    flag_end_current_start_state = 0

                    while flag_end_current_start_state == 0:
                        if clean_lines[iter_lines][0] not in dict_events:
                            current_event = clean_lines[iter_lines][0]
                            dict_events.update({clean_lines[iter_lines][0]: {"column": index_column_events,
                                                                             "isControllable": clean_lines[iter_lines][2],
                                                                             "isObservable": clean_lines[iter_lines][3],
                                                                             "isFault": clean_lines[iter_lines][4]}})
                            list_events.append(clean_lines[iter_lines][0])
                            dict_deltas.update({str(index_delta_events): {"start": current_start_state,
                                                                          "name": current_event,
                                                                          "ends": clean_lines[iter_lines][1]}})
                            index_column_events += 1
                            index_delta_events += 1
                        else:
                            current_end_state = clean_lines[iter_lines][1]
                            current_event_end_states = current_end_state
                            current_event = clean_lines[iter_lines][0]
                            for key in range(index_delta_events):
                                if (str(key) in dict_deltas) and dict_deltas[str(key)]["name"] == \
                                        clean_lines[iter_lines][0] and dict_deltas[str(key)]["start"] == current_start_state:
                                    current_event_end_states = current_event_end_states + "-" + dict_deltas[str(key)]["ends"]
                                    del dict_deltas[str(key)]

                            dict_deltas.update({str(index_delta_events): {"start": current_start_state,
                                                                          "name": current_event,
                                                                          "ends": current_event_end_states}})
                            index_delta_events += 1

                        if (iter_lines + 1) < len(clean_lines) and clean_lines[iter_lines + 1][0] != '':
                            iter_lines += 1  # reiteration of while flag_end_current_start_state == 0:
                            flag_the_next_line_is_a_state = 0
                        else:
                            iter_lines += 1  # reiteration of while iter_lines < len(clean_lines):
                            flag_end_current_start_state = 1  # exit from the while loop
                            flag_the_next_line_is_a_state = 0

        except:
            # Create an instance of Tkinter frame
            win = Tk()
            # Set the geometry of Tkinter frame
            win.geometry("440x200")
            win.title("Error loading the file")
            Label(win, text="There are some syntax error in the .txt or .fsa file you tried to import.\r\n"
                            "             Click here if you want to see an example on how to\r\n"
                            "                                  correctly populate the file.",
                  font=('Helvetica 10 bold')).pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()
            win.mainloop()

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
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

        return





    def parse_json_file_and_populate_the_table(self, filename=None):
        """Parse the .json file describing the fsa and populate the current table with its data"""
        # print("parse_json_file_and_populate_the_table")
        ## print("****************************************************************************************************************************")
        ## print("**                                                                                                                        **")
        ## print("**                                                                                                                        **")
        ## print("**                                                                                                                        **")
        ## print("**                                          parse_json_file_and_populate_the_table                                        **")
        ## print("**                                                                                                                        **")
        ## print("**                                                                                                                        **")
        ## print("****************************************************************************************************************************")

        with open(filename) as json_file:
            data = json.load(json_file)

        dict_events = data["E"].copy()
        iter = 0
        for key in dict_events:
            dict_events[key].update({"column": iter})
            iter += 1

        dict_start_states = data["X"].copy()
        iter = 0
        for key in dict_start_states:
            dict_start_states[key].update({"row": iter})
            iter += 1

        list_start_states = []
        list_start_states = list(dict_start_states.keys())
        list_events = list(dict_events.keys())
        dict_deltas = {}

        iter = 0
        for key in data["delta"]:
            dict_deltas.update({str(iter): data["delta"][key]})
            iter += 1

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
        json_file.close()
        return

    def parse_csv_file_and_populate_the_table(self, filename=None):
        """Parse the .csv file describing the fsa and populate the current table"""
        # print("parse_csv_file_and_populate_the_table")
        # # print("****************************************************************************************************************************")
        # # print("**                                                                                                                        **")
        # # print("**                                                                                                                        **")
        # # print("**                                                                                                                        **")
        # # print("**                                          parse_csv_file_and_populate_the_table                                         **")
        # # print("**                                                                                                                        **")
        # # print("**                                                                                                                        **")
        # # print("****************************************************************************************************************************")

        with open(filename, encoding='utf-8') as csvf:
            fd = open(filename, mode='rt')
            lines = fd.readlines()
        clean_lines = []

        for iter_list in range(len(lines)):
            clean_lines.append(lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
            clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")
            clean_lines[iter_list] = re.sub(" +", " ", clean_lines[iter_list])
            clean_lines[iter_list] = clean_lines[iter_list].split(",")

        fd.close()

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        GUI_Utils.dictcolControllableEvents.clear()
        GUI_Utils.dictcolObservableEvents.clear()
        GUI_Utils.dictcolFaultyEvents.clear()
        self.currenttable.model.addColumn("State")

        dict_event_properties = {}
        dict_event_suffixes = {}
        dict_col_label_widths = {}
        dict_col_label_widths.update({"0": len("State")})
        try:
            for i in range(1, len(clean_lines[0])):
                current_event = clean_lines[0][i]
                if clean_lines[0][i] and clean_lines[0][i] != '_':
                    if current_event.endswith("_uc_f_uo") or current_event.endswith("_uc_uo_f") or current_event.endswith(
                            "_f_uc_uo") or current_event.endswith("_f_uo_uc") or current_event.endswith(
                            "_uo_f_uc") or current_event.endswith("_uo_uc_f"):
                        substring_to_remove = current_event[-8:]
                        current_event = current_event.replace(str(substring_to_remove), "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 1}})
                    elif current_event.endswith("_uc_f"):
                        current_event = current_event.replace("_uc_f", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
                    elif current_event.endswith("_f_uc"):
                        current_event = current_event.replace("_f_uc", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
                    elif current_event.endswith("_uc_uo"):
                        current_event = current_event.replace("_uc_uo", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
                    elif current_event.endswith("_uo_uc"):
                        current_event = current_event.replace("_uo_uc", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
                    elif current_event.endswith("_uo_f"):
                        current_event = current_event.replace("_uo_f", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
                    elif current_event.endswith("_f_uo"):
                        current_event = current_event.replace("_f_uo", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
                    elif current_event.endswith("_uc"):
                        current_event = current_event.replace("_uc", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 0}})
                    elif current_event.endswith("_f"):
                        current_event = current_event.replace("_f", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 1}})
                    elif current_event.endswith("_uo"):
                        current_event = current_event.replace("_uo", "")
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 0}})
                    else:
                        current_event.replace(" ", "")
                        dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 0}})
                clean_lines[0][i] = current_event

                suffix_event = ""
                if "isObservable" in dict_event_properties[current_event]:
                    if dict_event_properties[current_event]["isObservable"] == 1:
                        GUI_Utils.setEventAsObservable(self.currenttable, current_event)
                    elif dict_event_properties[current_event]["isObservable"] == 0:
                        suffix_event += "_uo"
                        GUI_Utils.setEventAsUnobservable(self.currenttable, current_event)
                else:
                    GUI_Utils.setEventAsUnobservable(self.currenttable, current_event)

                if "isControllable" in dict_event_properties[current_event]:
                    if dict_event_properties[current_event]["isControllable"] == 1:
                        GUI_Utils.setEventAsControllable(self.currenttable, current_event)
                    elif dict_event_properties[current_event]["isControllable"] == 0:
                        suffix_event += "_uc"
                        GUI_Utils.setEventAsUncontrollable(self.currenttable, current_event)
                else:
                    GUI_Utils.setEventAsUncontrollable(self.currenttable, current_event)

                if "isFault" in dict_event_properties[current_event]:
                    if dict_event_properties[current_event]["isFault"] == 1:
                        suffix_event += "_f"
                        GUI_Utils.setEventAsFaulty(self.currenttable, current_event)
                    elif dict_event_properties[current_event]["isFault"] == 0:
                        GUI_Utils.setEventAsUnfaulty(self.currenttable, current_event)
                else:
                    GUI_Utils.setEventAsUnfaulty(self.currenttable, current_event)

                dict_event_suffixes.update({current_event: suffix_event})
                self.currenttable.model.addColumn(current_event + suffix_event)
                num_chars = len(current_event + suffix_event)
                dict_col_label_widths.update({str(i): num_chars})

            # adding or deleting rows
            while self.currenttable.model.getRowCount() < len(clean_lines)-1:
                self.currenttable.model.addRow()

            while self.currenttable.model.getRowCount() > len(clean_lines)-1:
                self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)

            # populating the table
            for row in range(1, len(clean_lines)):
                for col in range(0, len(clean_lines[0])):
                    self.currenttable.model.setValueAt(clean_lines[row][col], row-1, col)
                    num_chars = len(clean_lines[row][col])
                    if num_chars > dict_col_label_widths[str(col)]:
                        dict_col_label_widths.update({str(col): num_chars})
                    if dict_col_label_widths[str(col)] >= 10:
                        width_col = 120 + (dict_col_label_widths[str(col)]-10) * 10
                        self.currenttable.resizeColumn(col, width_col)

        except:
            # Create an instance of Tkinter frame
            win = Tk()
            # Set the geometry of Tkinter frame
            win.title("Error loading the file")
            win.geometry("400x200")
            Label(win, text="There are some syntax error in the .csv file you tried to import.\r\n"
                            "         Click here if you want to see an example on how to\r\n"
                            "                           correctly populate the file.",
                  font=('Helvetica 10 bold')).pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=self.open_popup_errors_on_csv_file).pack()
            win.mainloop()

        self.currenttable.redrawVisible()
        return

    def open_popup_errors_on_txt_file(self, win=None):
        """Open popup if some errors are present on the .txt file describing the fsa"""
        # print("open_popup_errors_on_txt_file")
        # Create an instance of tkinter frame
        self.example_win = Toplevel(win)
        # Set the geometry of tkinter frame
        self.example_win.geometry("1030x670")
        self.example_win.title("Example: how to populate a .txt description file of the FSA")
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
        # print("open_popup_errors_on_csv_file")
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

    def close_project(self):
        # print("close_project")
        if hasattr(self,'currenttable'):
            self.currenttable.destroy()
        return

    def import_csv(self):
        # print("import_csv")
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
        # print("export_csv")
        from tkintertable.Tables_IO import TableExporter
        exporter = TableExporter()
        exporter.ExportTableData(self.currenttable)
        return

    def add_Sheet(self, sheetname=None, sheetdata=None):
        """Add a new sheet - handles all the table creation stuff"""
        # print("add_Sheet")
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
        # print("delete_Sheet")
        s = self.notebook.index(self.notebook.select())
        name = self.notebook.tab(s, 'text')
        #self.notebook.delete(s)
        self.notebook.forget(s)
        del self.sheets[name]
        return

    def copy_Sheet(self, newname=None):
        """Copy a sheet"""
        # print("copy_Sheet")
        newdata = self.currenttable.getModel().getData().copy()
        if newname==None:
            return
            # self.add_Sheet(None, newdata)
        else:
            self.add_Sheet(newname, newdata)
        return

    def rename_Sheet(self):
        """Rename a sheet"""
        # print("rename_Sheet")
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
        # print("setcurrenttable")
        try:
            #s = self.notebook.getcurselection()
            s = self.notebook.index(self.notebook.select())
            self.currenttable = self.sheets[s]
        except:
            pass
        return

    def add_Row(self):
        """Add a new row"""
        # print("add_Row")
        self.currenttable.addRow()
        self.saved = 0
        return

    def delete_Row(self):
        """Delete currently selected row"""
        # print("delete_Row")
        self.currenttable.deleteRow()
        self.saved = 0
        return

    def add_Column(self):
        """Add a new column"""
        # print("add_Column")
        self.currenttable.addColumn()
        self.saved = 0
        return

    def delete_Column(self):
        """Delete currently selected column in table"""
        # print("delete_Column")
        self.currenttable.deleteColumn()
        self.saved = 0
        return

    def from_Table_To_Json(self):
        """Convert the current table content into an FSA Json file description"""
        # print("from_Table_To_Json")
        GUI_Utils.fromTableToJson(self.currenttable)
        self.saved = 0
        return

    def analyze_FSA(self):
        """Convert the current table content into a Json file"""
        # print("analyze_FSA")
        GUI_Utils.analyzeFsa(self.currenttable)
        self.saved = 0
        return

    def autoAdd_Rows(self):
        """Auto add x rows"""
        # print("autoAdd_Rows")
        self.currenttable.autoAddRows()
        self.saved = 0
        return

    def autoAdd_Columns(self):
        """Auto add x rows"""
        # print("autoAdd_Columns")
        self.currenttable.autoAddColumns()
        self.saved = 0
        return

    def findValue(self):
        # print("findValue")
        self.currenttable.findValue()
        return

    def do_find_text(self, event=None):
        """Find the text in the table"""
        # print("do_find_text")
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
        # print("do_find_again")
        if not hasattr(self,'currenttable'):
            return
        searchstring=self.findtext.get()
        if self.currenttable is not None:
            self.currenttable.findValue(searchstring, findagain=1)
        return

    def plot(self, event=None):
        # print("plot")
        self.currenttable.plotSelected()
        return

    def plotSetup(self, event=None):
        # print("plotSetup")
        self.currenttable.plotSetup()
        return

    def about_Tables(self):
        # print("about_Tables")
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
        # print("online_documentation")
        import webbrowser
        link='http://sourceforge.net/projects/tkintertable/'
        webbrowser.open(link,autoraise=bool(1))
        return

    def help_how_populate_txt_or_fsa(self):
        """Open a popup showing an image describing how to populate a .txt or .fsa file to define an fsa"""
        # print("help_how_populate_txt_or_fsa")
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
        # print("help_how_populate_csv")
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
        # print("help_how_populate_json")
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
        # print("quit")
        self.tablesapp_win.destroy()
        return

class ToolBar(Frame):
    """Uses the parent instance to provide the functions"""
    def __init__(self, parent=None, parentapp=None):
        # print("ToolBar__init__")
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

        img = GUI_Utils.from_table_to_json()
        self.add_button('From table to json', self.parentapp.from_Table_To_Json, img)
        img = GUI_Utils.analyze_fsa()
        self.add_button('Analyze FSA', self.parentapp.analyze_FSA, img)
        return

    def add_button(self, name, callback, img=None):
        # print("add_button")
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
    # print("main")
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
    main()

