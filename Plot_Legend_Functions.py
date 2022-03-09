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
        keynumber = str(leg)
        window["L" + keynumber].update(visible=vis)
        window[keynumber].update(visible=vis)
        window["space_a" + keynumber].update(visible=vis)
        window["W" + keynumber].update(visible=vis)
        window["space_b" + keynumber].update(visible=vis)
        window["S" + keynumber].update(visible=vis)
        window["space_d" + keynumber].update(visible=vis)
        window["C" + keynumber].update(visible=vis)

    keys = ["LegT", "LW", "LS", "LC", "space_c", "-ChLeg-"]
    for key in keys:
        window[key].update(visible=True)


def make_legend(string):
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


def framing(values):
    if values["-frame-"] == "yes":
        legend_frame = True
    else:
        legend_frame = False
    return (legend_frame)
