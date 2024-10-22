# 2ForeignLang-Helper
二外助手，目前为止主要依赖[edge-tts](https://github.com/rany2/edge-tts)这个项目。
## 安装依赖
请先pip安装edge-tts，命令为
```cmd
pip install edge_tts
```
### Dialog.py
本脚本分为两种模式，单次单句，批量多句。

对于批量多句模式，默认读取同级目录下的multi.txt文件，一行一句，段首以数字指定说话人，如：

```txt
1 Guten Tag!
2 Hallo Welt!
3 Ich bin Anna.
4 Wie geht es dir?
```
可用说话人会在单次单句模式下自动打印。批量模式默认不打印。

运行程序后，会在当前目录下生成一个Final.mp3文件。有需要请自行修改文件名。

支持命令行模式，例如：

```cmd
python path/to/Dialog.py --lang De --mode "2 a" --name "Test_Final"
```

### Godic.py
本脚本用于查询例句，主要依赖欧陆词典网站，需要先安装bs4 requests依赖库。命令为：

```cmd
pip install bs4 requests
```

同样支持单次单个和批量模式，默认读取同级目录下的multi.txt文件，一行一词，如：

```txt
merkwürdig
Heimatstadt
Dank
```

默认根据抓取到的例句，生成与单词同名的mp3文件。同时将在打印台输出例句和中文。请到main分支获取。