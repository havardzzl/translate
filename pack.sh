#!/bin/bash

# 创建应用图标 (需要自行准备一个翻译图标的.icns文件)
# 可以使用 https://iconverticons.com/online/ 转换png为.icns

# 打包应用
pyinstaller --onefile \
            --windowed \
            --name="TranslatorApp" \
            --icon=translator.icns \
            mac_translator.py

# 复制到Applications目录
cp -R dist/TranslatorApp.app /Applications/