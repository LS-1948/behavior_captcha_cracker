import os


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件
    return files

if __name__ == '__main__':
    files = file_name('C:\\Users\\LS\\PycharmProjects\\Geetest\\slider_captcha\\common_train\\data\\images')
    print(type(files))
    print(len(files))

    for i in files:
        f = open('file_names.txt', 'a')
        f.write('data/images/'+str(i) + '\n')
        f.close()