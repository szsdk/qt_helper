from PyQt5 import QtWidgets
import qt_helper as qh

app = QtWidgets.QApplication([])

mb = qh.menuBarFromList([
    {
        'title':'&File', 'type': 'menu', 'objectName': 'file',
        'children':[
            {
                'text': '&Open', 'objectName': 'open',
                # Attention: A extra argument `w` for the called widget itself is passed
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

w = qh.widgetFromList([[mb], [qh.label(text="Example for menu bar")]])
print(mb.findChild(object, 'open'))
w.show()
app.exec_()
