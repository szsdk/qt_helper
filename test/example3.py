from PyQt5 import QtWidgets
import qt_helper as qh

app = QtWidgets.QApplication([])
cmb = qh.comboBox(addItems=["on", "off"])
button = qh.pushButton(
        text="&Show Message",
        m_clicked_s=[lambda w, checked: print(23),
            lambda w, c: qh.messageBox(
                text=qh.toValue(cmb), 
                standardButtons_e="Ok | Cancel"
                ).exec_()]
        )
menus = [*map(qh.menuFromDic, [
{
    'title':'&File', 'type': 'menu', 'objectName': 'file', "toolTipsVisible": True,
    'children':[
        {
            'text': '&Open', 'objectName': 'open', "shortcut": "Ctrl+N", 
            # Attention: A extra argument `w` for the called widget itself is passed
            'triggered_s': lambda w, c: qh.messageBox(
                text=f"{w}, {c}", standardButtons_e="Ok"
                ).exec_()
        },
        # '----',
        {
            'triggered_s': lambda w, c: exit(),
            'text': '&Exit',
            "toolTip": "exit program",
        }
    ]
},
{'title': '&Edit', 'enabled': False}
])]

wl = [
        [qh.menuBar(m_addMenu=menus)],
        [ qh.label(
            text="switch",
            styleSheet="QLabel{background-color : #AAAAAA;"\
                    "color : blue; font-size: 24px;}"
                    ),
                    cmb ],
        [ qh.lineEdit(text="click the button", enabled=False), button ],
        [ None, qh.label(
            text="switch",
            styleSheet="QLabel{background-color : #AAAAAA;"\
                    "color : blue; font-size: 24px;}"
                    ),
                    ],
        ]
w = qh.widget(layout=qh.gridLayoutFromList(wl))
# button.clicked.connect(
    # lambda c: qh.messageBox(
        # text=qh.toValue(cmb), 
        # standardButtons_e="Ok | Cancel"
    # ).exec_()
# )
w.show()
app.exec_()
