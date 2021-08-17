import BlynkLib
from pop import PiezoBuzzer, Sht20, Potentiometer, Oled, PixelDisplay
from random import randint
import time
# import song

blynk = BlynkLib.Blynk('GWrezZR3LRG7VJtChNtMhWwvA9E1dvqX', server='127.0.0.1', port='8080')
# blynk = BlynkLib.Blynk('GWrezZR3LRG7VJtChNtMhWwvA9E1dvqX', server='127.0.0.1', port='8080')

pixel=PixelDisplay()
pt = Potentiometer()
sht = Sht20()
tmp = sht.readTemp()
hum = sht.readHumi()
mv_cnt = 0
oled = Oled()
start_time=0


@blynk.VIRTUAL_READ(9)
def on_tmp():
    blynk.virtual_write(9, int(tmp))

@blynk.VIRTUAL_READ(10)
def on_hum():
    blynk.virtual_write(10, int(hum))



oled.setCursor(20, 30)
oled.print("Game Start") 
print("Game Start")

if tmp<=15: rgb_tp=(0,255,0)        # 온도 색깔
elif 15<tmp<=25: rgb_tp=(238,43,21)
elif 25<tmp<=35: rgb_tp=(255,236,4)
elif 35<tmp: rgb_tp=(255,0,0)

if hum<=20: rgb_hm=(255,255,255)    # 습도 색깔
elif 20<hum<=50: rgb_hm=(149,202,255)
elif 20<hum<=80: rgb_hm=(0,0,255)
elif 80<hum: rgb_hm=(2,10,49)

#trs = [[x,y][x,y][x,y][][][]]
print("보물 개수설정 - Potentiometer(+5)")
for i in range(3):
    print(3-i,"초")
    time.sleep(1)

num = 5+int(pt.readVoltAverage()*10/3)  # 보물 개수
trs = set()
usr_x = 3
usr_y = 4
# rgb_hm = (0,0,255)
# rgb_tp = (255,0,0)

while len(trs) < num:
    trs.add((randint(0,7), randint(0,7)))
    trs.discard((3,3))
    trs.discard((4,3))
    trs.discard((3,4))
    trs.discard((4,4))

print(trs)



def show(n):
    global trs

    for i in trs:
        pixel.setColor(i[0],i[1],rgb_hm)
    
    trs.discard((usr_x,usr_y))
    trs.discard((usr_x+1,usr_y))
    trs.discard((usr_x,usr_y-1))
    trs.discard((usr_x+1,usr_y-1))
    
    pixel.setColor(usr_x,usr_y,rgb_tp)
    pixel.setColor(usr_x+1,usr_y,rgb_tp)
    pixel.setColor(usr_x,usr_y-1,rgb_tp)
    pixel.setColor(usr_x+1,usr_y-1,rgb_tp)

    return()

# while True:
#     show()  



def black(n):
    x = usr_x
    y = usr_y
    blc = [0,0,0]   # black
    
    pixel.setColor(x, y, blc)
    pixel.setColor(x+1, y, blc)
    pixel.setColor(x, y-1, blc)
    pixel.setColor(x+1, y-1, blc)
    
    #time.sleep(0.1)
    return()


@blynk.VIRTUAL_WRITE(1)
def pix_right(n):
    global usr_x,mv_cnt
   # global pixel
    
    
    for i in n:
        if i=="1" or i=="0":
            black(n)
            if usr_x >= 6:
                usr_x = 6
                show(n)
            else:
                usr_x += 1
                mv_cnt +=1
                show(n)

        buzzer = PiezoBuzzer()
        buzzer.setTempo(120)
        buzzer.tone(4,8,6) #솔

        #print(loc_x)


@blynk.VIRTUAL_WRITE(0)
def pix_left(n):
    global usr_x,mv_cnt

    for i in n:
        if i=="1" or i=="0":
            black(n)
            if usr_x <= 0:
                usr_x = 0 
                show(n)   
            else:
                usr_x -= 1
                mv_cnt +=1
                show(n)

        
        buzzer = PiezoBuzzer()
        buzzer.setTempo(120)
        buzzer.tone(4,1,6) #도

        #print(loc_x)


@blynk.VIRTUAL_WRITE(2)
def pix_up(n):
    global usr_y,mv_cnt

    for i in n:
        if i=="1" or i=="0":
            black(n)
            if usr_y <= 1:
                usr_y = 1 
                show(n)   
            else:
                usr_y -= 1
                mv_cnt +=1
                show(n)

        buzzer = PiezoBuzzer()
        buzzer.setTempo(120)
        buzzer.tone(5,1,6) #도
    #print(y)

