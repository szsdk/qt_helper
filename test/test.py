from PyQt5 import QtWidgets, QtCore
import qt_helper as qh

def test_widgets(qtbot):
    for t in [qh.pushButton, qh.label, qh.lineEdit]:
        la = t(text="hhh")
        la.show()
        assert la.text() == "hhh"

    wdg = qh.comboBox(addItems=["a", "b"])
    wdg.show()
    qtbot.addWidget(wdg)
    assert wdg.currentText() == "a"
    qtbot.keyClicks(wdg, 'b')
    assert wdg.currentText() == "b"
