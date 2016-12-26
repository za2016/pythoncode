# -*- coding=utf-8 -*-
from PIL import Image
import sys
import requests
import StringIO


ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft|()1{}[]?-_+~i!lI;:,^  "
max_width=100  #调节此项可调节图片大小，越大图片信息越好。
range_width=float(255)/(len(ASCII_CHARS)-1)

def scale_image(image, new_width=max_width):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)*0.5
    new_height = int(aspect_ratio * new_width)
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')
    
def map_pixels_to_ascii_chars(image, range_width=range_width):
    """Maps each pixel to an ascii char based on the range
    in which it lies.
    0-255 is divided into 11 ranges of 25 pixels each.
    """
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=max_width):
    image = scale_image(image)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)
    image_ascii = [pixels_to_chars[index: index + new_width] for index in xrange(0, len_pixels_to_chars, new_width)]
    f=open('image_ascii.txt','w')
    for line in image_ascii:
        f.write('%s\n'%line)
    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    image = None
    session=requests.Session()
    session.headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        if image_filepath.startswith('http://') or image_filepath.startswith('https://'):
            resp=session.get(image_filepath)
            imagebuf=StringIO.StringIO(resp.content)
            image=Image.open(imagebuf)
        else:
            image = Image.open(image_filepath)
    except Exception, e:
        print "Unable to open image file {image_filepath}.".format(image_filepath=image_filepath)
        print e
        return
    image_ascii = convert_image_to_ascii(image)
    print image_ascii

if __name__=='__main__':
    while 1:
        print u"请输入图片地址："
        try:
            image_file_path = sys.argv[1]
        except:
            image_file_path=raw_input()
        handle_image_conversion(image_file_path)
