def place_legend(values):
    legend_position = values["-leg-"]

    if values["-in_out-"] == "Position 1":
        box = None
    else:
        x = values["_SPINX_"]
        y = values["_SPINY_"]
        box = (x, y)

    return [legend_position, box]


def show_legend_edit(window, line_1):
    for leg in range(1, 11):
        if leg < len(line_1) + 1:
            vis = True
        else:
            vis = False
        key_number = str(leg)
        keys_1 = ["L", "", "space_a", "W", "space_b", "S", "space_d", "C"]
        for key in keys_1:
            window[key + key_number].update(visible=vis)

    keys_2 = ["LegT", "LW", "LS", "LC", "space_c", "-ChLeg-"]
    for key in keys_2:
        window[key].update(visible=True)

def framing(values):
    if values["-frame-"] == "yes":
        legend_frame = True
    else:
        legend_frame = False
    return legend_frame
