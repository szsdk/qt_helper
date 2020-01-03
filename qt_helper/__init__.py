"""
This package tries to simplify the usage of ``PyQt5`` library from three different
levels:

    1. more pythonic widget initialization;
    2. providing an easier to fill up grid layout;
    3. making widgets accessing and values fetching more directly.

Let's look at the hello-world example first.

.. code-block:: 
    :emphasize-lines: 4
    :linenos:

    from PyQt5 import QtWidgets
    import qt_helper as qh
    app = QtWidgets.QApplication([])
    w = qh.label(text="hello, world")
    w.show()
    app.exec_()

A label is shown with the classical string --- "hello, world". The key line
is the highlighted  line 4. This line shows one main usage of this package
for the pythonic widget initialization. You can put widget's properties by
passing arguments to its initialization function. In this case, we want a
``QtWidgets.QLabel`` object. Then its initialization function is `label`.
In ``Qt``, we can set the text to "hello, world" by using ``setText("hello, world")``.
Now, this setting step is simplified by passing ``text="hello, world"``.
First rule of argument parsing:
    if there is a method of some class in the name of ``setXxxXxx``, it could
    be called by passing argument ``xxxXxx`` (omit "set", change the first
    letter to lowercase) in to the initialization function.


In the second example, whenever the combo box is changed, a message box is poped 
up to show the changed result.

.. code-block:: 
    :linenos:

    from PyQt5 import QtWidgets
    import qt_helper as qh
    app = QtWidgets.QApplication([])
    w = qh.comboBox(
            addItems=["on", "off"],
            currentTextChanged_s=lambda w, t:
                qh.messageBox(text=t, standardButtons_e="Ok | Cancel").exec_()
            )
    w.show()
    app.exec_()

Line 5: clearly there is method called ``setAddItems`` in ``QtWidgets.QComboBox``.
But this still works because the second parsing rule is:
    you can directly passing the name of method you want to call into the 
    initialization function followed by the value to be passed.

Line 6: suffix ``_s`` indicates for signal. Third parsing rule:
    a signal is connected by passing its name with a suffix ``_s``.
An important thing is that the first argument of the passed function would be
the widget itself. In this example, the signature of signal ``currentTextChanged``
is just ``str``. But the passed lambda function take two arguments, and the
``comboBox`` widget ``w`` is sent in the first argument.

Line 7: There a new initialization function ``messageBox`` is used. A new
argument suffix ``_e`` is used which stands for ``enum`` in c++. Because
the input for method ``setStandardButtons`` is a combination of different
``QtWidgets.QMessageBox.StandardButton`` enum elements, which is quite long to input.
The forth rule is:
    string value of argument with suffix ``_e`` is converted the corresponding 
    class enum element. ``|`` can be used for connect different element just
    like original ``Qt`` does.

.. code-block:: 

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
    ])
    w = qh.widgetFromList(wl)
    wl['b'].clicked.connect(
        lambda c: qh.messageBox(
            text=str(wl.toValue(named=True)), 
            standardButtons_e="Ok | Cancel"
        ).exec_()
    )
    w.show()
    app.exec_()

There are three rules for parsing the input argument ``k=v`` to initialize the widget.

1. If ``k`` has suffix ``_s``, for example, ``clicked_s``, then run 

.. code-block:: python
    w.k_without_suffix.connect(lambda *arg, **karg: v(w, *arg, **karg))
2. If `set{k}` is an method of widget `w`, then run `w.set{k}(v)`
3. If `k` is an attribute of widget `w`, then run `w.k(v)`.
4. Ohterwise, raise an error
"""

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
