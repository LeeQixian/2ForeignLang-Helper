# 2ForeignLang-Helper
二外助手，目前为止主要依赖edgetts这个项目。
为了解决德语音频稀缺搞了一个基于人项目的批量语音合成。
使用须知：
1. 请确保您已经安装了edgetts库，如果没有请先安装。
2. 请确保您已经安装了ffmpeg，并将FFmpeg加入PATH变量，如果没有请先安装。
分为两种模式，单次单句，批量多句。批量多句，需要准备一个multi.txt文件，每行一个句子，段首以数字指定说话人，如：
'''txt
1. Guten Tag!
2. Hallo!
3. Wie geht es dir?
4. Auf Wiedersehen!
'''
运行程序后，会在当前目录下生成一个output.mp3文件。有需要请自行修改文件名。