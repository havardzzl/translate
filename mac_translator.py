import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QMovie

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('简单翻译器')
        self.setFixedSize(400, 500)
        
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
        self.movie = QMovie("loading.gif")  # 需要准备一个loading动画gif
        self.loading_label.setMovie(self.movie)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

        # 输出文本框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('翻译结果')
        layout.addWidget(self.output_text)

        # 设置布局
        self.setLayout(layout)

    def on_key_press(self, event):
        # 重写keyPressEvent以支持回车触发翻译
        QTextEdit.keyPressEvent(self.input_text, event)
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.translate_text()

    def translate_text(self):
        # 获取输入文本
        text_to_translate = self.input_text.toPlainText().strip()
        
        if not text_to_translate:
            return

        # 开始加载动画
        self.start_loading()

        # 使用QTimer模拟异步请求
        QTimer.singleShot(1000, lambda: self.perform_translation(text_to_translate))

    def start_loading(self):
        # 禁用按钮和输入框
        self.translate_btn.setEnabled(False)
        self.input_text.setEnabled(False)
        
        # 显示加载动画
        self.loading_label.show()
        self.movie.start()

    def stop_loading(self):
        # 恢复按钮和输入框
        self.translate_btn.setEnabled(True)
        self.input_text.setEnabled(True)
        
        # 隐藏加载动画
        self.movie.stop()
        self.loading_label.hide()

    def perform_translation(self, text_to_translate):
        # 准备请求数据
        data = {
            "text": text_to_translate
        }

        try:
            # 发送POST请求
            response = requests.post('http://192.168.50.252:8000/translate/', json=data)
            
            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                translated_text = result.get('translated_text', '翻译失败')
                self.output_text.setPlainText(translated_text[0])
            else:
                self.output_text.setPlainText(f'错误：{response.status_code}')
        
        except requests.exceptions.RequestException as e:
            self.output_text.setPlainText(f'网络错误：{str(e)}')
        
        finally:
            # 停止加载动画
            self.stop_loading()

def main():
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()