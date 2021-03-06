import os
import subprocess
import sys
from PIL import Image, ImageTk
from random import randint, shuffle

from Tkinter import Tk, Frame, BOTH, Label, Button
import tkFileDialog

def run():
	num_scenes = 10 # at least 2!
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

	new_im = new_im.resize((1920,192))
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

	new_im = Image.new('RGB', (total_width, max_height))

	x_offset = 0
	for im in images:
	  new_im.paste(im, (x_offset,0))
	  x_offset += im.size[0]

	new_im.save('platformer.png')

	updateImage()
	root.after(100, run)

def updateImage(seedfile='default.png'):
	seed = ImageTk.PhotoImage(Image.open(seedfile))
	random = ImageTk.PhotoImage(Image.open("random.png"))		
	platformer = ImageTk.PhotoImage(Image.open("platformer.png"))
	if seedfile != 'default.png':
		random = None
		platformer = None
	panel1.configure(image = platformer)
	panel2.configure(image = random)
	panel3.configure(image = seed)
	panel1.image = platformer
	panel2.image = random
	panel3.image = seed

def quit():
	root.quit()

def load():
	filename = tkFileDialog.askopenfilename(parent=root,title='Choose a file')
	if len(filename) > 0:
		updateImage(filename)


root = Tk()
seed = ImageTk.PhotoImage(Image.open("default_white.png"))
random = ImageTk.PhotoImage(Image.open("random_white.png"))
platformer = ImageTk.PhotoImage(Image.open("platformer_white.png"))
panel1 = Label(root, image = platformer)
panel1.configure(bg='white')
panel1.pack(side = "bottom", fill = "both", expand = "yes")
panel2 = Label(root, image = random)
panel2.configure(bg='white')
panel2.pack(side = "bottom", fill = "both", expand = "yes")
panel3 = Label(root, image = seed)
panel3.configure(bg='white')
panel3.pack(side = "bottom", fill = "both", expand = "yes")
Button(root, text="Load", command=load).pack(pady=5)
Button(root, text="Start", command=run).pack(pady=5)
Button(root, text="Quit", command=quit).pack(pady=5)
root.configure(bg='white')

root.mainloop()


