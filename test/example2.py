from PyQt5 import QtWidgets, QtGui
import qt_helper as qh

app = QtWidgets.QApplication([])
mb = qh.menuBar()
mb = qh.initWidget(mb,
m_addMenu=map(qh.menuFromDic, [
{
    'title':'&File', 'type': 'menu', 'objectName': 'file', "toolTipsVisible": True,
    'parent': mb,
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
        },
        {'w': qh.widgetAction(defaultWidget=qh.lineEdit(text="eee"), parent=mb)}
    ],
},
{'title': '&Edit', 'enabled': False, 'parent':mb}
]))
w = qh.widget(layout=qh.gridLayoutFromList([
    [mb],
    [qh.label(text="Example for menu bar")]]))
w.show()
app.exec_()