@blynk.VIRTUAL_WRITE(3)
def pix_down(n):
    global usr_y,mv_cnt

    for i in n:
        if i=="1" or i=="0":
            black(n)
            if usr_y >= 7:
                usr_y = 7 
                show(n)   
            else:
                usr_y += 1
                mv_cnt +=1
                show(n)

        buzzer = PiezoBuzzer()
        buzzer.setTempo(120)
        buzzer.tone(4,5,6) #미
        

        # print(usr_y)

@blynk.VIRTUAL_WRITE(5)
def start(n):
    start_time = time.time()
    show(n)


# @blynk.VIRTUAL_READ(4)
# def tmn(n):
#     terminal.print()

# @blynk.VIRTUAL_WRITE(6)
# def level(n):
#     global num
#     num = int(n[0])

#     threading.Thread().start()

# @blynk.VIRTUAL_WRITE(6)
# def slider():
#     val = readAverage(n)
#     return()
        #Blynk.virualWrite(2, n)
    
  
if __name__=="__main__":
    pass
    #show(1)



while True:
    blynk.run()

    # trs_n = len(trs)
    # if len(trs)<trs_n:
    #     print(trs)
    #     trs_n-=1

    #print(trs)
    if len(trs)==0:
        print(" Game Clear     ")
        oled.setCursor(20, 30)
        oled.clearDisplay()
        oled.print("Game Clear")
        # print("실행 시간: ",time.time()-start)
        if start_time==0: start_time=time.time()-30
        tt = time.time()-start_time
        if tt>100: tt=100
        score = 100 - mv_cnt - int(tt)
        if score<=0: score=0
        
        sc_p = (10,20,30,40,50,60,70,100)
        gr_p = ('F','D','C','B','A','S','SS','KR')

        for i in range(len(sc_p)): 
            if score<=sc_p[i]: gr= gr_p[i]; break
        
        print("점수 : ", score , ", ", gr)
        #print("실행 시간: ",time.time()-start)
      
        time.sleep(5)

        end = 4#randint(1,4)

        if end==1:
            for _ in range(3):
                rgb = [randint(0,255),randint(0,255),randint(0,255)]
                for p in range(0,4):
                    for i in range(0,8-(p*2)): pixel.setColor(i+p,0+p,rgb); time.sleep(0.05)
                    for j in range(0,7-(p*2)): pixel.setColor(7-p,j+1+p,rgb); time.sleep(0.05)

                    for i in range(0,7-(p*2)): pixel.setColor(6-i-p,7-p,rgb); time.sleep(0.05)
                    for j in range(0,6-(p*2)): pixel.setColor(0+p,6-j-p,rgb); time.sleep(0.05)
            
        elif end==2:
            for _ in range(3):
                rgb = [randint(0,255),randint(0,255),randint(0,255)]
                for p in range(3,-1,-1):
                    for j in range(0,6-(p*2)): pixel.setColor(0+p,6-j-p,rgb); time.sleep(0.05)
                    for i in range(0,7-(p*2)): pixel.setColor(6-i-p,7-p,rgb); time.sleep(0.05)
                    
                    for j in range(0,7-(p*2)): pixel.setColor(7-p,j+1+p,rgb); time.sleep(0.05)
                    for i in range(0,8-(p*2)): pixel.setColor(i+p,0+p,rgb); time.sleep(0.05)

        elif end==3:

            # 장애물 생성
            max_num = 5                 # 최대 5개
            cnt = 0                     # 장애물 번호
            rain_list = []
            speed = 1/40

            for i in range(30):          # 장애물 개수
                num = randint(0,7)

                if i < 5: rain_list.append(num)
                else: rain_list[cnt%max_num] = num
                cnt += 1            
                                    
            # 장애물 하강                            
                ii = i%5
                y = 0
                rgb = [randint(0,255),randint(0,255),randint(0,255)] # 장애물 color
                blc = [0,0,0]               # black

                while y <= 7:
                    #print("x:{}, y:{}".format(rain_list[ii], y))
                    pixel.setColor(rain_list[ii], y, rgb)
                    y += 1
                    time.sleep(speed)
                    pixel.setColor(rain_list[ii], y-1, blc)

                    if y==6 and (rain_list[ii]==usr_x or rain_list[ii]==usr_x+1):
                        score -= 10

                time.sleep(0.3)

        elif end==4:
            pixel.rainbow()
            song.piezo_buzzer()
        break

    
        #rain()  
