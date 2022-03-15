# -*- coding: utf-8 -*-tab2_layout
"""
Created on Tue Sep 14 19:36:38 2021

@author: Margarida Barbosa
"""

import PySimpleGUI as sg  # create GUI
import matplotlib  # make plot
import matplotlib.pyplot as plt
import os
import ctypes  # for error message
import pickle as pkl  # to edit the plots if needed
from colors import color_dictionary
from gui_tab_1 import tab1_layout
from gui_tab_2 import tab2_layout
from plot_functions import filter_files, make_plot, write_text, get_line_parameters
from axes_functions import get_axes, set_axes, set_axes_from_plot
from legend_functions import show_legend_editor, show_legend, get_legend_parameters, update_legend_editor, able_mode_1,able_mode_2

matplotlib.use('TkAgg')  # plot window
matplotlib.rcParams['mathtext.default'] = 'regular'  # text formatter

# Building Window
layout = [[sg.TabGroup([[sg.Tab('Graph', tab1_layout, key='_tab1_'), sg.Tab('Legend', tab2_layout, key='_tab2_')]])],
          [sg.T("File Name:"), sg.Input(key="-Save-", size=(30, 4), change_submits=True), sg.Button("Save")]]

window = sg.Window('My Graph Maker', layout, resizable=True, finalize=True)

window['Position 1'].bind('<ButtonRelease-1>', 'CHANGE')
window['Position 2'].bind('<ButtonRelease-1>', 'CHANGE')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # or event=="Exit": # if user closes window
        break

    elif event == "Submit":

        path_dir_folder: str = values["-IN2-"]
        if not path_dir_folder:  # is empty
            ctypes.windll.user32.MessageBoxW(0, u"You forgot to choose the folder!", u"Error", 0)
        else:
            [TRA, y_label] = filter_files(values, window)

    elif event == "Submit_file":
        path_dir_file: str = values["-open_file2-"]
        if not path_dir_file:  # is empty
            ctypes.windll.user32.MessageBoxW(0, u"You forgot to choose the file!", u"Error", 0)
        else:
            index = path_dir_file.rfind('/')
            path_dir_folder = path_dir_file[:index]
            if plt.fignum_exists(1):
                plt.close()
            info_file = open(path_dir_file, "rb")
            [fig_handle, ax, lines_plots, legend_parameters, visible_light] = pkl.load(info_file)
            update_legend_editor(window, legend_parameters, lines_plots)
            set_axes_from_plot(ax, window)
            plt.show()

    elif event == "MakeGraph":
        if values["-list-"]:  # chose csv files
            if not plt.fignum_exists(1):
                fig_handle, ax = plt.subplots(figsize=(6.1, 4.1))  # 6.1,4.1   #3.9, 4.1
                fig_handle.patch.set_alpha(0)
            else:
                ax.cla()

            [lines_plots, visible_light] = make_plot(path_dir_folder, TRA, y_label, values, ax)
            show_legend_editor(window, lines_plots)
            legend_parameters = get_legend_parameters(values)
            show_legend(ax, legend_parameters)
            set_axes_from_plot(ax, window)
            plt.show()
        else:
            ctypes.windll.user32.MessageBoxW(0, u"You haven't chosen any files!", u"Error", 0)

    elif event == "Position 1" + "CHANGE":
        able_mode_1(window)

    elif event == "Position 2" + "CHANGE":
        able_mode_2(window)
        
    elif plt.fignum_exists(1):

        if event == "Set Axis":
            axes = get_axes(values)
            set_axes(axes, ax)
            plt.show()

        elif event == "-ChLeg-":  # Change legend

            for leg_number in range(1, len(lines_plots) + 1):
                leg_number_key = str(leg_number)

                [color_chosen, line_style, width] = get_line_parameters(leg_number_key, values)

                leg_text = values[leg_number_key]
                position = leg_number - 1
                if leg_text:
                    leg_text = write_text(leg_text)
                    lines_plots[position].set_label(leg_text)

                if width.isdigit():
                    lines_plots[position].set_linewidth(width)
                lines_plots[position].set_linestyle(line_style)
                lines_plots[position].set_color(color_dictionary[color_chosen])

            # call legend to show update
            show_legend(ax, legend_parameters)
            plt.show()

        elif event == "Update":
            legend_parameters = get_legend_parameters(values)
            show_legend(ax, legend_parameters)
            plt.show()

        elif event == "Set Title":
            title_chosen = values["-title-"]
            title_chosen = write_text(title_chosen)
            ax.set_title(title_chosen, fontsize=17)
            plt.show()

        elif event == "Save":
            if "png-pickle folder" in path_dir_folder:
                dir_name_folder = path_dir_folder
            else:
                dir_name_folder = os.sep.join([path_dir_folder, "png-pickle folder"])
                if not os.path.exists(dir_name_folder):
                    os.mkdir(dir_name_folder)

            file_name = values["-Save-"]

            # save as png
            image_file = dir_name_folder + '/' + file_name + '.png'
            fig_handle.savefig(image_file, dpi=300, bbox_inches='tight')

            # save as pickle
            pickle_file = dir_name_folder + '/' + file_name + '.pickle'
            pkl.dump((fig_handle, ax, lines_plots, legend_parameters, visible_light),
                     open(pickle_file, 'wb', pkl.HIGHEST_PROTOCOL))
