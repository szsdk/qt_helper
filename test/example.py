from PyQt5 import QtWidgets
import qt_helper as qh

app = QtWidgets.QApplication([])
wl = qh.widgetList([
    [
        qh.label(text="switch"),
        ("c", qh.comboBox(addItems=["on", "off"]))
        ],
    [
        qh.lineEdit(text="click the button", enabled=False),
        {
            "name": "b", 
            'w': qh.pushButton(
                text="&Show Message",
                clicked_s=lambda w, checked: print(23)
            ),
            'toValue': lambda: "This is a button"
        }
    ]
],
updateObjectName=True)
w = qh.widgetFromList(wl)
wl['b'].clicked.connect(
    lambda c: qh.messageBox(
        text=str(wl.namedValue()['c']), 
        standardButtons_e="Ok | Cancel"
    ).exec_()
)
w.show()
app.exec_()
