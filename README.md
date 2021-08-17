# __Pybasic (Treasure Hunter Game)__

PyC basic으로 AIot 프로그래밍 및 python3 와 C++ 를 학습하며 Pop라이브러리 활용, blynk를 이용하여 원격조정

### Treasue Hunter 설명
2x2의 캐릭터를 움직여 랜덤으로 생성되는 보물들과 접촉하는 게임, 더 이상 보물이 없을시에 게임 클리어
'''
### 개발환경
- __Hardware__
  -Pyc basic
    - Nvidia Jetson Xavier AGX Board
    - Sensor Block
    - 8x8 Pixel Display
    - Psd Sensor
    - OLed, Led
    - Passice Buzzer
    - Switch input
  
- __Software__
  - Pop lib
    - Pixel
    - Potntiometer
    - Oled
    - PiezoBuzzer
    - Sht20
    - Blynk

## __개발환경 구성__
### Pop 라이브러리
Pyc baic에는 기본적으로 Os인 soda가 설치되어 있다. 따로 설치할 필요가 없음.

## __동작 테스트_
![KakaoTalk_20210430_135713997](https://user-images.githubusercontent.com/81665489/116650436-0bb09600-a9bc-11eb-98c9-8f86765368f9.png)
[조작 UI]
| Pin | 버튼 | 기능 |
|---|:---:|---:|
| `V0` | 버튼(스위치) |왼쪽으로 이동 (←) | 
| `V1` | 버튼(스위치) |오른쪽으로 이동 (→) |
| `V2` | 버튼(스위치) |위쪽으로 이동 (↑) |
| `V3` | 버튼(스위치) |아래쪽으로 이동 (↓) |
| `V5` | 버튼(스위치) | 시 작 |
| `V9` | 게이지 | 온도 측정 | 
| `V10` | 게이지 | 습도 측정 |



![KakaoTalk_20210430_135713881](https://user-images.githubusercontent.com/81665489/116650433-0a7f6900-a9bc-11eb-8c53-5064a16e51e1.png)
[Pyc basic]




## __Pop 라이브러리 활용 예제__
### 캐릭터(2x2)의 기본 설정 및 활용 - 1
```python
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

    #trs = {(x,y), (x,y), (x,y) (,) (,) (,)}
    print("보물 개수설정 - Potentiometer(+5)")
    for i in range(3):
        print(3-i,"초")
    time.sleep(1)

    num = 5+int(pt.readVoltAverage()*10/3) # 보물의 개수 
    trs = set()
    usr_x = 3
    usr_y = 4

    while len(trs) < num:                  # 보물의 위치설정(집합)
      trs.add((randint(0,7), randint(0,7)))
      trs.discard((3,3))
      trs.discard((4,3))
      trs.discard((3,4))
      trs.discard((4,4))

    print(trs)
```

### 캐릭터(2x2)의 기본 설정 및 활용 - 2
```python
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
    
    def black(n):
      x = usr_x
      y = usr_y
      blc = [0,0,0]   # black
      
      pixel.setColor(x, y, blc)
      pixel.setColor(x+1, y, blc)
      pixel.setColor(x, y-1, blc)
      pixel.setColor(x+1, y-1, bl
```
### 캐릭터(2x2)의 기본 설정 및 활용 - 3 (Control)
  '''python
  @blynk.VIRTUAL_WRITE(1)
   def pix_right(n):
   global usr_x,mv_cnt
  
   
   
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
       '''
### 캐릭터(2x2)의 기본 설정 및 활용 - 4 (Score)
  '''python
 while True:
    blynk.run()

    # trs_n = len(trs)
    # if len(trs)<trs_n:
    #     print(trs)
    #     trs_n-=1

    #print(trs)
    if len(trs)==0:
        print(" Game Clear")
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
        
        time.sleep(5)
       '''
       
### 게임 클리어시 Led를 활용한 예제(ening)
  '''python
 end = randint(1,4)

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
       '''
       
       
## Reference
'''
https://onefeel.tistory.com/510 
https://github.com/blynkkk/lib-python/blob/master/examples/08_blynk_timer.py
'''

       
      
       
       
