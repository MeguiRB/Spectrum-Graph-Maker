import PySimpleGUI as sg

sg.theme("DarkTeal2")
box_size = (4, 4)

column_a = [[sg.Text('Files', font=("bold", 11))],
            [sg.Listbox(values=[], select_mode='extended', key='-list-', size=(30, 10))]
            ]

column_b1 = [[sg.Text('Axis:', font=("bold", 11))]]
column_b2 = [
    [sg.Text('x min:'), sg.Input('0', key="-xmin-", size=box_size), sg.Text('x max:'),
     sg.Input('', key="-xmax-", size=box_size)],
    [sg.Text('y min:'), sg.Input('0', key="-ymin-", size=box_size), sg.Text('y max:'),
     sg.Input('100', key="-ymax-", size=box_size)]
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