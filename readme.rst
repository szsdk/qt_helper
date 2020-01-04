This package tries to simplify the usage of ``PyQt5`` library from three different
levels:

    1. more pythonic widget initialization;
    2. providing an easier to fill up grid layout;
    3. making widgets accessing and values fetching more directly.


Pythonic widget initialization
##############################

Let's look at the hello-world example first.

.. code-block:: python

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

.. code-block:: python

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

Line ``addItems=["on", "off"]``: clearly there is no method called ``setAddItems`` in ``QtWidgets.QComboBox``.
But this still works because the second parsing rule is:

    you can directly passing the name of method you want to call into the 
    initialization function followed by the value to be passed.

Suffix ``_s`` in ``currentTextChanged_s`` indicates for signal. Third parsing rule:

    a signal is connected by passing its name with a suffix ``_s``.

An important thing is that the first argument of the passed function would be
the widget itself. In this example, the signature of signal ``currentTextChanged``
is just ``str``. But the passed lambda function take two arguments, and the
``comboBox`` widget ``w`` is sent in the first argument.

Here, a new initialization function ``messageBox`` is used. The
argument suffix ``_e`` in ``standardButtons_e`` stands for ``enum`` in c++. Because
the input for method ``setStandardButtons`` is a combination of different
``QtWidgets.QMessageBox.StandardButton`` enum elements, which is quite long to input.
The forth rule is:

    string value of argument with suffix ``_e`` is converted the corresponding 
    class enum element. ``|`` can be used for connect different element just
    like original ``Qt`` does.


Fill up grid layout
###################

Two functions, ``widgetFromList`` and ``gridLayoutFromList``, are provided for
filling a grid layout from a widget list. The difference between those two
is that the first one returns a widget and the second one returns a pure
``QtWidgets.QGridLayout``. The following code explains itself.

.. code-block:: python

    from PyQt5 import QtWidgets
    import qt_helper as qh
    app = QtWidgets.QApplication([])
    w = qh.widgetFromList(
            [[None, qh.label(text="0, 1")],
                [qh.pushButton(text="1, 0"), qh.commandLinkButton(text="1, 1")]])
    w.show()
    app.exec_()

Accessing widgets
#################

Pratically, there is more job need to be done with widgets instead of just
initializing them, which means we need to access them and their `values` also.
A class called ``widgetList`` is implemented for this job. You can get a name
to certain elements in this list and access them again like a dictionary.
Let's look at the example first.

.. code-block:: python

    from PyQt5 import QtWidgets
    import qt_helper as qh
    app = QtWidgets.QApplication([])
    wl = qh.widgetList([[
        qh.lineEdit(),
        ('equal', qh.pushButton(text="=")),
        {'name': 'ans', 'w': qh.lineEdit()}
    ]])
    wl['equal'].clicked.connect(lambda c:
            wl['ans'].setText(str(eval(wl[0][0].text()))))
    w = qh.widgetFromList(wl)
    w.show()
    app.exec_()

The input of ``widgetList`` is widget list while the element of this
list could also be a tuple or a dictionary. This class inherits from builtin 
list class, so can be passed into ``widgetFromList`` and
``gridLayoutFromList`` directly. 

If the element is a tuple, then the first element would the name (or key) for
the widget in the second element. A dictionary is also acceptable, the key 
for name is ``'name'`` and the key for widget is ``'w'``. Those named widgets
can be access by using their names as the keys or you can use it as a normal
list.

One important job for widgets is helping user to input some values into the 
program. However, the definition of value varies from widget to widget.
In ``QLineEdit``, usually it is ``text()`` while in ``QSlider`` it is ``value()``.
In ``QLabel``, it is nothing, we do not use it for inputing. In this library,
we predefined the value for some standard widgets which is listed in the following.

============== ==============
Widget         Value
============== ==============
QLineEdit      text
QSlider        value
QComboBox      currentText
QCheckBox      checkState
============== ==============

The values of widgets in a ``widgetList`` can be fetched with method ``namedValue``
or ``toValue`` as shown in this final example which includes almost all features
of ``qt_helper``. 

.. code-block:: python

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
            text=str(wl.namedValue()), 
            standardButtons_e="Ok | Cancel"
        ).exec_()
    )
    w.show()
    app.exec_()

Let's look at the sentence ``wl['b'].clicked.connect`` at the end of this example
first. The values of widgets in a ``widgetList`` can be fetched with two methods

1. ``namedValue``: returns a dictionary whose key or value are the 
   names or values of named widgets
2. ``toValue``: returns the value list whose elements are values of all widgets
   in the ``widgetList`` and structure are as same as the ``widgetList``'s.

In both cases, if there is no definition of value for a widget, ``None`` is returned.

How to modify the ``toValue`` behavior of a widget? Actually, the real
question should be what the ``toValue`` is. The answer is

1. Checking whether the widget has a ``toValue`` method. If it does,
   call its ``toValue()``.
2. If the answer is no, try to find a predefined tovalue method based on the
   type of widget.

``toValue`` method of the widget can be modified by adding a ``toValue`` item to 
the dictionary as a shortcut.
