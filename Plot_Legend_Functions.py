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


def show_legend_edit(window, lines_plots):
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
