import sys
from PyQt5 import QtWidgets
from typing import List
from functools import reduce
import operator

_QH = sys.modules[__name__]
_upperFirst = lambda p: p[0].upper() + p[1:]

def _convertEnumVals(wt, vals):
    return reduce(operator.ior, map(lambda s: getattr(wt, s.strip()), vals.split("|")))

def _initWidget(w, **kargs):
    for k, v in kargs.items():
        if k[-2:] == "_s":
            getattr(w, k[:-2]).connect(
                    lambda *arg, v=v, **kargs: v(w, *arg, **kargs))
        elif k[-2:] == "_e" and hasattr(w, f"set{_upperFirst(k[:-2])}"):
            if isinstance(v, str):
                v = _convertEnumVals(type(w), v)
            getattr(w, f"set{_upperFirst(k[:-2])}")(v)
        elif hasattr(w, f"set{_upperFirst(k)}"):
            getattr(w, f"set{_upperFirst(k)}")(v)
        elif hasattr(w, k):
            getattr(w, k)(v)
        else:
            raise Exception(f"Cannot parse {k}")
    return w

def widgetHelper(widgetType):
    """
    Get the helper for a given widget type.
    """
    def wrap(parent=None, **kargs)->widgetType:
        w = widgetType(parent)
        return _initWidget(w, **kargs)
    wrap.__doc__ = f"Quick initialization function for {widgetType}"
    return wrap

def addHelpers(ws: List[str])->None:
    """
    This function add widget initialization helpers to this package by a name
    list.
    """
    for w in ws:
        setattr(_QH, w, widgetHelper(getattr(QtWidgets, f"Q{_upperFirst(w)}")))

addHelpers(["lineEdit", "pushButton", "slider", "checkBox", "spinBox",
"comboBox", "dial", "label", "messageBox", "menu", "menuBar", "action", "widget", "gridLayout"])

def gridLayoutFromList(wl, **kargs)->QtWidgets.QGridLayout:
    """
    Generate a ``QGridLayout`` by a widget list ``wl``.
    """
    w = gridLayout(**kargs)
    for row, rws in enumerate(wl, w.rowCount()):
        for col, w0 in enumerate(rws):
            if isinstance(w0, QtWidgets.QLayout):
                w.addLayout(w0, row, col)
            else:
                w.addWidget(w0, row, col)
    return w

widgetToValue = {
    QtWidgets.QLineEdit: 'text', QtWidgets.QComboBox:  'currentText',
    QtWidgets.QSlider:  'value', QtWidgets.QCheckBox:  'checkState',
    QtWidgets.QSpinBox: 'value',
    }

def toValue(w):
    if hasattr(w, "toValue"): return w.toValue()
    for wt, v in widgetToValue.items():
        if isinstance(w, wt):
            return getattr(w, v)()
    return None

def _menuAddItem(dic, parent):
    # Get type of dic: menu or action
    if dic == "----":
        return action(parent=parent, separator=True)
    if 'type' in dic:
        tp = dic.pop('type')
    elif 'children' in dic or 'title' in dic:
        tp = 'menu'
    elif 'triggered_s' in dic or 'text' in dic:
        tp = 'action'
    else:
        raise Exception(f"Can not identify the type from {dic}")

    dic['parent'] = dic.pop('parent', parent)
    if tp == 'action':
        return action(**dic)
    elif tp == "menu":
        children = dic.pop("children", [])
        w = menu(**dic)
        for child in children:
            cw = _menuAddItem(child, w)
            if isinstance(cw, QtWidgets.QMenu):
                w.addMenu(cw)
            elif isinstance(cw, QtWidgets.QAction):
                w.addAction(cw)
            else:
                raise Exception(f"Wrong type: {cw} - {type(cw)}")
        return w

def menuFromDic(dic, parent=None):
    """
    Generate and initialize `QMenu` by a dictionary
    """
    return _menuAddItem(dic, parent)

def menuBarFromList(li, **kargs) -> QtWidgets.QMenuBar:
    """
    Generate and initialize `QMenu` by a list. The elements of this list
    are the dictionaries to be used for initializing the menu.
    """
    mb = menuBar(**kargs)
    for i in li:
        m = _menuAddItem(i, mb)
        mb.addMenu(m)
    return mb
