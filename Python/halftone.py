import Image, ImageDraw, ImageStat
from os import listdir
from os.path import isfile, join
import pandas as pd

def halftone(im, cmyk, sample, scale):
    '''Returns list of half-tone images for cmyk image. sample (pixels), 
       determines the sample box size from the original image. The maximum 
       output dot diameter is given by sample * scale (which is also the number 
       of possible dot sizes). So sample=1 will presevere the original image 
       resolution, but scale must be >1 to allow variation in dot size.'''
    cmyk = cmyk.split()
    dots = []
    angle = 0
    for channel in cmyk:
        channel = channel.rotate(angle, expand=1)
        size = channel.size[0]*scale, channel.size[1]*scale
        half_tone = Image.new('L', size)
        draw = ImageDraw.Draw(half_tone)
        for x in xrange(0, channel.size[0], sample):
            for y in xrange(0, channel.size[1], sample):
                box = channel.crop((x, y, x + sample, y + sample))
                stat = ImageStat.Stat(box)
                diameter = (stat.mean[0] / 255)**0.5
                edge = 0.5*(1-diameter)
                x_pos, y_pos = (x+edge)*scale, (y+edge)*scale
                box_edge = sample*diameter*scale
                draw.ellipse((x_pos, y_pos, x_pos + box_edge, y_pos + box_edge), fill=255)
        half_tone = half_tone.rotate(-angle, expand=1)
        width_half, height_half = half_tone.size
        xx=(width_half-im.size[0]*scale) / 2
        yy=(height_half-im.size[1]*scale) / 2
        half_tone = half_tone.crop((xx, yy, xx + im.size[0]*scale, yy + im.size[1]*scale))
        dots.append(half_tone)
        angle += 30
    return dots

image_dir = 'E:/Local Code/Work/Local Code - Los Angeles/08 Images/00 Background Images/batched amigos renders nov 15 12'
new_images = 'E:/Local Code/Work/Local Code - Los Angeles/08 Images/00 Background Images/batched amigos renders nov 15 12/test'
onlyfiles = [ f for f in listdir(image_dir) if isfile(join(image_dir,f))]

csv_file = 'Filename and Funding Only_result.csv'

def remap(number, old_interval, new_interval):
    delta = float(old_interval[1] - old_interval[0])
    t = (number-old_interval[0]) / delta
    new_delta = float(new_interval[1] - new_interval[0])
    return new_delta * t + new_interval[0]
    

df = pd.DataFrame.from_csv(csv_file)
max_val = df['h-actual'].values.max()
min_val = df['h-actual'].values.min()
old_interval = [min_val, max_val]
# Setup a new interval
new_interval = [50, 5]

all_vals = df['h-actual'].values

for index, image in enumerate(onlyfiles):
    im = Image.open(join(image_dir,image))
    img = Image.open(join(image_dir,image)).convert('L')
    
    value = remap(all_vals[index], old_interval, new_interval)
    dots = halftone(im, img, int(value), 1)
    new = Image.merge('L', dots)
    
    new.save(join(new_images,image), 'PNG')