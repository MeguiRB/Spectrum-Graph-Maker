import PySimpleGUI as sg
from colors import color_dictionary
from defaults_values import default_leg_font_size, default_col_num, default_width
sg.theme("DarkTeal2")
box_size = (4, 4)

color_list = list(color_dictionary.keys())
style_types = ['solid', 'dashed', 'dashdot', 'dotted']

size_color_box = (9, 7)
tab2_layout = [[sg.Text('Legend Editor', font=("Arial", 20))],
               [sg.pin(sg.Text('                                             Text', key="LegT", visible=False)),
                sg.pin(sg.Text("                             Linewidth", key="LW", visible=False)),
                sg.pin(sg.Text("     Linestyle", key="LS", visible=False)),
                sg.pin(sg.Text("          Linecolor", key="LC", visible=False))]]

length = len(color_dictionary) + 1
for z in range(1, length):
    tab2_layout.append([sg.pin(sg.Text(f"Legend {z:02}:  ", key=f"L{z}", visible=False)),
                        sg.pin(sg.Input(key=f"{z}", size=(32, 4), visible=False)),
                        sg.pin(sg.T("   ", key=f"space_a{z}", visible=False)),
                        sg.pin(sg.Input(f"{default_width}", key=f"W{z}", size=(4, 4), visible=False)),
                        sg.pin(sg.T("   ", key=f"space_b{z}", visible=False)),
                        sg.pin(sg.Combo(style_types, default_value="solid", key=f"S{z}", size=(7, 4), visible=False)),
                        sg.pin(sg.T("   ", key=f"space_d{z}", visible=False)),
                        sg.pin(sg.Combo(color_list, default_value=color_list[z - 1], key=f"C{z}", size=size_color_box,
                                        visible=False))])

i = -3
list_position = []
while i <= 3:
    list_position.append(i)
    i = round(i + 0.01, 2)

positions_choices = ['best', 'upper left', 'upper center', 'upper right', 'center left', 'center', 'center right',
                     'lower left', 'lower center', 'lower right']

column_1 = [[sg.T("Columns:"), sg.Input(f'{default_col_num}', key="-columns-", size=box_size), sg.T("    Frame:"),
             sg.Combo(['yes', 'no'], default_value="no", key="-frame-"), sg.T("    Text size:"),
             sg.Input(f'{default_leg_font_size}', key="-Tsize-", size=box_size)],
            [sg.T("")],
            [sg.Radio("Position Mode 1", "RADIO_P", default=True, key="Position 1"),
             sg.Combo(positions_choices, default_value="best", key="-leg-", size=(18, 1))],
            [sg.Radio("Position Mode 2", "RADIO_P", key="Position 2"), sg.T("↔"),
             sg.Spin(list_position, initial_value=0.65, key='_SPINX_', size=box_size, disabled=True), sg.T("↕"),
             sg.Spin(list_position, initial_value=0.65, key='_SPINY_', size=box_size, disabled=True)]
            ]

column_2 = [[sg.T(" "), sg.Button("  Update \n Legend", key="Update", size=(9, 5))]]

tab2_layout.extend([[sg.pin(sg.T("                  ", key="space_c", visible=False)),
                     sg.pin(sg.Button("Change legend", key="-ChLeg-", visible=False))],
                    [sg.HorizontalSeparator(key="Separate2")],
                    [sg.Column(column_1), sg.Column(column_2)]])
