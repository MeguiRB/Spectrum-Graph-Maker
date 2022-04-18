from colors import color_dictionary
from defaults_values import default_col_num, default_leg_font_size, default_frame_color


def able_mode_1(window):
    """Able the components that allow to position the legend using descreptive strings
    Disabled the components that allow to position the legend the  using coordinates"""
    window["-leg-"].update(disabled=False)
    window['_SPINX_'].update(disabled=True)
    window['_SPINY_'].update(disabled=True)


def able_mode_2(window):
    """Disabled the components that allow to position the legend the  using coordinates
    Able the components that allow to position the legend using descreptive strings"""
    window["-leg-"].update(disabled=True)
    window['_SPINX_'].update(disabled=False)
    window['_SPINY_'].update(disabled=False)


def update_legend_editor(window, legend_parameters, lines_plots):
    """Update the legend parameters in the GUI according to the current plot"""
    style_types = {'-': 'solid', '--': 'dashed', '-.': 'dashdot', ':': 'dotted'}

    for index, line in enumerate(lines_plots, start=1):
        line_style = style_types[line.get_linestyle()]
        window["S" + str(index)].update(line_style)

        window["W" + str(index)].update(line.get_linewidth())

        value_color = line.get_color()
        key_color = [key for key, value in color_dictionary.items() if value == value_color][0]
        window["C" + str(index)].update(key_color)

    show_legend_editor(window, lines_plots)
    if legend_parameters["box"] is None:
        window['-leg-'].update(legend_parameters["legend_position"])
        window["Position 1"].update(True)
        able_mode_1(window)
    else:
        # example: legend_parameters["box"] = (1,1)
        window['_SPINX_'].update(legend_parameters["box"][0])
        window['_SPINY_'].update(legend_parameters["box"][1])
        window["Position 2"].update(True)
        able_mode_2(window)

    window['-columns-'].update(legend_parameters["number_columns"])
    window["-Tsize-"].update(legend_parameters["size_legend_letter"])
    frame = {True: "yes", False: "no"}
    window["-frame-"].update(frame[legend_parameters["put_frame"]])


def show_legend_editor(window, lines_plots):
    """Shows in tab2 only part of the legend editor according to number of plot lines"""
    length = len(color_dictionary) + 1
    for leg in range(1, length):
        if leg < len(lines_plots) + 1:
            vis = True
        else:
            vis = False
        key_number = str(leg)
        keys_a = ["L", "", "space_a", "W", "space_b", "S", "space_d", "C"]
        for key in keys_a:
            window[key + key_number].update(visible=vis)

    keys_b = ["LegT", "LW", "LS", "LC", "space_c", "-ChLeg-"]
    for key in keys_b:
        window[key].update(visible=True)


def place_legend(values):
    """Get the position to place the legend of the plot"""
    if values["Position 1"]:
        legend_position = values["-leg-"]
        box = None
    else:
        legend_position = "lower left"
        x = values["_SPINX_"]
        y = values["_SPINY_"]
        box = (x, y)

    return [legend_position, box]


def framing(values):
    """Returns True if we want to frame the legend, if not returns False """
    if values["-frame-"] == "yes":
        legend_frame = True
    else:
        legend_frame = False
    return legend_frame


def check_col_num(string):
    """Checks if string is a digit"""
    if string.isdigit():
        num_col = int(string)
        if num_col == 0:
            num_col = default_col_num
        return num_col
    else:
        return default_col_num


def check_size_num(string):
    """Checks if string is a float"""
    try:
        return float(string)
    except ValueError:
        return default_leg_font_size


def get_legend_parameters(values):
    """Get the legend parameters such as legend_position, box, number_columns, size_legend_letter, put_frame from GUI"""
    put_frame = framing(values)
    size_legend_letter = check_size_num(values["-Tsize-"])
    [legend_position, box] = place_legend(values)
    number_columns = check_col_num(values['-columns-'])
    return {"legend_position": legend_position, "box": box, "number_columns": number_columns,
            "size_legend_letter": size_legend_letter, "put_frame": put_frame}


def show_legend(ax, parameters):
    """Places a customized legend (according to the parameters) on the graph"""
    legend_variable = ax.legend(loc=parameters["legend_position"], bbox_to_anchor=parameters["box"],
                                ncol=parameters["number_columns"],prop={'size': parameters["size_legend_letter"]},
                                frameon=parameters["put_frame"], framealpha=1, borderpad=0.5)
    frame = legend_variable.get_frame()
    frame.set_edgecolor(default_frame_color)
