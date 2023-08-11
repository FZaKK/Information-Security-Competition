import os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import string
def random_str(length=4):
    """随机字符串 默认长度为4"""
    return ''.join(random.sample(string.ascii_letters,length))

def random_color(s=1,e = 255):
    return random.randint(s,e),random.randint(s,e),random.randint(s,e)

def veri_code(length=4,width=240,height=60,size=48):
    # 创建Image图片
    image = Image.new('RGB',(width,height),(255,255,255))
    # 创建Font对象

    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建相对路径
    # 是不是把这个改成绝对路径？好像不该也可以
    font_path = os.path.join(current_dir, 'COOPBL.TTF')
    font = ImageFont.truetype(font_path,size)
    # print(font.path)
    # 创建Draw对象
    draw = ImageDraw.Draw(image)
    # 随机颜色填充每个像素
    for x in range (0,width,2):
        for y in range(height):
            draw.point((x,y),fill = random_color(64,255))
    # 验证码
    code = random_str(length)
    # 随机颜色验证码写到图片上
    for t in range (length):
        draw.text((40*t+5,5),code[t],font=font,fill=random_color(32,127))
    # 模糊滤镜
    # image= image.filter(ImageFilter.BLUR)
    return image,code


if __name__=='__main__':
    img,code = veri_code()
    with open('test.png','wb')as f:
        img.save(f)
