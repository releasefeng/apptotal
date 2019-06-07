#-*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ListProperty
from kivy.graphics import Color, Ellipse
import socket
import threading

Builder.load_string('''
<FourScreen>
    BoxLayout:
        canvas.before:
            Color:
                rgba: 255, 255, 255, 1
        orientation: 'vertical'
        AsyncImage:
            id:kedu
            source: 'kedu.jpg'
            #size_hint: 1, 1
            #pos_hint: {'center_x':.5, 'center_y': .5}
        GridLayout:
            cols:4
		    Label:
		        text:'左速度'
		        font_name:'DroidSansFallback'
		    Label:
		        id:leftmotor
			    text:'0mm/s'
		    Label:
		        text:'右速度'
		        font_name:'DroidSansFallback'
		    Label:
		        id:rightmotor
			    text:'0mm/s'
		    Label:
		        text:'左编码'
		        font_name:'DroidSansFallback'
		    Label:
		        id:leftcode
			    text:'0'
		    Label:
		        text:'右编码'
		        font_name:'DroidSansFallback'
		    Label:
		        id:rightcode
			    text:'0'
			Label:
	            id:controlstat
	            text:'停止'
	            font_name:'DroidSansFallback'
            Button:
                text:"+"
                #on_press:root.MaxSpeed()
            Button:
                text:"-"
                #on_press:root.MinSpeed()
            Label:
                id:speed
                text:'0mm/s'
            Label:
                id:postion
                text:'0,0'
            Button:
                text:"右转圈"
                font_name:'DroidSansFallback'
            Button:
                text:"左转圈"
                font_name:'DroidSansFallback'
''')

