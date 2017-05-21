import os
import subprocess
import sys
from PIL import Image
from random import randint, shuffle

num_scenes = 10
filenames = []

img = Image.open('samples/platformer.bmp')
images = [ img.crop((x,0,x+1,32)) for x in range(72) ]
images = [ images[randint(0,len(images)-1)] for i in range(320) ]

widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('random.png')


for i in range(num_scenes/2):
	x1 = -1
	while x1 not in range(21)+range(29,34)+range(42,48):
		x1 = randint(0,18)*4
	x2 = x1 + 18	
	tmp = img.crop((x1,0,x2,32))
	tmp.save('tmp/platformer_'+str(i)+'.bmp')

with open('samples.cfg','w+') as config:
	config.write('image_dir:"tmp/"\n\noverlapping: {\n')
	for i,filename in enumerate(os.listdir('tmp/')):
		config.write('	"platformer'+str(i)+'":      { image: "'+filename+'"  n: 3 symmetry:     2     foundation:  true               }\n')
	config.write('}')


subprocess.Popen(['./call_main.sh']).wait()

images = [ Image.open('output/'+f) for f in os.listdir('output/') ]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)
print max_height

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('platformer.png')
