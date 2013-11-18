#!/usr/bin/python
import Image, ImageDraw

#im = Image.open("lena.pgm")
img = Image.new('L', (1200,500), color=0)
text1 = 'GET /qik_production/photos/6/scoblecam_highres.jpg \n 3.amazonaws.com'
draw = ImageDraw.Draw(img)
#draw.line((0, 0) + img.size, fill=128)
#draw.line((0, img.size[1], img.size[0], 0), fill=128)
#draw.line((0,0) + (0,256), fill=1, width=10)
sizex, sizey = draw.textsize(text1)
#print sizex, sizey

aspect = 20
for i in range(0,10):
    text_size = 450
    time_size = 220
    time_shift = 10
    draw.text((0,(aspect)*i), text1, fill=100)
    draw.line((text_size + time_shift*i,aspect*i) + (time_size + text_size + time_shift*i,i*aspect), fill=128, width=15)
    
    
"""
draw.text((0,0), text1, fill=100)
draw.line((450,0) + (770,0), fill=128, width=15)

draw.text((0,20), text1, fill=100)
draw.line((450,20) + (770,20), fill=128, width=15)

draw.text((0,40), text1, fill=100)
draw.line((450,40) + (770,40), fill=128, width=15)
"""
del draw

# write to stdout
#img.save(sys.stdout, "PNG")
img.save("/tmp/box.png", transparency=0)


