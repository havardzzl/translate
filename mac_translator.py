import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QDialog, QMessageBox, QMainWindow, QAction)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QMovie

class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.initUI()

    def initUI(self):
        self.setWindowTitle('设置')
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()

        # API 设置
        api_layout = QHBoxLayout()
        api_label = QLabel('API地址:')
        self.api_input = QLineEdit()
        self.api_input.setText(self.settings.value('api_url', 'https://api.example.com/translate'))
        api_layout.addWidget(api_label)
        api_layout.addWidget(self.api_input)
        
        # 源语言设置
        source_layout = QHBoxLayout()
        source_label = QLabel('源语言:')
        self.source_input = QLineEdit()
        self.source_input.setText(self.settings.value('source_lang', 'auto'))
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_input)

        # 目标语言设置
        target_layout = QHBoxLayout()
        target_label = QLabel('目标语言:')
        self.target_input = QLineEdit()
        self.target_input.setText(self.settings.value('target_lang', 'zh'))
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_input)

        # 保存按钮
        save_btn = QPushButton('保存')
        save_btn.clicked.connect(self.save_settings)

        # 添加所有控件到主布局
        layout.addLayout(api_layout)
        layout.addLayout(source_layout)
        layout.addLayout(target_layout)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)

    def save_settings(self):
        self.settings.setValue('api_url', self.api_input.text())
        self.settings.setValue('source_lang', self.source_input.text())
        self.settings.setValue('target_lang', self.target_input.text())
        self.settings.sync()
        QMessageBox.information(self, '提示', '设置已保存！')
        self.close()

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('YourCompany', 'TranslatorApp')
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('简单翻译器')
        self.setFixedSize(400, 500)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建菜单栏
        menubar = self.menuBar()
        settings_menu = menubar.addMenu('设置')
        
        # 添加设置动作
        settings_action = QAction('打开设置', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 输入文本框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('请输入要翻译的文本')
        self.input_text.keyPressEvent = self.on_key_press
        layout.addWidget(self.input_text)

        # 翻译按钮
        self.translate_btn = QPushButton('翻译')
        self.translate_btn.clicked.connect(self.translate_text)
        layout.addWidget(self.translate_btn)

        # 加载动画
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("loading.gif")
        self.loading_label.setMovie(self.movie)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

        # 输出文本框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('翻译结果')
        layout.addWidget(self.output_text)

        # 设置布局
        central_widget.setLayout(layout)

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)
        dialog.exec_()

    def on_key_press(self, event):
        QTextEdit.keyPressEvent(self.input_text, event)
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.NoModifier:
            # 只在按下回车键且没有按下其他修饰键时触发翻译
            self.translate_text()

    def translate_text(self):
        text_to_translate = self.input_text.toPlainText().strip()
        
        if not text_to_translate:
            return

        self.start_loading()
        QTimer.singleShot(100, lambda: self.perform_translation(text_to_translate))

    def start_loading(self):
        self.translate_btn.setEnabled(False)
        self.input_text.setReadOnly(True)
        self.loading_label.show()
        self.movie.start()

    def stop_loading(self):
        self.translate_btn.setEnabled(True)
        self.input_text.setReadOnly(False)
        self.movie.stop()
        self.loading_label.hide()

    def perform_translation(self, text_to_translate):
        api_url = self.settings.value('api_url', 'http://192.168.50.252:8000/translate/')
        source_lang = self.settings.value('source_lang', 'auto')
        target_lang = self.settings.value('target_lang', 'zh')

        data = {
            "text": text_to_translate
            # "source_lang": source_lang,
            # "target_lang": target_lang
        }

        try:
            response = requests.post(api_url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get('translated_text', '翻译失败')
                self.output_text.setPlainText(translated_text[0])
            else:
                self.output_text.setPlainText(f'错误：{response.status_code}')
        
        except requests.exceptions.RequestException as e:
            self.output_text.setPlainText(f'网络错误：{str(e)}')
        
        finally:
            self.stop_loading()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()