def get_main_style():
    return """
    QMainWindow {
        background-color: #f5f5f5;
    }
    
    QLabel#title {
        font-size: 24px;
        color: #333333;
        padding: 20px;
        font-weight: bold;
    }
    
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        min-width: 100px;
    }
    
    QPushButton:hover {
        background-color: #1976D2;
    }
    
    QPushButton:pressed {
        background-color: #0D47A1;
    }
    
    QListWidget {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 4px;
        padding: 4px;
    }
    
    QRadioButton {
        color: #424242;
        padding: 4px;
    }
    
    QProgressBar {
        border: 1px solid #E0E0E0;
        border-radius: 4px;
        text-align: center;
    }
    
    QProgressBar::chunk {
        background-color: #2196F3;
    }
    
    QMessageBox {
        background-color: white;
    }
    
    QMessageBox QPushButton {
        min-width: 80px;
    }
    """

def get_sidebar_style():
    return """
    QWidget#sidebar {
        background-color: #263238;
        min-width: 200px;
        max-width: 200px;
    }
    
    QLabel#title {
        color: white;
        background-color: #1976D2;
        padding: 20px;
        font-weight: bold;
        margin: 0;
    }
    
    QPushButton#sidebar_button {
        background-color: transparent;
        color: #B0BEC5;
        text-align: left;
        padding: 12px 20px;
        border: none;
        border-radius: 0;
        margin: 0;
    }
    
    QPushButton#sidebar_button:hover {
        background-color: #37474F;
        color: white;
    }
    
    QPushButton#sidebar_button:checked {
        background-color: #1976D2;
        color: white;
    }
    """

def get_page_style():
    return """
        QLabel { 
            color: #333333; 
            font-size: 14px;
        }
        QCheckBox { 
            color: #333333;
            font-size: 14px;
        }
        QLineEdit { 
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
            background-color: #f5f5f5;
            color: #333333;
        }
        QLineEdit:disabled {
            background-color: #e8e8e8;
        }
        QPushButton {
            padding: 5px 15px;
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QFrame {
            background-color: white;
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #e0e0e0;
        }
        QComboBox {
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
            background-color: #f5f5f5;
            color: #333333;
        }
        QComboBox::drop-down {
            border: none;
            background-color: #f5f5f5;
        }
        QComboBox::down-arrow {
            image: url(resources/down_arrow.png);
            width: 12px;
            height: 12px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: #333333;
            selection-background-color: #f5f5f5;
            selection-color: #333333;
        }
        QSpinBox {
            padding: 5px;
            border: 1px solid #cccccc;
            border-radius: 3px;
            background-color: #f5f5f5;
            color: #333333;
        }
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #f5f5f5;
            border: none;
            border-left: 1px solid #cccccc;
            width: 16px;
        }
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #e8e8e8;
        }
        QSpinBox::up-arrow {
            image: url(resources/up_arrow.png);
            width: 8px;
            height: 8px;
        }
        QSpinBox::down-arrow {
            image: url(resources/down_arrow.png);
            width: 8px;
            height: 8px;
        }
    """ 