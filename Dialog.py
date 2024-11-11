import edge_tts
import asyncio
import re
import os 
import json
import argparse
import sys
def parse_args():
    parser = argparse.ArgumentParser(description='Test for edge_tts')
    parser.add_argument('--lang', type=str, help='language to use')
    parser.add_argument('--mode', type=str, help='the mode and speed')
    parser.add_argument('--name', type=str, help='whether to name the output file')
    args = parser.parse_args()
    if args.lang is None:
        args.lang = input("Please enter the language , choose from De, Es, Fr, Jp, AmE, BrE, zh:\n")
    
    if args.mode is None:
        args.mode = input("enter the mode and speed you prefer, separated by space:\n1. manual dialogues 2.load multi-dialogue\na.Normal b. Low\n")
    
    if args.name is None:
        user_input = input("Enter the name of the output file, or enter to use default name:\n")
        if user_input == "":
            args.name = "Final"
        else:
            args.name = user_input
    return args
args = parse_args()
class FileManager:
    def __init__(self):
        self.human_use = {}
        self.practical_use = {}
        self.in_use = {}
        self.more_info = {}
        self.friendly = {}

        # 判断程序是否被打包
        if getattr(sys, 'frozen', False):
            # 当脚本被打包成可执行文件时
            self.current_dir = os.path.dirname(sys.executable)
        else:
            self.current_dir = os.path.dirname(os.path.abspath(__file__))

        # 设置当前工作目录为程序所在目录
        os.chdir(self.current_dir)

        self.temp_dir = os.path.join(self.current_dir, 'Temp')
        self.final_output = os.path.join(self.current_dir, args.name + '.mp3')
        self.file_path1 = os.path.join(self.current_dir, "multi.txt")
        self.file_path2 = os.path.join(self.current_dir, "voice_list.json")
        
        self.audios = []
        self.i = 1
        self.x = 1
        self.y = 1
        os.makedirs(self.temp_dir, exist_ok=True)

    async def single_play(self, text, voice, speed):
        generate = edge_tts.Communicate(text, voice, rate=speed_control(speed))
        filepath = os.path.join(fm.temp_dir, f'output{self.x}.mp3')
        await generate.save(filepath)
        self.x += 1  # 更新计数器
        self.audios.append(filepath)  # 更新音频列表
        
    def concatenate_mp3_files(self,output_path, *input_files):
        with open(output_path, 'wb') as outfile:
            for file in input_files:
                print("\rCombining Part{}".format(fm.y),end="")
                fm.y+=1
                with open(file, 'rb') as infile:
                    outfile.write(infile.read())  # 直接写入文件的二进制数据
                os.remove(file)  # 删除临时文件
        os.removedirs(fm.temp_dir)
        print(f"\nDone!Your file here:{output_path}")
fm = FileManager()

async def get_available_list():
    print("loading available voice list...")
    if os.path.exists(fm.file_path2):
        try:
            with open(fm.file_path2, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("Loaded voice list!")
                return data
        except Exception as e:
            print(f"Failed to load voice list, error: {e}")
            return []
    elif not os.path.exists(fm.file_path2):
        to_select = await edge_tts.list_voices()  # 调用edge_tts库的list_voices函数
        filtered_list = [voice for voice in to_select if voice['Status'] != 'GA']
        with open(fm.file_path2, 'w', encoding='utf-8') as f:
            json.dump(to_select, f, ensure_ascii=False, indent=4)
    return filtered_list
to_select = asyncio.run(get_available_list())

def get_list_ready(lang,list):
    for i in range(len(list)):
        cleaned_name = re.sub(r'^Microsoft (.+?) Online \(Natural\)', r'\1',str(list[i]['FriendlyName']) )
        real_name = cleaned_name.split(" ")[0]
        reference_name = cleaned_name.replace(" ", "")
        fm.in_use [real_name] = str(list[i]['ShortName']) #Killian de-DE-KillianNeural
        fm.more_info [real_name] = reference_name #Killian Killian-German(Germany)

    lang_patterns = {
        'De': [r'German\(Germany\)', r'de-DE'],
        'Es': [r'Spanish\(Spain\)', r'es-ES'],
        'Fr': [r'French\(France\)', r'fr-FR'],
        'Jp':[r'Japanese\(Japan\)', r'ja-JP'],
        'AmE':[r'English\(UnitedStates\)', r'en-US'],
        'BrE':[r'English\(UnitedKingdom\)', r'en-GB'],
        'zh':[r'Chinese\(Mainland\)', r'zh-CN']
    }
    if lang in lang_patterns:
        for pattern in lang_patterns[lang]:
            pattern_more_info, pattern_in_use = lang_patterns[lang]
            for key, value in fm.more_info.items():
                if re.search(pattern_more_info, value):
                    fm.human_use[key] = value
            
            for key, value in fm.in_use.items():
                if re.search(pattern_in_use, value):
                    fm.practical_use[key] = value
#practical_use = {Killian de-DE-KillianNeural } human_use = {Killian Killian-German(Germany)}
get_list_ready(args.lang,to_select)

def speed_control(speed):
    if speed == 'a':
        return "-0%"
    elif speed == 'b':
        return "-30%"  # 对于低速，返回相应的参数
    else:
        raise ValueError("Invalid Input")  # 处理无效输入
def process_available_list(mode):
    for key in fm.human_use:
        fm.friendly[fm.i] = key
        fm.i += 1 
    if mode == '1':
        i = 1
        for key,value in fm.human_use.items():
            print(f"{i}. {key}")
            i += 1

async def start_generate():
    mode , speed= args.mode.split()
    process_available_list(mode)
    if mode == '1':
        texts = []
        voices = []
        while True:
            input1 = input("Enter to quit. Or choose the speaker,then enter the text, separated by space:\n")
            if input1 == "":
                break  # 退出循环
            voice = fm.practical_use[fm.friendly[int(input1.split()[0])]]
            voices.append(voice)
            text = (" ").join(input1.split()[1:])
            texts.append(text)
        for text, voice in zip(texts, voices):
            print(f"Generating {text} with {voice}...")
            await fm.single_play(text, voice, speed)
    elif mode == '2':     #input("Enter the file name")
        with open(fm.file_path1, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        os.makedirs(fm.temp_dir, exist_ok=True)
        for line in lines:
            print("\rGenerating Part{}".format(fm.x),end="")
            voice = fm.practical_use[fm.friendly[int(line.split()[0])]]
            text = ' '.join(line.split()[1:])
            await fm.single_play(text,voice,speed)
        print("\nStart Concatenating...")
    else:
        print("Invalid mode, please try again.")

    fm.concatenate_mp3_files(fm.final_output, *fm.audios)
asyncio.run(start_generate())