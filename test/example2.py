from PyQt5 import QtWidgets
import qt_helper as qh

app = QtWidgets.QApplication([])

mb = qh.menuBarFromList([
    {
        'title':'&File', 'type': 'menu', 'objectName': 'file',
        'children':[
            {
                'text': '&Open', 'objectName': 'open',
                'triggered_s': lambda w, c: qh.messageBox(
                    text=f"{w}, {c}", standardButtons_e="Ok"
                    ).exec_()
                },
            '----',
            {'text': '&Exit', 'triggered_s': lambda w, c: exit()},
            ],
        },
    {'title': '&Edit'}
    ])

w = qh.widgetFromList([[mb]])
print(mb.findChild(object, 'open'))
app.exec_()
