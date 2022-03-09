# -*- coding: utf-8 -*-tab2_layout
"""
Created on Tue Sep 14 19:36:38 2021

@author: Margarida Barbosa
"""

import PySimpleGUI as sg  # criar a GUI
import pandas as pd  # Tratar os dados
import matplotlib  # fazer os gráficos

matplotlib.use('TkAgg')  # janela dos gráficos
matplotlib.rcParams['mathtext.default'] = 'regular'  # formatar o texto
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import os
import ctypes  # usado para as mensagens de erro
from typing import List
import pickle as pkl  # para poder guardar e editar posteriormente os gráficos
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import natsort  # sort list

# import numpy as np


# from cycler import cycler
# matplotlib.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
from Colors import color_dictionary


def Importar(pathDir, file):
    pathFile = os.sep.join([pathDir, file])
    df = pd.read_csv(pathFile)

    Col1 = df.columns[0]  # nome da coluna 1
    Col2 = df.columns[1]  # nome da coluna 2

    # strings que nao interessam ficam NaN, tornando o resto em formato numerico
    df[Col1] = pd.to_numeric(df[Col1], errors='coerce')

    # importante formato numerico para o grafico
    df[Col2] = pd.to_numeric(df[Col2], errors='coerce')

    # retira linhas com NaN
    df = df.dropna()

    # x= df[Col1].to_numpy()
    # y= df[Col2].to_numpy()
    return ([df[Col1], df[Col2]])


def ChoosingValues():
    path_dir: str = values["-IN2-"]

    content_dir: List[str] = os.listdir(path_dir)
    content_dir = natsort.natsorted(content_dir)  # considers 2 before 10

    if values["-Trans-"]:
        if values["-Total-"]:
            TRA = "TT"
        elif values["-Spec-"]:
            TRA = "TE"
        yNome = "Transmittance (%)"

    elif values["-Refl-"]:
        if values["-Total-"]:
            TRA = "R"
        elif values["-Dif-"]:
            TRA = "RD"
        yNome = "Reflectance (%)"

    elif values["-Absorp-"]:
        yNome = "Absorption (%)"
        TRA = "-----"

    elif values["-Absorb-"]:
        yNome = "Absorbance"
        TRA = "Abs"

    # window['_EXIT_'].Update(visible = True)

    number = 0
    files = []
    for fileName in content_dir:
        if fileName.find("csv") != -1:
            if fileName.find(TRA) != -1:
                number += 1
                files.append(fileName.replace('.csv', ''))

            elif values["-Absorp-"]:
                if fileName.find("R") != -1 or fileName.find("TT") != -1:
                    number += 1
                    files.append(fileName.replace('.csv', ''))

    window["-list-"].Update(files)
    return ([path_dir, TRA, yNome, files])


