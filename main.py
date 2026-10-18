import pygame,random,math,sys
pygame.init()

s=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
W,H=s.get_size(); c=pygame.time.Clock()

sky=(90,175,230); green=(35,145,65); white=(245,245,245)
red=(225,55,60); yellow=(255,205,55); black=(15,15,18)

gw,gh=int(W*.7),int(H*.25)
gx=(W-gw)//2; gy=int(H*.13)
ground=int(H*.38)
bx,by=W/2,H*.82
r=int(W*.024)

score=attempt=0
shoot=False; aim=False; over=False
ax,ay=bx,by-100
tx,ty=bx,by
p=0
kx=W/2; kt=W/2
msg=""

font=pygame.font.Font(None,int(W*.07))

def reset():
    global bx,by,shoot,p,ax,ay,kx
    bx,by=W/2,H*.82; shoot=False;p=0
    ax,ay=bx,by-100;kx=W/2

def start_shot():
    global shoot,tx,ty,p,kt
    shoot=True;p=0
    tx=max(gx+20,min(ax,gx+gw-20))
    ty=max(gy+20,min(ay,ground-20))
    kt=random.choice([gx+gw*.2,gx+gw*.5,gx+gw*.8])

reset()

while 1:
    dt=c.tick(60)

    for e in pygame.event.get():

        if e.type==pygame.QUIT:
            pygame.quit();sys.exit()

        if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
            pygame.quit();sys.exit()

        if e.type==pygame.MOUSEBUTTONDOWN:
            x,y=e.pos

            if over:
                if W/2-130<x<W/2+130 and H/2+30<y<H/2+110:
                    score=attempt=0;over=False;msg="";reset()
            elif not shoot:
                aim=True;ax,ay=x,y

        if e.type==pygame.MOUSEMOTION and aim and not shoot:
            ax=max(gx+10,min(e.pos[0],gx+gw-10))
            ay=max(gy+10,min(e.pos[1],H*.79))

        if e.type==pygame.MOUSEBUTTONUP and aim and not shoot:
            aim=False
            if math.hypot(ax-W/2,ay-H*.82)>45:
                start_shot()

    # bola & kiper smooth
    if shoot:
        p=min(1,p+.035)
        q=1-(1-p)**3
        bx=(W/2)+(tx-W/2)*q
        by=(H*.82)+(ty-H*.82)*q
        kx+=((kt-kx)*.13)

        if p>=1:
            save=abs(kx-tx)<r*3 and abs(ty-(ground-H*.06))<H*.14
            msg="DITANGKAP!" if save else "GOOOL!"
            if not save: score+=1
            attempt+=1;shoot=False
            if attempt>=5: over=True
            reset()

    # gambar
    s.fill(sky)
    pygame.draw.rect(s,green,(0,ground,W,H-ground))

    # gawang + jaring
    pygame.draw.rect(s,white,(gx,gy,gw,ground-gy),5)
    for x in range(gx,gx+gw,30):
        pygame.draw.line(s,(200,205,210),(x,gy),(x,ground),1)

    # kiper
    ky=ground-int(H*.06)
    pygame.draw.rect(s,red,(kx-W*.052,ky,W*.104,H*.13),border_radius=10)
    pygame.draw.circle(s,(235,180,135),(int(kx),ky-18),18)

    # garis arah
    if aim and not shoot:
        pygame.draw.line(s,white,(W/2,H*.82),(ax,ay),3)
        pygame.draw.circle(s,white,(int(ax),int(ay)),8)

    # bola
    pygame.draw.circle(s,white,(int(bx),int(by)),r)
    pygame.draw.circle(s,black,(int(bx),int(by)),r,2)

    # skor
    text=font.render(f"PENALTY   {score}/5",True,white)
    s.blit(text,(W/2-text.get_width()/2,20))

    if msg:
        t=font.render(msg,True,yellow if msg=="GOOOL!" else white)
        s.blit(t,(W/2-t.get_width()/2,int(H*.30)))

    if over:
        ov=pygame.Surface((W,H));ov.set_alpha(190);ov.fill(black);s.blit(ov,(0,0))
        t=font.render(f"SELESAI  {score}/5",True,white)
        s.blit(t,(W/2-t.get_width()/2,H/2-80))
        b=pygame.Rect(W/2-130,H/2+30,260,80)
        pygame.draw.rect(s,(55,110,220),b,border_radius=15)
        t=font.render("MAIN LAGI",True,white)
        s.blit(t,(W/2-t.get_width()/2,H/2+50))

    pygame.display.flip()
