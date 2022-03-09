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
from Functions import filter_files, get_plot_values, AxesGraph, write_text
from Plot_Legend_Functions import place_legend, framing, show_legend_edit
matplotlib.use('TkAgg')  # plot window
matplotlib.rcParams['mathtext.default'] = 'regular'  # text formatter


# Building Window
layout = [[sg.TabGroup([[sg.Tab('Graph', tab1_layout, tooltip='tip'), sg.Tab('Legend', tab2_layout)]], tooltip='TIP2')],
          [sg.T("File Name:"), sg.Input(key="-Save-", size=(30, 4), change_submits=True), sg.Button("Save")]]

window = sg.Window('My Graph Maker', layout, size=(680, 450), resizable=True)  # size=(horizontal,vertical)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # or event=="Exit": # if user closes window
        break

    elif event == "Submit":

        path_dir: str = values["-IN2-"]
        if not path_dir:  # is empty
            ctypes.windll.user32.MessageBoxW(0, u"You forgot to choose the paste!", u"Error", 0)
        else:
            [path_dir, TRA, yNome, files] = filter_files(values, window)
            print(values["-IN-"])

    elif event == "MakeGraph":

        if not plt.fignum_exists(1) or not plt.fignum_exists(2):
            fig_handle, ax1 = plt.subplots(figsize=(6.1, 4.1))  # 6.1,4.1   #3.9, 4.1
            fig_handle.patch.set_alpha(0)

            fig_handle2, ax2 = plt.subplots(figsize=(6.1, 4.1))  # 6.1,4.1   #3.9, 4.1
            fig_handle2.patch.set_alpha(0)
        else:
            ax1.cla()
            ax2.cla()

        [line_1, line_2, visible_light] = get_plot_values(path_dir, TRA, yNome, files, values, ax1, ax2)
        show_legend_edit(window, line_1)
        [legend_position, box] = place_legend(values)
        number_columns = int(values['-columns-'])
        frameL = framing(values)
        size_legend_letter = values["-Tsize-"]

        leg1 = ax1.legend(loc=legend_position, bbox_to_anchor=box, ncol=number_columns,
                          prop={'size': size_legend_letter}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        leg2 = ax2.legend(loc=legend_position, bbox_to_anchor=box, ncol=number_columns,
                          prop={'size': size_legend_letter}, frameon=frameL,
                          framealpha=1, borderpad=0.5)

        frameC = leg2.get_frame()
        frameC.set_edgecolor('black')

        plt.show()


    elif event == "Set Axis":
        [xmin, xmax, ymin, ymax] = AxesGraph(values)

        if values['-xmax-']:
            ax1.set_xlim(xmin, xmax)
            ax2.set_xlim(xmin, xmax)
        ax1.set_ylim(ymin, ymax)
        ax2.set_ylim(ymin, ymax)
        plt.show()


    elif event == "-ChLeg-":  # Change legend

        for numberleg in range(1, len(line_1) + 1):

            numberleg_key = str(numberleg)
            textleg = values[numberleg_key]
            width = values["W" + numberleg_key]
            Type = values["S" + numberleg_key]
            color_chosen = values["C" + numberleg_key]

            position = numberleg - 1
            if textleg:
                textleg = write_text(textleg)
                line_1[position].set_label(textleg)
                line_2[position].set_label(textleg)

            line_1[position].set_linewidth(width)
            line_1[position].set_linestyle(Type)
            line_1[position].set_color(color_dictionary[color_chosen])
            line_2[position].set_linewidth(width)
            line_2[position].set_linestyle(Type)
            line_2[position].set_color(color_dictionary[color_chosen])

        # call legend to show update
        leg1 = ax1.legend(loc=legend_position, bbox_to_anchor=box, ncol=number_columns,
                          prop={'size': size_legend_letter}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        leg2 = ax2.legend(loc=legend_position, bbox_to_anchor=box, ncol=number_columns,
                          prop={'size': size_legend_letter}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        frameC = leg2.get_frame()
        frameC.set_edgecolor('black')
        plt.show()

        plt.show()


    elif event == "Update":

        frameL = framing(values)
        size_legend_letter = values["-Tsize-"]
        [legend_position, box] = place_legend(values)
        number_columns = int(values['-columns-'])

        leg1 = ax1.legend(loc=legend_position, bbox_to_anchor=box, ncol=number_columns,
                          prop={'size': size_legend_letter}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        leg2 = ax2.legend(loc=legend_position, bbox_to_anchor=box, ncol=number_columns,
                          prop={'size': size_legend_letter}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        frameC = leg2.get_frame()
        frameC.set_edgecolor('black')
        plt.show()


    elif event == "Set Title":

        title_chosen = values["-title-"]
        title_chosen = write_text(title_chosen)

        font_size = 17
        ax1.set_title(title_chosen, fontsize=font_size)
        ax2.set_title(title_chosen, fontsize=font_size)

        plt.show()

    elif event == "Save":

        dirName_images = os.sep.join([path_dir, "Images"])
        dirName_pickle = os.sep.join([path_dir, "Pickles"])

        if not os.path.exists(dirName_images):
            os.mkdir(dirName_images)

        if not os.path.exists(dirName_pickle):
            os.mkdir(dirName_pickle)

        parameters = [legend_position, box, number_columns, size_legend_letter, frameL]
        NomeImage = values["-Save-"]

        NomeImage_1 = dirName_images + '/' + NomeImage + '.png'
        NomeImage_2 = dirName_pickle + '/' + NomeImage + '.pickle'
        fig_handle.savefig(NomeImage_1, dpi=300, bbox_inches='tight')
        pkl.dump((fig_handle, ax1, line_1, parameters), open(NomeImage_2, 'wb', pkl.HIGHEST_PROTOCOL))

        NomeImage_a = dirName_images + '/' + 'vis_' + NomeImage + '.png'
        NomeImage_b = dirName_pickle + '/' + 'vis_' + NomeImage + '.pickle'
        fig_handle2.savefig(NomeImage_a, dpi=300, bbox_inches='tight')
        pkl.dump((fig_handle2, ax2, line_2, parameters, visible_light), open(NomeImage_b, 'wb', pkl.HIGHEST_PROTOCOL))