def ValuesForGraph(path_dir, TRA, yNome, files):
    # sg.Radio('Transmittance', "RADIO1", default=False, key="-Trans-"),
    # sg.Radio('Reflectance', "RADIO1", default=False,key="-Refl-"),
    # sg.Radio('Absorption', "RADIO1", default=False,key="-Absorp"),
    # sg.Radio('Absorbance', "RADIO1", default=False,key="-Absorb")],
    # sg.Radio('Total', "RADIO2", default=False, key="-Total-"),
    # sg.Radio('Specular', "RADIO2", default=False,key="-Spec-"),
    # sg.Radio('Difuse', "RADIO2", default=False,key="-Dif-")],

    rainbow_rgb = {(400, 440): '#8b00ff', (440, 460): '#4b0082',
                   (460, 500): '#0000ff', (500, 570): '#00ff00',
                   (570, 590): '#ffff00', (590, 620): '#ff7f00',
                   (620, 750): '#ff0000'}
    for wv_range, rgb in rainbow_rgb.items():
        visible_light = ax2.axvspan(*wv_range, color=rgb, ec='none', alpha=0.1)

    filesselected_beta = values["-list-"]
    filesselected = []
    for file in filesselected_beta:
        file_csv = file + ".csv"
        filesselected.append(file_csv)

    # print(filesselected)
    line_1 = []
    line_2 = []
    nlines = 0
    for fileName in filesselected:

        if fileName.find(".csv") != -1:

            if values["-Absorp-"] == False:

                [Val1, Val2] = Importar(path_dir, fileName)

                Valores = pd.DataFrame(Val2)
                Coluna = Valores.columns[0]

                legendName = fileName.replace('.csv', '')
                legendName = legendName.replace(" " + TRA, '')
                legendName = legendName.replace(" ", '/')
                legendName = writeL(legendName)

                line_1.append("")
                line_2.append("")
                color_chosen = values["C" + str(nlines + 1)]
                line_1[nlines], = ax1.plot(Val1, Valores[Coluna], label=legendName, linewidth=0.9,
                                           color=color_dictionary[color_chosen])
                line_2[nlines], = ax2.plot(Val1, Valores[Coluna], label=legendName, linewidth=0.9,
                                           color=color_dictionary[color_chosen])
                nlines += 1

            elif values["-Absorp-"]:

                fileName_import = fileName

                findT = fileName.find("TT")
                findR = fileName.find("R")

                if findT >= 0:
                    fileName = fileName.replace('TT', '')
                    search = "R"
                elif findR >= 0:
                    fileName = fileName.replace('R', '')
                    search = "TT"
                fileName = fileName.replace('.csv', '')

                fileName_check = [i for i in filesselected if fileName and search in i]

                print(fileName_check)

                index = -1
                for f in fileName_check:
                    index += 1
                    f = f.replace('.csv', '')

                    if findT >= 0:
                        f = f.replace('R', '')

                    elif findR >= 0:
                        f = f.replace('TT', '')

                    if fileName == f:
                        break

                if fileName == f:
                    fileName_import2 = fileName_check[index]
                    print(fileName_import)
                    print(fileName_import2)

                    [Vala, Valb] = Importar(path_dir, fileName_import)
                    [Val1, Val2] = Importar(path_dir, fileName_import2)

                    filesselected.remove(fileName_import2)

                    Valores = pd.DataFrame(100 - Valb - Val2)
                    Coluna = Valores.columns[0]

                    legendName = fileName
                    # legendName=legendName.replace(" ",'/')
                    legendName = writeL(legendName)

                    # last_char_index = legendName.rfind("/")        
                    # legendName =  legendName[:last_char_index]
                    line_1.append("")
                    line_2.append("")
                    color_chosen = values["C" + str(nlines + 1)]
                    line_1[nlines], = ax1.plot(Val1, Valores[Coluna], label=legendName, linewidth=0.9,
                                               color=color_dictionary[color_chosen])
                    line_2[nlines], = ax2.plot(Val1, Valores[Coluna], label=legendName, linewidth=0.9,
                                               color=color_dictionary[color_chosen])
                    nlines += 1

        print(f"Maximo de {legendName}: {Valores[Coluna].max()}")

    fsize = 17
    ax1.set_xlabel('Wavelength (nm)', fontsize=fsize)
    ax1.set_ylabel(yNome, fontsize=fsize)
    ###
    ax1.tick_params(axis="x", labelsize=fsize)
    ax1.tick_params(axis="y", labelsize=fsize)
    ax1.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax1.yaxis.set_minor_locator(AutoMinorLocator(2))

    ######################3
    # line1 = 400 # vertical x = 3
    # line2 = 750 # vertical x = 5
    # ax2.axvspan(line1, line2, alpha=.1, color='grey')

    ax2.set_xlabel('Wavelength (nm)', fontsize=fsize)
    ax2.set_ylabel(yNome, fontsize=fsize)

    ##
    ax2.tick_params(axis="x", labelsize=fsize)
    ax2.tick_params(axis="y", labelsize=fsize)
    ax2.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax2.yaxis.set_minor_locator(AutoMinorLocator(2))

    [xmin, xmax, ymin, ymax] = AxesGraph()
    if values['-ymax-']:
        ax1.set_ylim(ymin, ymax)
        ax2.set_ylim(ymin, ymax)

    return ([line_1, line_2, visible_light])  # text labels


def legendGraph():
    legend_position = values["-leg-"]

    if values["-in_out-"] == "Position 1":
        box = None
    else:
        x = values["_SPINX_"]
        y = values["_SPINY_"]
        box = (x, y)

    return ([legend_position, box])


