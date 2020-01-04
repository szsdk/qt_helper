from PyQt5 import QtWidgets

_upperFirst = lambda p: p[0].upper() + p[1:]

def _convertEnumVals(wt, vals):
    def str2enum(s):
        if hasattr(wt, s):
            return eval(f"wt.{s}")
        else:
            raise Exception(f"Can not find {s} in {wt}")
    viter = map(lambda s: str2enum(s.strip()), vals.split("|"))
    ans = next(viter)
    for v in viter:
        ans |= v
    return ans

def _initWidget(w, **kargs):
    for k, v in kargs.items():
        if k[-2:] == "_s":
            eval(f"w.{k[:-2]}").connect(lambda *arg, **kargs: v(w, *arg, **kargs))
        elif k[-2:] == "_e" and hasattr(w, f"set{_upperFirst(k[:-2])}"):
            if isinstance(v, str):
                v = _convertEnumVals(type(w), v)
            eval(f"w.set{_upperFirst(k[:-2])}")(v)
        elif hasattr(w, f"set{_upperFirst(k)}"):
            eval(f"w.set{_upperFirst(k)}")(v)
        elif hasattr(w, k):
            eval(f"w.{k}")(v)
        else:
            raise Exception(f"Cannot parse {k}")
    return w

def widgetHelper(widgetType):
    def wrap(parent=None, **kargs)->widgetType:
        w = widgetType(parent)
        return _initWidget(w, **kargs)
    wrap.__doc__ = f"Quick initialization function for {widgetType}"
    return wrap

for w in ["lineEdit", "pushButton", "slider", "checkBox", "spinBox",
"comboBox", "commandLinkButton", "dateEdit", "dateTimeEdit",
"timeEdit", "dial", "fontComboBox", "label", "messageBox"]:
    exec(f"{w} = widgetHelper(QtWidgets.Q{_upperFirst(w)})")

def gridLayoutFromList(wl, parent=None):
    w = QtWidgets.QGridLayout(parent)
    for row, rws in enumerate(wl, w.rowCount()):
        for col, w0 in enumerate(rws):
            if isinstance(w0, QtWidgets.QLayout):
                w.addLayout(w0, row, col)
            else:
                w.addWidget(w0, row, col)
    return w

def widgetFromList(l, parent=None):
    "test help doc"
    w = QtWidgets.QWidget(parent=parent)
    w.setLayout(gridLayoutFromList(l, w))
    return w

def _toValue(w):
    if hasattr(w, "toValue"): return w.toValue()
    if isinstance(w, QtWidgets.QLineEdit): return w.text()
    elif isinstance(w, QtWidgets.QSlider): return w.value()
    elif isinstance(w, QtWidgets.QComboBox): return w.currentText()
    elif isinstance(w, QtWidgets.QSpinBox): return int(w.text())
    elif isinstance(w, QtWidgets.QCheckBox): return w.checkState()
    return None

def _listFunctor(f, l):
    if isinstance(l, list):
        r = []
        for w in l:
            r.append(_listFunctor(f, w))
        return r
    else:
        return f(l)

class widgetList(list):
    """
    This class is a subclass of ``list``, where user can access named widgets
    quickly by ``__getitem__`` and get some default values from named / unnamed
    widgets.
    """
    def __init__(self, l, updateObjectName=True):
        self._named = {}
        self._updateObjectName = updateObjectName
        super().__init__(_listFunctor(self._initialize, l))

    def _initialize(self, l):
        if isinstance(l, QtWidgets.QWidget):
            return l
        if isinstance(l, tuple):
            name, w = l
        elif  isinstance(l, dict):
            name, w = l['name'], l['w']
            if 'toValue' in l:
                w.toValue = l['toValue']
        else:
            raise Exception(f"can not recognize {l}")
        self._named[name] = w
        return w

    def __getitem__(self, idx):
        if isinstance(idx, str):
            return self._named[idx]
        else:
            return super().__getitem__(idx)

    def toValue(self, named=True):
        return _listFunctor(_toValue, self)

    def namedValue(self):
        return {k: _toValue(v) for k, v in self._named.items()}