class FourScreen(Screen):
    def __init__(self, **kwargs):
        super(FourScreen, self).__init__(**kwargs)

        cb = CustomBtn()
        cb.bind(pressed=self.btn_pressed)

        cu = CustomUnBtn()
        cu.bind(pressed=self.btn_unpressed)

        self.add_widget(cb)
        self.add_widget(cu)

        t= threading.Thread(target=self.start)
        t.setDaemon(True)
        t.start()

    def btn_pressed(self, instance, pos):
        postion=str(int(pos[0]))+','+str(int(pos[1]))
        if int(pos[0])<=390 and int(pos[0]) >=220 and int(pos[1])>=165 and int(pos[1]) <=280:
            self.speedadd()
        elif int(pos[0])<=390 and int(pos[0]) >=220 and int(pos[1])>=30 and int(pos[1]) <=120:
            self.ids['controlstat'].text='右转圈'
            turnr= threading.Thread(target=self.righturnrun)
            turnr.setDaemon(True)
            turnr.start()
        elif int(pos[0])<=580 and int(pos[0]) >=400 and int(pos[1])>=30 and int(pos[1]) <=120:
            self.ids['controlstat'].text='左转圈'
            turnl= threading.Thread(target=self.lefturnrun)
            turnl.setDaemon(True)
            turnl.start()
        elif int(pos[0])<=580 and int(pos[0]) >=400 and int(pos[1])>=165 and int(pos[1]) <=280:
            self.speedsub()
        else:
            self.ids['postion'].text=postion
            self.ids['controlstat'].text='开始'

    def btn_unpressed(self, instance, pos):
        self.ids['controlstat'].text='停止'

    def start(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['controlstat'].text=='开始':
                booPostion,localx,localy=self.getPostion()
                if booPostion:
                    data=self.tock(localx,localy)
                    udpclient.sendto(data.decode('hex'),('192.168.80.201',6650))
                    try:
                        mess=udpclient.recv(1024)
                        flag=1
                    except:
                        flag=0
                    if flag==1:
                        result=mess.encode('hex')
                        self.motorany(result)
                else:
                    pass
            else:
                pass

    def getPostion(self):
        repostion=0
        postion=self.ids['postion'].text
        poslist=str(postion).split(',')
        posx=int(poslist[0])
        posy=int(poslist[1])
        if posx <=596 and posx >=196 and posy<=1110 and posy >=710:
            repostion=1
        else:
            pass
        return repostion,posx,posy

    def speedadd(self):
        currentspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
        targetspeed=currentspeed+10
        self.ids['speed'].text=str(targetspeed)+'mm/s'

    def righturnrun(self):
        currentspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['controlstat'].text=='右转圈':
                if currentspeed==0:
                    rightspeedcode='0000'
                else:
                    rightspeed=65536-currentspeed
                    rightspeedcode=hex(rightspeed).lstrip('0x')
                leftspeedcode=hex(currentspeed).lstrip('0x')
                for i in range(0,4-len(rightspeedcode)):
                    rightspeedcode='0'+rightspeedcode
                for i in range(0,4-len(leftspeedcode)):
                    leftspeedcode='0'+leftspeedcode
                leftvol=leftspeedcode[2]+leftspeedcode[3]+leftspeedcode[0]+leftspeedcode[1]
                rightvol=rightspeedcode[2]+rightspeedcode[3]+rightspeedcode[0]+rightspeedcode[1]
                motorvol=leftvol+rightvol
                mess='59'+'ee'+'ee'+'11'+'10'+motorvol+'11'+'0000'+'000F00'+'000000000000'+'00'
                CRCHi,CRCLo=self.calc(mess.decode('hex'))
                tockmess=mess+CRCLo+CRCHi+'47'
                udpclient.sendto(tockmess.decode('hex'),('192.168.80.201',6650))
                try:
                    mess=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag==1:
                    result=mess.encode('hex')
                    self.motorany(result)
            else:
                break
        udpclient.close()

    def lefturnrun(self):
        currentspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['controlstat'].text=='左转圈':
                if currentspeed==0:
                    leftspeedcode='0000'
                else:
                    leftspeed=65536-currentspeed
                    leftspeedcode=hex(leftspeed).lstrip('0x')
                rightspeedcode=hex(currentspeed).lstrip('0x')
                for i in range(0,4-len(rightspeedcode)):
                    rightspeedcode='0'+rightspeedcode
                for i in range(0,4-len(leftspeedcode)):
                    leftspeedcode='0'+leftspeedcode
                leftvol=leftspeedcode[2]+leftspeedcode[3]+leftspeedcode[0]+leftspeedcode[1]
                rightvol=rightspeedcode[2]+rightspeedcode[3]+rightspeedcode[0]+rightspeedcode[1]
                motorvol=leftvol+rightvol
                mess='59'+'ee'+'ee'+'11'+'10'+motorvol+'11'+'0000'+'000F00'+'000000000000'+'00'
                CRCHi,CRCLo=self.calc(mess.decode('hex'))
                tockmess=mess+CRCLo+CRCHi+'47'
                udpclient.sendto(tockmess.decode('hex'),('192.168.80.201',6650))
                try:
                    mess=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag==1:
                    result=mess.encode('hex')
                    self.motorany(result)
            else:
                break
        udpclient.close()

    def speedsub(self):
        currentspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
        if currentspeed==0:
            pass
        else:
            targetspeed=currentspeed-10
            self.ids['speed'].text=str(targetspeed)+'mm/s'

    def tock(self,posx,posy):
        motorvol='00000000'
        robotdis,robotdir=self.getdirinfo(posx,posy)
        if robotdis=='front':
            targetspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
            if robotdir=='lev1':
                speed=targetspeed/2
            else:
                speed=targetspeed
            hexspeed=hex(speed).lstrip('0x')
            for i in range(0,4-len(hexspeed)):
                hexspeed='0'+hexspeed
            motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if robotdis=='back':
            if self.ids['speed'].text == '0mm/s':
                motorvol='00000000'
            else:
                temp=int(str(self.ids['speed'].text).rstrip('mm/s'))
                if robotdir=='lev1':
                    speed=temp/2
                    targetspeed=65536-speed
                else:
                    speed=temp
                    targetspeed=65536-speed
                hexspeed=hex(targetspeed).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if robotdis=='left':
            targetspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
            if robotdir=='lev1':
                leftarsped=(targetspeed/3)*2
            else:
                leftarsped=targetspeed/3
            hexspeed=hex(targetspeed).lstrip('0x')
            lefthexspeed=hex(leftarsped).lstrip('0x')
            for i in range(0,4-len(hexspeed)):
                hexspeed='0'+hexspeed
            for i in range(0,4-len(lefthexspeed)):
                lefthexspeed='0'+lefthexspeed
            motorvol=lefthexspeed[2]+lefthexspeed[3]+lefthexspeed[0]+lefthexspeed[1]+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if robotdis=='right':
            targetspeed=int(str(self.ids['speed'].text).rstrip('mm/s'))
            if robotdir=='lev1':
                rightarsped=(targetspeed/3)*2
            else:
                rightarsped=targetspeed/3
            hexspeed=hex(targetspeed).lstrip('0x')
            righthexspeed=hex(rightarsped).lstrip('0x')
            for i in range(0,4-len(hexspeed)):
                hexspeed='0'+hexspeed
            for i in range(0,4-len(righthexspeed)):
                righthexspeed='0'+righthexspeed
            motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+righthexspeed[2]+righthexspeed[3]+righthexspeed[0]+righthexspeed[1]
        else:
            pass
        if robotdis=='backleft':
            if self.ids['speed'].text == '0mm/s':
                motorvol='00000000'
            else:
                temp=int(str(self.ids['speed'].text).rstrip('mm/s'))/2
                targetspeed=65536-int(str(self.ids['speed'].text).rstrip('mm/s'))
                leftarsped=65536-temp
                hexspeed=hex(targetspeed).lstrip('0x')
                lefthexspeed=hex(leftarsped).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                for i in range(0,4-len(lefthexspeed)):
                    lefthexspeed='0'+lefthexspeed
                motorvol=lefthexspeed[2]+lefthexspeed[3]+lefthexspeed[0]+lefthexspeed[1]+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if robotdis=='backright':
            if self.ids['speed'].text == '0mm/s':
                motorvol='00000000'
            else:
                temp=int(str(self.ids['speed'].text).rstrip('mm/s'))/2
                targetspeed=65536-int(str(self.ids['speed'].text).rstrip('mm/s'))
                rightsped=65536-temp
                hexspeed=hex(targetspeed).lstrip('0x')
                righthexspeed=hex(rightsped).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                for i in range(0,4-len(righthexspeed)):
                    righthexspeed='0'+righthexspeed
                motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+righthexspeed[2]+righthexspeed[3]+righthexspeed[0]+righthexspeed[1]
        else:
            pass

        mess='59'+'ee'+'ee'+'11'+'10'+motorvol+'11'+'0000'+'000F00'+'000000000000'+'00'
        CRCHi,CRCLo=self.calc(mess.decode('hex'))
        tockmess=mess+CRCLo+CRCHi+'47'
        return tockmess

    def getdirinfo(self,posx,posy):
        if posx>=396 and posx<=596 and posy>=870 and posy<=950:
            distance='front'
            if posx>=396 and posx<=496:
                navi='lev1'
            else:
                navi='lev2'
        elif posx>=396 and posx<=596 and posy>950 and posy<=1030:
            distance='left'
            navi='lev1'
        elif posx>=396 and posx<=596 and posy>1030 and posy<=1110:
            distance='left'
            navi='lev2'
        elif posx>=396 and posx<=596 and posy>=790 and posy<870:
            distance='right'
            navi='lev1'
        elif posx>=396 and posx<=596 and posy>=710 and posy<790:
            distance='right'
            navi='lev2'
        elif posx<396 and posx>=196 and posy>=870 and posy<=950:
            distance='back'
            if posx<396 and posx>=296:
                navi='lev1'
            else:
                navi='lev2'
        elif posx<396 and posx>=196 and posy>950 and posy<=1110:
            distance='backleft'
            navi='None'
        elif posx<396 and posx>=196 and posy>=710 and posy<870:
            distance='backright'
            navi='None'
        else:
            distance='None'
            navi='None'
        #print(navi)
        return distance,navi

    def motorany(self,result):
        leftcode=int(result[20]+result[21]+result[18]+result[19],16)
        leftspeed=self.speedany(result[22:26])
        rightcode=int(result[28]+result[29]+result[26]+result[27],16)
        rightspeed=self.speedany(result[30:34])
        self.ids['leftcode'].text=str(leftcode)
        self.ids['rightcode'].text=str(rightcode)
        self.ids['leftmotor'].text=str(leftspeed)+'mm/s'
        self.ids['rightmotor'].text=str(rightspeed)+'mm/s'

    def speedany(self,data):
        temp=data[2]+data[3]+data[0]+data[1]
        speed=int(temp,16)
        if speed>32768:
            speed=65536-speed
            finaldata='-'+str(speed)
        else:
            finaldata=speed
        return finaldata

    def calc(self,data):
        crc_table=[0x0000,0xC0C1,0xC181,0x0140,0xC301,0x03C0,0x0280,0xC241,0xC601,0x06C0,0x0780,0xC741,0x0500,0xC5C1,0xC481,0x0440,0xCC01,0x0CC0,0x0D80,0xCD41,0x0F00,0xCFC1,0xCE81,0x0E40,0x0A00,0xCAC1,0xCB81,0x0B40,0xC901,0x09C0,0x0880,0xC841,0xD801,0x18C0,0x1980,0xD941,0x1B00,0xDBC1,0xDA81,0x1A40,0x1E00,0xDEC1,0xDF81,0x1F40,0xDD01,0x1DC0,0x1C80,0xDC41,0x1400,0xD4C1,0xD581,0x1540,0xD701,0x17C0,0x1680,0xD641,0xD201,0x12C0,0x1380,0xD341,0x1100,0xD1C1,0xD081,0x1040,0xF001,0x30C0,0x3180,0xF141,0x3300,0xF3C1,0xF281,0x3240,0x3600,0xF6C1,0xF781,0x3740,0xF501,0x35C0,0x3480,0xF441,0x3C00,0xFCC1,0xFD81,0x3D40,0xFF01,0x3FC0,0x3E80,0xFE41,0xFA01,0x3AC0,0x3B80,0xFB41,0x3900,0xF9C1,0xF881,0x3840,0x2800,0xE8C1,0xE981,0x2940,0xEB01,0x2BC0,0x2A80,0xEA41,0xEE01,0x2EC0,0x2F80,0xEF41,0x2D00,0xEDC1,0xEC81,0x2C40,0xE401,0x24C0,0x2580,0xE541,0x2700,0xE7C1,0xE681,0x2640,0x2200,0xE2C1,0xE381,0x2340,0xE101,0x21C0,0x2080,0xE041,0xA001,0x60C0,0x6180,0xA141,0x6300,0xA3C1,0xA281,0x6240,0x6600,0xA6C1,0xA781,0x6740,0xA501,0x65C0,0x6480,0xA441,0x6C00,0xACC1,0xAD81,0x6D40,0xAF01,0x6FC0,0x6E80,0xAE41,0xAA01,0x6AC0,0x6B80,0xAB41,0x6900,0xA9C1,0xA881,0x6840,0x7800,0xB8C1,0xB981,0x7940,0xBB01,0x7BC0,0x7A80,0xBA41,0xBE01,0x7EC0,0x7F80,0xBF41,0x7D00,0xBDC1,0xBC81,0x7C40,0xB401,0x74C0,0x7580,0xB541,0x7700,0xB7C1,0xB681,0x7640,0x7200,0xB2C1,0xB381,0x7340,0xB101,0x71C0,0x7080,0xB041,0x5000,0x90C1,0x9181,0x5140,0x9301,0x53C0,0x5280,0x9241,0x9601,0x56C0,0x5780,0x9741,0x5500,0x95C1,0x9481,0x5440,0x9C01,0x5CC0,0x5D80,0x9D41,0x5F00,0x9FC1,0x9E81,0x5E40,0x5A00,0x9AC1,0x9B81,0x5B40,0x9901,0x59C0,0x5880,0x9841,0x8801,0x48C0,0x4980,0x8941,0x4B00,0x8BC1,0x8A81,0x4A40,0x4E00,0x8EC1,0x8F81,0x4F40,0x8D01,0x4DC0,0x4C80,0x8C41,0x4400,0x84C1,0x8581,0x4540,0x8701,0x47C0,0x4680,0x8641,0x8201,0x42C0,0x4380,0x8341,0x4100,0x81C1,0x8081,0x4040]
        crc_hi=0xFF
        crc_lo=0xFF
        for w in data:
            index=crc_lo ^ ord(w)
            crc_val=crc_table[index]
            crc_temp=crc_val/256
            crc_val_low=crc_val-(crc_temp*256)
            crc_lo=crc_val_low ^ crc_hi
            crc_hi=crc_temp
        crc=crc_hi*256 +crc_lo
        crc_hi = hex(crc/256).lstrip('0x')
        if len(crc_hi)==1:
            crc_hi='0'+crc_hi
        crc_lo = hex(crc & 0xFF).lstrip('0x')
        if len(crc_lo)==1:
            crc_lo='0'+crc_lo
        return crc_hi,crc_lo

class CustomBtn(Widget):
    pressed = ListProperty([0, 0])
    def on_touch_down(self, touch):
        if touch.x>=196 and touch.x<=596 and touch.y>=710 and touch.y<=1110:
            with self.canvas:
                Color(1,1,0)
                d = 60.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.x>=196 and touch.x<=596 and touch.y>=710 and touch.y<=1110:
            self.canvas.clear()
            with self.canvas:
                Color(1,1,0)
                d = 60.
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            #print('The touch is at position', touch.pos)
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            #print('The touch is at position', touch.pos)
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_up(touch)

    def on_pressed(self, instance, pos):
        pass
        #print ('pressed at {pos}'.format(pos=pos))

class CustomUnBtn(Widget):
    pressed = ListProperty([0, 0])
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            #print('The touch is at position', touch.pos)
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomUnBtn, self).on_touch_up(touch)

    def on_pressed(self, instance, pos):
        pass
        #print ('pressed at {pos}'.format(pos=pos))

class YopkApp(App):
    def build(self):
        return FourScreen()

YopkApp().run()