def AxesGraph():
    xmin = float(values['-xmin-'])
    ymin = float(values['-ymin-'])
    if not not values['-xmax-']:
        xmax = float(values['-xmax-'])
    else:
        xmax = values['-xmax-']
    ymax = float(values['-ymax-'])
    return ([xmin, xmax, ymin, ymax])


def writeL(string):
    if 'n_line' in string:
        text = string.split(" n_line ")
        text1 = text[0]
        str_latex = r'$' + text1 + ' $'

        for i in range(1, len(text)):
            textx = text[i]
            str_latex += "\n" + r'$' + textx + ' $'

    else:
        str_latex = '$' + string + '$'

    str_latex = str_latex.replace(" ", "\:")
    return (str_latex)


def framing():
    if values["-frame-"] == "yes":
        frameL = True
    else:
        frameL = False
    return (frameL)


def MakeLegVisible():
    for nleg in range(1, 11):

        if nleg < len(line_1) + 1:
            vis = True
        else:
            vis = False
        keynumber = str(nleg)
        window["L" + keynumber].update(visible=vis)
        window[keynumber].update(visible=vis)
        window["space_a" + keynumber].update(visible=vis)
        window["W" + keynumber].update(visible=vis)
        window["space_b" + keynumber].update(visible=vis)
        window["S" + keynumber].update(visible=vis)
        window["space_d" + keynumber].update(visible=vis)
        window["C" + keynumber].update(visible=vis)

    window["LegT"].update(visible=True)
    window["LW"].update(visible=True)
    window["LS"].update(visible=True)
    window["LC"].update(visible=True)
    window["space_c"].update(visible=True)
    window["-ChLeg-"].update(visible=True)




#######################################################################################################################

cola = [[sg.Text('Files', font=("bold", 11))],
        [sg.Listbox(values=[], select_mode='extended', key='-list-', size=(30, 10))]
        ]

sz = (4, 4)

colb_1 = [[sg.Text('Axis:', font=("bold", 11))]]
colb_2 = [
    [sg.Text('x min:'), sg.Input('0', key="-xmin-", size=sz), sg.Text('x max:'), sg.Input('', key="-xmax-", size=sz)],
    [sg.Text('y min:'), sg.Input('0', key="-ymin-", size=sz), sg.Text('y max:'), sg.Input('100', key="-ymax-", size=sz)]
    ]
colb_3 = [[sg.Button("Set Axis")]]

colb = [[sg.T("")],
        [sg.Button("MakeGraph")],
        [sg.T("")],
        [sg.Text("Title:", font=("bold", 11)), sg.Input(key="-title-", size=(38, 4)), sg.Button("Set Title")],
        [sg.T("")],
        [sg.Column(colb_1), sg.Column(colb_2), sg.Column(colb_3)],
        ]
################


i = -2
list_position = []
while i <= 2:
    list_position.append(i)
    i = round(i + 0.01, 2)

positions_choices = ['best', 'upper left', 'upper center', 'upper right', 'center left', 'center', 'center right',
                     'lower left', 'lower center', 'lower right']

col1 = [[sg.T("Columns:"), sg.Input('1', key="-columns-", size=sz), sg.T("    Frame:"),
         sg.Combo(['yes', 'no'], default_value="no", key="-frame-"), sg.T("    Text size:"),
         sg.Input('13', key="-Tsize-", size=sz)],
        [sg.T("")],
        [sg.T("  Choice: "),
         sg.Combo(['Position 1', 'Position 2'], default_value="Position 1", key="-in_out-", size=(10, 1)),
         sg.T("    Position 1:"), sg.Combo(positions_choices, default_value="best", key="-leg-", size=(18, 1))],
        [sg.T("                                              Position 2:"), sg.T("↔"),
         sg.Spin(list_position, initial_value=1.00, key='_SPINX_', size=(4, 4)), sg.T("↕"),
         sg.Spin(list_position, initial_value=1.02, key='_SPINY_', size=(4, 4))]
        ]

col2 = [[sg.T(" "), sg.Button("  Update \n Legend", key="Update", size=(9, 5))]]

