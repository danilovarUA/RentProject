from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
#from GUI.MainWidget import MainWidget
#import sys

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
print(window.isHidden())
print(window.isVisible())
app.exec_()



# GUI and some other weird shit set up
# app = QApplication(sys.argv)
# screen = app.primaryScreen()
# print("here 0")
# window = MainWidget(screen.size().width(), screen.size().height())
# print("here 1")
# exec_code = app.exec_()
# print("here 2")
# sys.exit(exec_code)
#
