from PyQt5 import QtWidgets, QtGui
import qt_helper as qh

app = QtWidgets.QApplication([])

mb = qh.menuBarFromList([
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
        '----',
        {
            'triggered_s': lambda w, c: exit(),
            'text': '&Exit',
            "toolTip": "exit program",
        }
    ],
},
{'title': '&Edit', 'enabled': False}
])

w = qh.widget(layout=qh.gridLayoutFromList([[mb], [qh.label(text="Example for menu bar")]]))
print(mb.findChild(object, 'open'))
w.show()
app.exec_()
