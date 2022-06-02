#!/usr/bin/env python
"""
    Custom Table sub-class illustrate table functionality.
    Created January 2008
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from __future__ import absolute_import, division, print_function
try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import filedialog, messagebox, simpledialog
    from tkinter import font
except:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog
    import tkSimpleDialog as simpledialog
    import tkMessageBox as messagebox
    import TkFont as font

from .Tables import TableCanvas, ColumnHeader

# added by me **********************************************************************************************************

import json

import my_globals

# **********************************************************************************************************************


class MyTable(TableCanvas):
    """Sub-class of Tablecanvas, with some changes in behaviour to make
    a customised table - just an example"""
    def __init__(self, parent=None, model=None):
        TableCanvas.__init__(self, parent, model)
        self.bgcolor = '#FFFAF1'
        self.fgcolor = 'black'
        self.entrybackgr = 'white'

        self.selectedcolor = 'yellow'
        self.rowselectedcolor = '#B0E0E6'
        self.multipleselectioncolor = '#ECD672'

        return


    '''
    # added by me ******************************************************************************************************
    @classmethod
    def setEventAsUnobservable(self, column_name=None):
        """Set the event as Unobservable - can be used in a table header"""
        print("setEventAsUnobservable")

        if column_name == None:
            n = messagebox.askyesno("Setting",
                                    "Unobservable Event?",
                                    parent=self.parentframe)
            if n:
                # global dictcolObservableEvents

                current_col_index = self.getSelectedColumn()
                current_col_name = self.model.getColumnLabel(current_col_index)
                my_globals.dictcolObservableEvents[str(current_col_name)] = 0
                # print(current_col_index)
                # print(str(self.model.getColumnLabel(current_col_index)))
                print("Observable events:", my_globals.dictcolObservableEvents)
        else:
            my_globals.dictcolObservableEvents[str(column_name)] = 0

    # ******************************************************************************************************************

    # added by me ******************************************************************************************************
    @classmethod
    def setEventAsObservable(self, column_name=None):
        """Set the event as Observable - can be used in a table header"""
        print("setEventAsObservable")

        if column_name == None:

            n = messagebox.askyesno("Setting",
                                    "Observable Event?",
                                    parent=self.parentframe)
            if n:
                # global dictcolObservableEvents
                current_col_index = self.getSelectedColumn()
                current_col_name = self.model.getColumnLabel(current_col_index)
                my_globals.dictcolObservableEvents[str(current_col_name)] = 1
                # print(current_col_index)
                # print(str(self.model.getColumnLabel(current_col_index)))
                print("Observable events:", my_globals.dictcolObservableEvents)
        else:
            my_globals.dictcolObservableEvents[str(column_name)] = 1
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Observable events:", my_globals.dictcolObservableEvents)

    # ******************************************************************************************************************

    # added by me ******************************************************************************************************
    @classmethod
    def setEventAsUncontrollable(self, column_name=None):
        """Set the event as Uncontrollable - can be used in a table header"""
        print("setEventAsUncontrollable")

        if column_name == None:

            n = messagebox.askyesno("Setting",
                                    "Uncontrollable Event?",
                                    parent=self.parentframe)
            if n:
                # global dictcolControllableEvents
                current_col_index = self.getSelectedColumn()
                current_col_name = self.model.getColumnLabel(current_col_index)
                my_globals.dictcolControllableEvents[str(current_col_name)] = 0
                # print(current_col_index)
                # print(str(self.model.getColumnLabel(current_col_index)))
                print("Controllable events:", my_globals.dictcolControllableEvents)
        else:
            my_globals.dictcolControllableEvents[str(column_name)] = 0

    # ******************************************************************************************************************

    # added by me ******************************************************************************************************
    @classmethod
    def setEventAsControllable(self, column_name=None):
        """Set the event as Controllable - can be used in a table header"""
        print("setEventAsControllable")

        if column_name == None:

            n = messagebox.askyesno("Setting",
                                    "Controllable Event?",
                                    parent=self.parentframe)
            if n:
                # global dictcolControllableEvents
                current_col_index = self.getSelectedColumn()
                current_col_name = self.model.getColumnLabel(current_col_index)
                my_globals.dictcolControllableEvents[str(current_col_name)] = 1
                # print(current_col_index)
                # print(str(self.model.getColumnLabel(current_col_index)))
                print("Controllable events:", my_globals.dictcolControllableEvents)
        else:
            my_globals.dictcolControllableEvents[str(column_name)] = 1

    # ******************************************************************************************************************

    # added by me ******************************************************************************************************
    @classmethod
    def setEventAsFaulty(self, column_name=None):
        """Set the event as Faulty - can be used in a table header"""
        print("setEventAsFaulty")

        if column_name == None:
            n = messagebox.askyesno("Setting",
                                    "Faulty Event?",
                                    parent=self.parentframe)
            if n:
                # global dictcolFaultyEvents

                current_col_index = self.getSelectedColumn()
                current_col_name = self.model.getColumnLabel(current_col_index)
                my_globals.dictcolFaultyEvents[str(current_col_name)] = 1
                # print(current_col_index)
                # print(str(self.model.getColumnLabel(current_col_index)))
                print("Faulty events:", my_globals.dictcolFaultyEvents)
        else:
            my_globals.dictcolFaultyEvents[str(column_name)] = 1

    # ******************************************************************************************************************

    # added by me ******************************************************************************************************
    @classmethod
    def setEventAsUnfaulty(self, column_name=None):
        """Set the event as Unfaulty - can be used in a table header"""
        print("setEventAsUnfaulty")

        if column_name == None:

            n = messagebox.askyesno("Setting",
                                    "Observable Event?",
                                    parent=self.parentframe)
            if n:
                # global dictcolFaultyEvents
                current_col_index = self.getSelectedColumn()
                current_col_name = self.model.getColumnLabel(current_col_index)
                my_globals.dictcolFaultyEvents[str(current_col_name)] = 0
                # print(current_col_index)
                # print(str(self.model.getColumnLabel(current_col_index)))
                print("Faulty events:", my_globals.dictcolFaultyEvents)
        else:
            my_globals.dictcolFaultyEvents[str(column_name)] = 0
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Faulty events:", my_globals.dictcolFaultyEvents)

    # ******************************************************************************************************************

    # added by me *******************************************************************************************************
    @classmethod
    def fromTableToJson(self):
        """Convert the current table content into a Json file"""
        print("fromTableToJson")
        # Algorithm of conversion of the current table to a json file
        n = messagebox.askyesno("Convert",
                                "Convert table to json file?",
                                parent=self.parentframe)
        if n:
            print("columnlabels:", self.model.columnlabels.values())
            # rows start from 0, columns start from 0

            json_dict = {"X": {}, "E": {}, "delta": {}}
            dict_X = {}
            dict_E = {}
            dict_delta = {}
            current_state = ""
            iter_ascii_delta = 65  # decimal value of the ASCII character 'A'
            num_rows = self.model.getRowCount()
            num_cols = len(self.model.columnlabels)
            for iter_row in range(num_rows):
                for iter_col in range(num_cols):
                    print("iter_row,iter_col:" + str(iter_row) + "," + str(iter_col))
                    if self.model.getCellRecord(iter_row, iter_col) != None:
                        current_cell = self.model.getCellRecord(iter_row, iter_col)
                        print("current_cell: ", current_cell)
                        if iter_col == 0:
                            if current_cell[0] and current_cell[0] != '_':
                                if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                        "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                                    "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith(
                                    "_p_i_f"):
                                    string_lenght = len(current_cell)
                                    substring_to_remove = current_cell[-6:]
                                    current_state = current_cell.replace(str(substring_to_remove), "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "1", "isFinal": "1", "isProhibited": "1"}})
                                elif current_cell.endswith("_i_f"):
                                    current_state = current_cell.replace("_i_f", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "1", "isFinal": "1", "isProhibited": "0"}})
                                elif current_cell.endswith("_f_i"):
                                    current_state = current_cell.replace("_f_i", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "1", "isFinal": "1", "isProhibited": "0"}})
                                elif current_cell.endswith("_i_p"):
                                    current_state = current_cell.replace("_i_p", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "1", "isFinal": "0", "isProhibited": "1"}})
                                elif current_cell.endswith("_p_i"):
                                    current_state = current_cell.replace("_p_i", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "1", "isFinal": "0", "isProhibited": "1"}})
                                elif current_cell.endswith("_p_f"):
                                    current_state = current_cell.replace("_p_f", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "0", "isFinal": "1", "isProhibited": "1"}})
                                elif current_cell.endswith("_f_p"):
                                    current_state = current_cell.replace("_f_p", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "0", "isFinal": "1", "isProhibited": "1"}})
                                elif current_cell.endswith("_i"):
                                    current_state = current_cell.replace("_i", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "1", "isFinal": "0", "isProhibited": "0"}})
                                elif current_cell.endswith("_f"):
                                    current_state = current_cell.replace("_f", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "0", "isFinal": "1", "isProhibited": "0"}})
                                elif current_cell.endswith("_p"):
                                    current_state = current_cell.replace("_p", "")
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "0", "isFinal": "0", "isProhibited": "1"}})
                                else:
                                    current_state = current_cell
                                    current_state.replace(" ", "")
                                    dict_X.update(
                                        {str(current_state): {"isInit": "0", "isFinal": "0", "isProhibited": "0"}})
                            else:
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
                                dict_delta.update({str(chr(iter_ascii_delta)): {"start": str(current_state),
                                                                                "name": str(self.model.getColumnLabel(
                                                                                    iter_col)),
                                                                                "ends": str(current_delta_ends[i])}})
                                print("dict_delta", dict_delta)
                                current_key_event = str(self.model.getColumnLabel(iter_col))
                                dict_E.update({current_key_event: {
                                    "isObs": str(my_globals.dictcolObservableEvents[current_key_event]),
                                    "isContr": str(my_globals.dictcolControllableEvents[current_key_event]),
                                    "isFaulty": str(my_globals.dictcolFaultyEvents[current_key_event])}})
                                iter_ascii_delta += 1

                            print(current_delta_ends)
                    else:
                        pass

            json_dict["X"] = dict_X
            json_dict["delta"] = dict_delta
            json_dict["E"] = dict_E
            print(json_dict)

            with open("sample.json", "w") as outfile:
                # json_object = json.dumps(json_dict, outfile, indent=4 )
                json.dump(json_dict, outfile, indent=4)

            # print("cella 1,1", self.model.getCellRecord(1,1))

            outfile.close()
            print("Tabella convertita in un json file")

        return


    # *****************************************************************************************************************
    '''