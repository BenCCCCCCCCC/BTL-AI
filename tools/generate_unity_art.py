"""Original deterministic pixel art for the internal chapter; no model or network calls."""
from pathlib import Path
from random import Random
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / 'unity/BTL/Assets/BTL/Art'
OUT.mkdir(parents=True, exist_ok=True)
rng = Random(1701)
INK, DARK, STEEL, TEAL = '#18232c', '#24333b', '#526367', '#69817a'
GOLD, LIGHT, PAPER, RED = '#bc9558', '#e9c98b', '#d5cbb2', '#914d46'

def canvas():
    im = Image.new('RGB', (400, 225), INK)
    return im, ImageDraw.Draw(im)

def rect(d, box, c): d.rectangle(box, fill=c)

def window(d, box):
    x,y,w,h = box
    rect(d,(x-3,y-3,x+w+3,y+h+3),'#111c25')
    rect(d,(x,y,x+w,y+h),'#31454f')
    for xx in range(x+4,x+w-8,14):
        top=y+rng.randint(8,35)
        rect(d,(xx,top,xx+10,y+h),DARK)
        for yy in range(top+4,y+h-4,8):
            if rng.random()>.4: rect(d,(xx+3,yy,xx+5,yy+2),GOLD)
    for yy in range(y+8,y+h,9): rect(d,(x,yy,x+w,yy+1),'#52616a')
    rect(d,(x+w//2-2,y,x+w//2+2,y+h),'#17252e')

def paper(d,x,y,w=35,h=25):
    rect(d,(x+2,y+2,x+w+2,y+h+2),'#1c272c')
    rect(d,(x,y,x+w,y+h),PAPER)
    for yy in range(y+5,y+h-4,4): rect(d,(x+4,yy,x+w-rng.randint(5,12),yy),'#8b8e7e')

im,d=canvas()
rect(d,(0,0,399,147),'#3a4546'); window(d,(29,20,127,103))
rect(d,(173,16,283,116),'#273639');rect(d,(179,22,277,110),'#827e69')
for x,y in [(185,30),(230,35),(197,72),(244,70)]: paper(d,x,y,23,27)
rect(d,(294,0,301,151),'#26353b');rect(d,(0,142,399,152),GOLD)
rect(d,(0,153,399,224),'#493f37')
for y in range(161,225,12):rect(d,(0,y,399,y),'#5b4d3d')
paper(d,178,163,83,42);paper(d,190,159,70,40)
rect(d,(196,166,252,173),'#34434a');rect(d,(198,168,234,170),PAPER)
# Desk lamp and pool of light.
d.polygon([(292,138),(337,138),(385,214),(235,214)],fill='#786744')
rect(d,(321,99,324,169),STEEL);rect(d,(310,168,338,174),INK)
d.polygon([(306,108),(339,108),(351,140),(290,140)],fill=TEAL)
rect(d,(295,139,346,142),LIGHT)
# Typewriter, coffee, pencil.
rect(d,(49,172,135,204),'#17262c');rect(d,(60,155,124,180),STEEL)
paper(d,67,143,51,34)
for x in range(55,132,10):
    for y in (184,193):rect(d,(x,y,x+6,y+4),'#a9ac99')
rect(d,(149,180,163,197),PAPER);rect(d,(163,183,168,192),GOLD)
d.line((272,188,302,173),fill=GOLD,width=2)
im.save(OUT/'desk.png')

im,d=canvas()
for y in range(225):rect(d,(0,y,399,y), '#22313d' if y<65 else '#2e414b' if y<130 else '#3d4947')
rect(d,(0,84,399,125),'#1a2932')
for x in range(0,400,36):rect(d,(x,67+rng.randint(0,17),x+30,130),'#243842')
# Yard shed and corrugated container.
d.polygon([(23,100),(77,73),(172,73),(191,100)],fill='#576768')
rect(d,(38,100,182,163),'#263b42')
for x in (41,111,176):rect(d,(x,100,x+3,165),'#61736f')
rect(d,(225,111,344,162),'#616e66')
for x in range(230,341,7):rect(d,(x,113,x+1,161),'#3e5355')
rect(d,(225,112,344,115),'#8b9581')
# Light poles; no action depicted, so the background discloses no evidence.
for x in (199,362):
    d.polygon([(x-26,160),(x-6,74),(x+6,74),(x+31,160)], fill='#586352')
    rect(d,(x,61,x+3,173),'#182a32');rect(d,(x-8,62,x+13,67),GOLD);rect(d,(x-5,66,x+10,69),LIGHT)
for x in range(-70,401,64):
    d.line((190,137,x,224),fill='#202f36',width=3)
    d.line((202,137,x+23,224),fill='#8c8d76',width=1)
for y in (166,176,190,208):rect(d,(0,y,399,y+2),'#253a42')
# Foreground fence and empty stool.
for x in range(5,160,24):d.line((x,128,x+35,193),fill=STEEL,width=1)
rect(d,(4,127,7,218),DARK);rect(d,(146,127,150,224),DARK)
rect(d,(69,183,96,188),GOLD);rect(d,(72,188,75,213),INK);rect(d,(91,188,94,213),INK)
for _ in range(70):
    x,y=rng.randrange(400),rng.randrange(160,225)
    rect(d,(x,y,x+3,y), '#596b68')
im.save(OUT/'yard.png')

im,d=canvas()
rect(d,(0,0,399,159),'#354345');window(d,(267,21,103,86))
for x in (19,97,175):
    rect(d,(x,12,x+65,152),'#23363d')
    for y in (42,81,120):
        for xx in range(x+5,x+60,9):
            rect(d,(xx,y-24,xx+6,y-1),rng.choice([STEEL,TEAL,'#8e8568','#705b4b']))
            rect(d,(xx+1,y-18,xx+4,y-16),PAPER)
        rect(d,(x,y,x+65,y+3),'#a19573')
rect(d,(0,159,399,224),'#685740');rect(d,(0,159,399,163),'#ad946a')
paper(d,219,176,97,39);paper(d,228,170,95,38)
for x in (246,270,293):rect(d,(x,175,x,203),'#7d8374')
rect(d,(38,179,124,206),'#303c41');rect(d,(42,176,118,199),'#697a74')
rect(d,(55,181,108,186),PAPER);rect(d,(136,183,160,205),RED)
rect(d,(142,173,154,188),INK);rect(d,(339,158,342,203),GOLD)
im.save(OUT/'records.png')

def portrait(name,coat,hair,skin,shirt,glasses=False):
    im=Image.new('RGBA',(80,96),(0,0,0,0));d=ImageDraw.Draw(im)
    d.polygon([(7,95),(12,69),(29,60),(51,60),(68,69),(74,95)],fill=coat)
    rect(d,(33,53,47,71),skin)
    d.polygon([(26,64),(40,78),(54,64),(50,95),(30,95)],fill=shirt)
    d.polygon([(21,24),(27,13),(49,12),(59,23),(57,49),(48,62),(32,60),(22,47)],fill=skin)
    d.polygon([(21,37),(19,20),(25,9),(48,7),(60,19),(59,38),(54,23),(31,23),(25,34)],fill=hair)
    rect(d,(29,35,33,37),INK);rect(d,(47,35,51,37),INK)
    rect(d,(39,38,41,46),'#987a68');rect(d,(34,51,47,52),'#805d50')
    if glasses:
        d.rectangle((26,31,36,41),outline=INK,width=2);d.rectangle((44,31,54,41),outline=INK,width=2)
        rect(d,(36,34,44,35),INK)
    d.line((15,74,10,95),fill='#586466',width=2);d.line((64,75,69,95),fill='#17252f',width=3)
    im.save(OUT/(name+'.png'))
portrait('editor', '#4b565c','#51585b','#c4a48b','#b9b7a1',True)
portrait('witness','#617267','#28323a','#bc9b80','#48545a')
portrait('clerk','#4c5c68','#202c35','#c3aa92','#c7c6af',True)
print('Generated three 400x225 scenes and three 80x96 portraits in',OUT)
