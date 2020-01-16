from PyQt5 import QtWidgets, QtGui
import qt_helper as qh

app = QtWidgets.QApplication([])
ms = [*map(qh.menuFromDic, [
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
])]
mb = qh.menuBar(m_addMenu=ms)
le = qh.lineEdit(text="eee")
wa = qh.widgetAction(defaultWidget=le)
ms[0].addAction(wa)
w = qh.widget(layout=qh.gridLayoutFromList([[mb], [qh.label(text="Example for menu bar")]]))
w.show()
app.exec_()
