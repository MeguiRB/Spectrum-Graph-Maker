from VisibleWavelength import rainbow_rgb
import pandas as pd  # data treatment
from matplotlib.ticker import AutoMinorLocator
from typing import List
import natsort  # sort list
from Colors import color_dictionary
import os


def import_data(dir_path, file):
    path_file = os.sep.join([dir_path, file])
    df = pd.read_csv(path_file)

    x_column_label = df.columns[0]
    y_column_label = df.columns[1]

    # Non-numeric values turn to NaN, while the rest turn into numeric values
    df[x_column_label] = pd.to_numeric(df[x_column_label], errors='coerce')
    df[y_column_label] = pd.to_numeric(df[y_column_label], errors='coerce')

    # remove lines with NaN
    df = df.dropna()

    return [df[x_column_label], df[y_column_label]]


def get_chosen_parameter(values):
    optical_property, y_label = '', ''

    if values["-Trans-"]:
        optical_property = "TT"
        y_label = "Transmittance (%)"

    elif values["-Refl-"]:
        optical_property = "R"
        y_label = "Reflectance (%)"

    elif values["-Absorp-"]:
        y_label = "Absorption (%)"

    elif values["-Absorb-"]:
        y_label = "Absorbance"
        optical_property = "Abs"

    return [optical_property, y_label]


def filter_files(values, window):
    [optical_property, y_label] = get_chosen_parameter(values)

    dir_path: str = values["-IN2-"]
    content_dir: List[str] = os.listdir(dir_path)
    content_dir = natsort.natsorted(content_dir)  # what happened: 1,10,2,3,4. Now considers 2 before 10

    name_files = []
    for fileName in content_dir:

        if fileName.find("csv") != -1 and fileName.find(optical_property) != -1:
            name_files.append(fileName.replace('.csv', ''))

        elif values["-Absorp-"] and (fileName.find("R") != -1 or fileName.find("TT") != -1):
            name_files.append(fileName.replace('.csv', ''))

    window["-list-"].Update(name_files)
    return [optical_property, y_label]


def pair_rt_files(file_name, files_selected):
    """pair reflectance and transmittance files"""

    file_name_import = file_name
    find_t = file_name.find("TT")
    find_r = file_name.find("R")

    search = ''
    if find_t >= 0:
        file_name = file_name.replace('TT', '')
        search = "R"
    elif find_r >= 0:
        file_name = file_name.replace('R', '')
        search = "TT"
    file_name = file_name.replace('.csv', '')
    file_name_check = [i for i in files_selected if file_name and search in i]

    index = -1
    for possible_file in file_name_check:
        index += 1
        possible_file = possible_file.replace('.csv', '')

        if search == "R":
            possible_file = possible_file.replace('R', '')
        if search == "TT":
            possible_file = possible_file.replace('TT', '')
        if file_name == possible_file:
            file_name_import_2 = file_name_check[index]
            files_selected.remove(file_name_import_2)
            return [file_name_import, file_name_import_2, files_selected]


def get_line_parameters(num_key, values):
    color_chosen = values["C" + num_key]
    line_style = values["S" + num_key]
    width = values["W" + num_key]

    return [color_chosen, line_style, width]


def make_plot(path_dir, TRA, y_label, values, ax):
    for wv_range, rgb in rainbow_rgb.items():
        visible_light = ax.axvspan(*wv_range, color=rgb, ec='none', alpha=0.1)

    files_selected_beta = values["-list-"]
    files_selected = [file + ".csv" for file in files_selected_beta]

    lines_plots = []
    n_lines = 0
    for file_name, legend_name in zip(files_selected, files_selected_beta):

        if not values["-Absorp-"]:
            [values_x, values_y] = import_data(path_dir, file_name)
            legend_name = legend_name.replace(" " + TRA, '')
            legend_name = write_text(legend_name)

            lines_plots.append("")

            [color_chosen, line_style, width] = get_line_parameters(str(n_lines+1), values)
            lines_plots[n_lines], = ax.plot(values_x, values_y, label=legend_name, linestyle=line_style,
                                            linewidth=width, color=color_dictionary[color_chosen])
            n_lines += 1

        elif values["-Absorp-"]:
            pair = pair_rt_files(file_name, files_selected)
            if pair:
                file_name_import, file_name_import_2, files_selected = pair[0], pair[1], pair[2]

                [values_x, values_y_1] = import_data(path_dir, file_name_import)
                [values_x, values_y_2] = import_data(path_dir, file_name_import_2)

                abs_dataframe = pd.DataFrame(100 - values_y_1 - values_y_2)
                abs_column_label = abs_dataframe.columns[0]
                values_y = abs_dataframe[abs_column_label]

                legend_name = write_text(legend_name)

                lines_plots.append("")
                [color_chosen, line_style, width] = get_line_parameters(str(n_lines+1), values)
                lines_plots[n_lines], = ax.plot(values_x, values_y, label=legend_name, linestyle=line_style,
                                                linewidth=width, color=color_dictionary[color_chosen])

                n_lines += 1

    font_size = 17

    ax.set_xlabel('Wavelength (nm)', fontsize=font_size)
    ax.set_ylabel(y_label, fontsize=font_size)
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.tick_params(labelsize=font_size, top=False, right=False, which='both')  # both major and minor ticks are affected

    return [lines_plots, visible_light]  # text labels


def write_text(string):
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
    return str_latex
