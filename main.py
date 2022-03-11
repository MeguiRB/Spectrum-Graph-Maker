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
from Colors import color_dictionary
from GUI_Tab_1 import tab1_layout
from GUI_Tab_2 import tab2_layout
from Functions import filter_files, get_plot_values, write_text
from Axes_Functions import get_axes, set_axes, set_axes_from_plot
from Plot_Legend_Functions import show_legend_editor, show_legend, get_legend_parameters
from matplotlib.ticker import AutoMinorLocator

matplotlib.use('TkAgg')  # plot window
matplotlib.rcParams['mathtext.default'] = 'regular'  # text formatter

# Building Window
layout = [[sg.TabGroup([[sg.Tab('Graph', tab1_layout, key='_tab1_'), sg.Tab('Legend', tab2_layout, key='_tab2_')]])],
          [sg.T("File Name:"), sg.Input(key="-Save-", size=(30, 4), change_submits=True), sg.Button("Save")]]

window = sg.Window('My Graph Maker', layout, size=(680, 450), resizable=True, finalize=True)

window['Position 1'].bind('<ButtonRelease-1>', 'CHANGE')
window['Position 2'].bind('<ButtonRelease-1>', 'CHANGE')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # or event=="Exit": # if user closes window
        break

    elif event == "Submit":

        path_dir: str = values["-IN2-"]
        if not path_dir:  # is empty
            ctypes.windll.user32.MessageBoxW(0, u"You forgot to choose the folder!", u"Error", 0)
        else:
            [TRA, y_label] = filter_files(values, window)
            print(values["-IN-"])

    elif event == "MakeGraph":
        if values["-list-"]:  # chose csv files
            if not plt.fignum_exists(1):
                fig_handle, ax = plt.subplots(figsize=(6.1, 4.1))  # 6.1,4.1   #3.9, 4.1
                fig_handle.patch.set_alpha(0)
            else:
                ax.cla()

            [lines_plots, visible_light] = get_plot_values(path_dir, TRA, y_label, values, ax)
            show_legend_editor(window, lines_plots)
            legend_parameters = get_legend_parameters(values)
            show_legend(ax, legend_parameters)
            set_axes_from_plot(ax, window)
            plt.show()
        else:
            ctypes.windll.user32.MessageBoxW(0, u"You haven't chosen any files!", u"Error", 0)

    elif event == "Set Axis":
        axes = get_axes(values)
        set_axes(axes, ax)
        plt.show()

    elif event == "-ChLeg-":  # Change legend

        for leg_number in range(1, len(lines_plots) + 1):
            leg_number_key = str(leg_number)
            leg_text = values[leg_number_key]
            width = values["W" + leg_number_key]
            Type = values["S" + leg_number_key]
            color_chosen = values["C" + leg_number_key]

            position = leg_number - 1
            if leg_text:
                leg_text = write_text(leg_text)
                lines_plots[position].set_label(leg_text)

            lines_plots[position].set_linewidth(width)
            lines_plots[position].set_linestyle(Type)
            lines_plots[position].set_color(color_dictionary[color_chosen])

        # call legend to show update
        show_legend(ax, legend_parameters)
        plt.show()

    elif event == "Position 1" + "CHANGE":
        window["-leg-"].update(disabled=False)
        window['_SPINX_'].update(disabled=True)
        window['_SPINY_'].update(disabled=True)

    elif event == "Position 2" + "CHANGE":
        window["-leg-"].update(disabled=True)
        window['_SPINX_'].update(disabled=False)
        window['_SPINY_'].update(disabled=False)

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

        if plt.fignum_exists(1):
            dirName_images = os.sep.join([path_dir, "Images"])
            dirName_pickle = os.sep.join([path_dir, "Pickles"])

            if not os.path.exists(dirName_images):
                os.mkdir(dirName_images)

            if not os.path.exists(dirName_pickle):
                os.mkdir(dirName_pickle)

            NomeImage = values["-Save-"]

            NomeImage_a = dirName_images + '/' + NomeImage + '.png'
            NomeImage_b = dirName_pickle + '/' + NomeImage + '.pickle'
            fig_handle.savefig(NomeImage_a, dpi=300, bbox_inches='tight')
            pkl.dump((fig_handle, ax, lines_plots, legend_parameters, visible_light),
                     open(NomeImage_b, 'wb', pkl.HIGHEST_PROTOCOL))
