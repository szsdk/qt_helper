from PyQt5 import QtWidgets
import qt_helper as qh

app = QtWidgets.QApplication([])
cmb = qh.comboBox(addItems=["on", "off"])
button = qh.pushButton(
        text="&Show Message",
        clicked_s=lambda w, checked: print(23)
        )
wl = [
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
button.clicked.connect(
    lambda c: qh.messageBox(
        text=qh.toValue(cmb), 
        standardButtons_e="Ok | Cancel"
    ).exec_()
)
w.show()
app.exec_()