sg.theme("DarkTeal2")
tab1_layout = [[sg.Text('Graph Maker', font=(25))],
               [sg.Text("Choose a folder: "), sg.Input(key="-IN2-", size=(65, 4), change_submits=True),
                sg.FolderBrowse(key="-IN-")],
               [sg.HorizontalSeparator(key="Separate0")],
               [sg.Text("Chose one: "), sg.Radio('Transmittance', "RADIO1", default=True, key="-Trans-"),
                sg.Radio('Reflectance', "RADIO1", default=False, key="-Refl-"),
                sg.Radio('Absorption', "RADIO1", default=False, key="-Absorp-"),
                sg.Radio('Absorbance', "RADIO1", default=False, key="-Absorb-")],
               [sg.Text("Chose one: "), sg.Radio('Total', "RADIO2", default=True, key="-Total-"),
                sg.Radio('Specular', "RADIO2", default=False, key="-Spec-"),
                sg.Radio('Difuse', "RADIO2", default=False, key="-Dif-"),
                sg.T("                                                                "), sg.Button("Submit")],
               [sg.HorizontalSeparator(key="Separate")],
               [sg.Column(cola), sg.Column(colb)],
               [sg.T("")]
               ]

color_list = []
color_list_code = []
for key in color_dictionary:
    color_list.append(key)

style_types = ['solid', 'dashed', 'dashdot', 'dotted']

