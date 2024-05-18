"""
遍历当前目录下的所有的ncm文件，并进行转换
"""
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="遍历当前目录下的所有的ncm文件，并进行转换")
parser.add_argument('--path', type=str, help='要转换的目录',
                    required=False, default='.')
parser.add_argument('--out', type=str, help='要输出的文件夹路径',
                    required=False, default='out')
parser.add_argument('--convert', type=str, help='ncmdump.exe 路径',
                    required=False, default='ncmdump.exe')


def copy_file(s, d):
    """
    复制文件从源路径到目标路径。

    :param src_file_path: 源文件路径
    :param dest_file_path: 目标文件路径
    """
    try:
        with open(s, 'rb') as src_file:  # 以二进制模式打开源文件
            with open(d, 'wb') as dest_file:  # 以二进制模式打开目标文件
                # 读取源文件内容并写入目标文件
                dest_file.write(src_file.read())
        print(f"文件复制完成，源文件：{s} -> 目标文件：{d}")
    except FileNotFoundError:
        print("源文件不存在，请检查路径是否正确。")
    except Exception as ee:
        print(f"复制文件时发生错误：{ee}")


if __name__ == '__main__':
    args = parser.parse_args()
    convert_path = args.path
    output_path = args.out
    ncm_path = args.convert
    # 1. 调用ncmdump.exe转换为mp3文件
    for root, dirs, files in os.walk(convert_path):
        for file in files:
            if file != '' and file.endswith('.ncm'):
                abs_path = os.path.join(os.path.abspath(root), file)
                dir_name = os.path.dirname(abs_path)
                base_name = os.path.basename(file)
                if not os.path.exists(os.path.join(dir_name, f'{os.path.splitext(base_name)[0]}.mp3')):
                    try:
                        result = subprocess.run([ncm_path, abs_path],
                                                stdout=subprocess.PIPE,
                                                text=True,
                                                shell=True,
                                                check=True,
                                                universal_newlines=True,
                                                encoding='utf-8')
                        print(result.stdout)
                    except subprocess.CalledProcessError as e:
                        print(e)
    # 2. 复制所有的mp3文件到out文件夹中
    output_path = os.path.abspath(os.path.join(convert_path, output_path))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for root, _, files in os.walk(convert_path):
        for file in files:
            if file != '' and file.endswith('.mp3'):
                src_path = os.path.join(os.path.abspath(root), file)
                dest_path = os.path.join(output_path, file)
                if os.path.dirname(src_path) == os.path.dirname(dest_path):
                    continue
                copy_file(src_path, dest_path)
                os.remove(src_path)
