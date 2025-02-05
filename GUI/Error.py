import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QWidget

class CustomDialog(QDialog):
    def __init__(self,error):
        super().__init__()
        self.setWindowTitle("Ошибка")
        layout = QVBoxLayout()
        
        label = QLabel(f"Произошла ошибка:\n{error}")
        layout.addWidget(label)
        
        button = QPushButton("Ок")
        button.clicked.connect(self.accept)  # Закрывает диалог
        layout.addWidget(button)
        
        self.setLayout(layout)


if __name__ == '__main__':


    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Главное окно")

    layout = QVBoxLayout()
    button = QPushButton("Показать диалог")
    button.clicked.connect(lambda: CustomDialog('капец блин короче дима дурачок').exec())

    layout.addWidget(button)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())