scolor = (9, 7)
tab2_layout = [[sg.Text('Legend Editor', font=(25))],
               [sg.pin(sg.Text('                                             Text', key="LegT", visible=False)),
                sg.pin(sg.Text("                            Linewidth", key="LW", visible=False)),
                sg.pin(sg.Text("     Linestyle", key="LS", visible=False)),
                sg.pin(sg.Text("          Linecolor", key="LC", visible=False))],
               [sg.pin(sg.Text("Legend 1:  ", key="L1", visible=False)),
                sg.pin(sg.Input(key="1", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a1", visible=False)),
                sg.pin(sg.Input("0.9", key="W1", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b1", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S1", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d1", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[0], key="C1", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 2:  ", key="L2", visible=False)),
                sg.pin(sg.Input(key="2", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a2", visible=False)),
                sg.pin(sg.Input("0.9", key="W2", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b2", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S2", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d2", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[1], key="C2", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 3:  ", key="L3", visible=False)),
                sg.pin(sg.Input(key="3", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a3", visible=False)),
                sg.pin(sg.Input("0.9", key="W3", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b3", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S3", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d3", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[2], key="C3", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 4:  ", key="L4", visible=False)),
                sg.pin(sg.Input(key="4", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a4", visible=False)),
                sg.pin(sg.Input("0.9", key="W4", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b4", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S4", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d4", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[3], key="C4", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 5:  ", key="L5", visible=False)),
                sg.pin(sg.Input(key="5", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a5", visible=False)),
                sg.pin(sg.Input("0.9", key="W5", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b5", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S5", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d5", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[4], key="C5", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 6:  ", key="L6", visible=False)),
                sg.pin(sg.Input(key="6", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a6", visible=False)),
                sg.pin(sg.Input("0.9", key="W6", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b6", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S6", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d6", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[5], key="C6", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 7:  ", key="L7", visible=False)),
                sg.pin(sg.Input(key="7", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a7", visible=False)),
                sg.pin(sg.Input("0.9", key="W7", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b7", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S7", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d7", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[6], key="C7", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 8:  ", key="L8", visible=False)),
                sg.pin(sg.Input(key="8", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a8", visible=False)),
                sg.pin(sg.Input("0.9", key="W8", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b8", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S8", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d8", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[7], key="C8", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 9:  ", key="L9", visible=False)),
                sg.pin(sg.Input(key="9", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a9", visible=False)),
                sg.pin(sg.Input("0.9", key="W9", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b9", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S9", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d9", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[8], key="C9", size=scolor, visible=False))],
               [sg.pin(sg.Text("Legend 10:", key="L10", visible=False)),
                sg.pin(sg.Input(key="10", size=(32, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_a10", visible=False)),
                sg.pin(sg.Input("0.9", key="W10", size=(4, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_b10", visible=False)),
                sg.pin(sg.Combo(style_types, default_value="solid", key="S10", size=(7, 4), visible=False)),
                sg.pin(sg.T("   ", key="space_d10", visible=False)),
                sg.pin(sg.Combo(color_list, default_value=color_list[9], key="C10", size=scolor, visible=False))],
               [sg.pin(sg.T("               ", key="space_c", visible=False)),
                sg.pin(sg.Button("Change legend", key="-ChLeg-", visible=False))],
               [sg.HorizontalSeparator(key="Separate2")],
               [sg.Column(col1), sg.Column(col2)]
               ]
###Building Window
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
            [path_dir, TRA, yNome, files] = ChoosingValues()
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

        [line_1, line_2, visible_light] = ValuesForGraph(path_dir, TRA, yNome, files)
        MakeLegVisible()
        [legend_position, box] = legendGraph()
        ncolumn = int(values['-columns-'])
        frameL = framing()
        sizeL = values["-Tsize-"]

        leg1 = ax1.legend(loc=legend_position, bbox_to_anchor=box, ncol=ncolumn, prop={'size': sizeL}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        leg2 = ax2.legend(loc=legend_position, bbox_to_anchor=box, ncol=ncolumn, prop={'size': sizeL}, frameon=frameL,
                          framealpha=1, borderpad=0.5)

        frameC = leg2.get_frame()
        frameC.set_edgecolor('black')

        plt.show()

        # fig_agg = draw_figure(window['canvas'].TKCanvas,  fig_handle)
    elif event == "Set Axis":
        [xmin, xmax, ymin, ymax] = AxesGraph()

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
                textleg = writeL(textleg)
                line_1[position].set_label(textleg)
                line_2[position].set_label(textleg)

            line_1[position].set_linewidth(width)
            line_1[position].set_linestyle(Type)
            line_1[position].set_color(color_dictionary[color_chosen])
            line_2[position].set_linewidth(width)
            line_2[position].set_linestyle(Type)
            line_2[position].set_color(color_dictionary[color_chosen])

        # call legend to show update
        leg1 = ax1.legend(loc=legend_position, bbox_to_anchor=box, ncol=ncolumn, prop={'size': sizeL}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        leg2 = ax2.legend(loc=legend_position, bbox_to_anchor=box, ncol=ncolumn, prop={'size': sizeL}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        frameC = leg2.get_frame()
        frameC.set_edgecolor('black')
        plt.show()

        plt.show()


    elif event == "Update":

        frameL = framing()
        sizeL = values["-Tsize-"]
        [legend_position, box] = legendGraph()
        ncolumn = int(values['-columns-'])

        leg1 = ax1.legend(loc=legend_position, bbox_to_anchor=box, ncol=ncolumn, prop={'size': sizeL}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        leg2 = ax2.legend(loc=legend_position, bbox_to_anchor=box, ncol=ncolumn, prop={'size': sizeL}, frameon=frameL,
                          framealpha=1, borderpad=0.5)
        frameC = leg2.get_frame()
        frameC.set_edgecolor('black')
        plt.show()






    elif event == "Set Title":
        title_chosen = values["-title-"]
        title_chosen = writeL(title_chosen)

        fsize = 17
        ax1.set_title(title_chosen, fontsize=fsize)
        ax2.set_title(title_chosen, fontsize=fsize)

        plt.show()

    elif event == "Save":

        dirName_images = os.sep.join([path_dir, "Images"])
        dirName_pickle = os.sep.join([path_dir, "Pickles"])

        if not os.path.exists(dirName_images):
            os.mkdir(dirName_images)

        if not os.path.exists(dirName_pickle):
            os.mkdir(dirName_pickle)

        parameters = [legend_position, box, ncolumn, sizeL, frameL]
        NomeImage = values["-Save-"]

        NomeImage_1 = dirName_images + '/' + NomeImage + '.png'
        NomeImage_2 = dirName_pickle + '/' + NomeImage + '.pickle'
        fig_handle.savefig(NomeImage_1, dpi=300, bbox_inches='tight')
        pkl.dump((fig_handle, ax1, line_1, parameters), open(NomeImage_2, 'wb', pkl.HIGHEST_PROTOCOL))

        NomeImage_a = dirName_images + '/' + 'vis_' + NomeImage + '.png'
        NomeImage_b = dirName_pickle + '/' + 'vis_' + NomeImage + '.pickle'
        fig_handle2.savefig(NomeImage_a, dpi=300, bbox_inches='tight')
        pkl.dump((fig_handle2, ax2, line_2, parameters, visible_light), open(NomeImage_b, 'wb', pkl.HIGHEST_PROTOCOL))
