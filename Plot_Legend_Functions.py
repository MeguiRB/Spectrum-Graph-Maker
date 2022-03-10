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


def show_legend_editor(window, lines_plots):
    for leg in range(1, 11):
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