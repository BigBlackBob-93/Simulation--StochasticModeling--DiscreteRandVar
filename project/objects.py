from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox
)
from base_object import Object
from constants import number_of_events

obj: Object = Object()

window: QMainWindow = obj.set_obj(
    object=QMainWindow(),
    title="Simulation: Stochastic modeling"
)
for i in range(number_of_events):
    obj.set_obj(
        object=QLabel(window),
        title='Prob ' + str(i + 1),
        case=0,
        above=obj.indent
    )
    obj.add_obj(
        obj.set_obj(
            object=QDoubleSpinBox(window),
            left=100, above=obj.indent + 7,
            step=0.1,
            span=[0, 1]),
        key='spinbox'
    )
    obj.increase_indent()

obj.increase_indent()
obj.set_obj(
    object=QLabel(window),
    title='Trails ',
    above=obj.indent
)
obj.add_obj(
    obj.set_obj(
        object=QSpinBox(window),
        left=100, above=obj.indent + 7,
        step=100, span=[0, 10000]),
    key='spinbox'
)
obj.increase_indent(2)
obj.add_obj(
    obj.set_obj(
        object=QPushButton(window),
        title='Start',
        above=obj.indent),
    key='button'
)
obj.increase_indent()
for i in range(3):
    obj.increase_indent()
    obj.add_obj(
        obj.set_obj(
            object=QLabel(window),
            case=0,
            above=obj.indent),
        key='label'
    )

window.show()
