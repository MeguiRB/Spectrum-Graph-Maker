import PySimpleGUI as sg
from Colors import color_dictionary

sg.theme("DarkTeal2")

# First Tab
box_size = (4, 4)

column_a = [[sg.Text('Files', font=("bold", 11))],
            [sg.Listbox(values=[], select_mode='extended', key='-list-', size=(30, 10))]
            ]

column_b1 = [[sg.Text('Axis:', font=("bold", 11))]]
column_b2 = [
    [sg.Text('x min:'), sg.Input('0', key="-xmin-", size=box_size), sg.Text('x max:'), sg.Input('', key="-xmax-", size=box_size)],
    [sg.Text('y min:'), sg.Input('0', key="-ymin-", size=box_size), sg.Text('y max:'), sg.Input('100', key="-ymax-", size=box_size)]
]
column_b3 = [[sg.Button("Set Axis")]]

column_b = [[sg.T("")],
            [sg.Button("MakeGraph")],
            [sg.T("")],
            [sg.Text("Title:", font=("bold", 11)), sg.Input(key="-title-", size=(38, 4)), sg.Button("Set Title")],
            [sg.T("")],
            [sg.Column(column_b1), sg.Column(column_b2), sg.Column(column_b3)],
            ]


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
               [sg.Column(column_a), sg.Column(column_b)],
               [sg.T("")]
               ]


# Second Tab
color_list = list(color_dictionary.keys())
style_types = ['solid', 'dashed', 'dashdot', 'dotted']

size_color_box = (9, 7)
tab2_layout = [[sg.Text('Legend Editor', font=(25))],
               [sg.pin(sg.Text('                                             Text', key="LegT", visible=False)),
                sg.pin(sg.Text("                            Linewidth", key="LW", visible=False)),
                sg.pin(sg.Text("     Linestyle", key="LS", visible=False)),
                sg.pin(sg.Text("          Linecolor", key="LC", visible=False))]]

for z in range(1, 11):
    tab2_layout.append([sg.pin(sg.Text(f"Legend {z:02}:  ", key=f"L{z}", visible=False)),
                        sg.pin(sg.Input(key=f"{z}", size=(32, 4), visible=False)),
                        sg.pin(sg.T("   ", key=f"space_a{z}", visible=False)),
                        sg.pin(sg.Input("0.9", key=f"W{z}", size=(4, 4), visible=False)),
                        sg.pin(sg.T("   ", key=f"space_b{z}", visible=False)),
                        sg.pin(sg.Combo(style_types, default_value="solid", key=f"S{z}", size=(7, 4), visible=False)),
                        sg.pin(sg.T("   ", key=f"space_d{z}", visible=False)),
                        sg.pin(sg.Combo(color_list, default_value=color_list[z - 1], key=f"C{z}", size=size_color_box,
                                        visible=False))])


i = -2
list_position = []
while i <= 2:
    list_position.append(i)
    i = round(i + 0.01, 2)

positions_choices = ['best', 'upper left', 'upper center', 'upper right', 'center left', 'center', 'center right',
                     'lower left', 'lower center', 'lower right']

column_1 = [[sg.T("Columns:"), sg.Input('1', key="-columns-", size=box_size), sg.T("    Frame:"),
             sg.Combo(['yes', 'no'], default_value="no", key="-frame-"), sg.T("    Text size:"),
             sg.Input('13', key="-Tsize-", size=box_size)],
            [sg.T("")],
            [sg.T("  Choice: "),
         sg.Combo(['Position 1', 'Position 2'], default_value="Position 1", key="-in_out-", size=(10, 1)),
         sg.T("    Position 1:"), sg.Combo(positions_choices, default_value="best", key="-leg-", size=(18, 1))],
            [sg.T("                                              Position 2:"), sg.T("↔"),
         sg.Spin(list_position, initial_value=1.00, key='_SPINX_', size=(4, 4)), sg.T("↕"),
         sg.Spin(list_position, initial_value=1.02, key='_SPINY_', size=(4, 4))]
            ]

column_2 = [[sg.T(" "), sg.Button("  Update \n Legend", key="Update", size=(9, 5))]]

tab2_layout.extend([[sg.pin(sg.T("               ", key="space_c", visible=False)),
                     sg.pin(sg.Button("Change legend", key="-ChLeg-", visible=False))],
                    [sg.HorizontalSeparator(key="Separate2")],
                    [sg.Column(column_1), sg.Column(column_2)]])
