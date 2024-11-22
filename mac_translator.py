import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('简单翻译器')
        
        # 创建垂直布局
        layout = QVBoxLayout()

        # 输入文本框
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('请输入要翻译的文本')
        layout.addWidget(self.input_text)

        # 翻译按钮
        translate_btn = QPushButton('翻译')
        translate_btn.clicked.connect(self.translate_text)
        layout.addWidget(translate_btn)

        # 输出文本框
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText('翻译结果')
        layout.addWidget(self.output_text)

        # 设置布局
        self.setLayout(layout)

    def translate_text(self):
        # 获取输入文本
        text_to_translate = self.input_text.toPlainText()
        
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

def main():
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_())
#  They have no viable way of drastically increasing their revenue, and if investors take even a customary glance at their business fundamentals and basics of AI, there is no way they would pile billions more into them. But it looks like I have egg on my face

if __name__ == '__main__':
    main()