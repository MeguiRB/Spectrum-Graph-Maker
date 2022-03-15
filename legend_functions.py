from colors import color_dictionary


def able_mode_1(window):
    window["-leg-"].update(disabled=False)
    window['_SPINX_'].update(disabled=True)
    window['_SPINY_'].update(disabled=True)


def able_mode_2(window):
    window["-leg-"].update(disabled=True)
    window['_SPINX_'].update(disabled=False)
    window['_SPINY_'].update(disabled=False)


def update_legend_editor(window, legend_parameters, lines_plots):
    style_types = {'-': 'solid', '--': 'dashed', '-.': 'dashdot', ':': 'dotted'}

    for index, line in enumerate(lines_plots, start=1):
        line_style = style_types[line.get_linestyle()]
        window["S" + str(index)].update(line_style)

        window["W" + str(index)].update(line.get_linewidth())

        value_color = line.get_color()
        key_color = [key for key, value in color_dictionary.items() if value == value_color][0]
        window["C" + str(index)].update(key_color)

    show_legend_editor(window, lines_plots)
    if not legend_parameters[1]:
        window['-leg-'].update(legend_parameters[0])
        window["Position 1"].update(True)
        able_mode_1(window)
    else:
        window['_SPINX_'].update(legend_parameters[1][0])
        window['_SPINY_'].update(legend_parameters[1][1])
        window["Position 2"].update(True)
        able_mode_2(window)

    window['-columns-'].update(legend_parameters[2])
    window["-Tsize-"].update(legend_parameters[3])
    frame = {True: "yes", False: "no"}
    window["-frame-"].update(frame[legend_parameters[4]])


def show_legend_editor(window, lines_plots):
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
    if values["-frame-"] == "yes":
        legend_frame = True
    else:
        legend_frame = False
    return legend_frame


def get_legend_parameters(values):
    put_frame = framing(values)
    size_legend_letter = values["-Tsize-"]
    [legend_position, box] = place_legend(values)
    number_columns = int(values['-columns-'])

    return [legend_position, box, number_columns, size_legend_letter, put_frame]


def show_legend(ax, parameters):
    legend_variable = ax.legend(loc=parameters[0], bbox_to_anchor=parameters[1], ncol=parameters[2],
                                prop={'size': parameters[3]}, frameon=parameters[4],
                                framealpha=1, borderpad=0.5)
    frame = legend_variable.get_frame()
    frame.set_edgecolor('black')
