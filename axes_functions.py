def check_num(string):
    """Checks if string is a number (positive or negative)"""
    string = string.strip()
    if string.isdigit() or (string.startswith("-") and string[1:].isdigit()):
        return True
    else:
        return False


def get_axes(values):
    """Returns the axis range (min and max x, y) from GUI"""
    keys = ['-xmin-', '-xmax-', '-ymin-', '-ymax-']
    axes = []
    for key in keys:
        if check_num(values[key]):
            axes.append(float(values[key]))
        else:
            axes.append('')
    return axes


def set_axes(values, ax):
    """Sets the plot axis range"""
    axes = get_axes(values)
    if axes[0] != '':
        ax.set_xlim(left=axes[0])

    if axes[1] != '':
        ax.set_xlim(right=axes[1])

    if axes[2] != '':
        ax.set_ylim(bottom=axes[2])

    if axes[3] != '':
        ax.set_ylim(top=axes[3])


def set_axes_from_plot(ax, window):
    """Sets the plot axis range in the GUI text boxes"""
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    axes = [x_min, x_max, y_min, y_max]
    keys = ['-xmin-', '-xmax-', '-ymin-', '-ymax-']
    for key, axis in zip(keys, axes):
        window[key].update(format(axis, ".2f"))
