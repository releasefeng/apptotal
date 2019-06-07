#-*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ListProperty
import socket
import threading

Builder.load_string('''
<OneScreen>
    GridLayout:
        cols:4
	    Label:
		    text:'红外1'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf1value
			text:'0'
		Label:
		    text:'红外2'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf2value
			text:'0'
		Label:
		    text:'红外3'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf3value
			text:'0'
		Label:
		    text:'红外4'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf4value
			text:'0'
		Label:
		    text:'红外5'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf5value
			text:'0'
		Label:
		    text:'红外6'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf6value
			text:'0'
		Label:
		    text:'红外7'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf7value
			text:'0'
		Label:
		    text:'红外8'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf8value
			text:'0'
		Label:
		    text:'红外9'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf9value
			text:'0'
		Label:
		    text:'红外10'
		    font_name:'DroidSansFallback'
		Label:
		    id:infavalue
			text:'0'
		Label:
		    text:'超声1'
		    font_name:'DroidSansFallback'
		Label:
		    id:ult1value
			text:'0'
		Label:
		    text:'超声2'
		    font_name:'DroidSansFallback'
		Label:
		    id:ult2value
			text:'0'
		Label:
		    text:'超声3'
		    font_name:'DroidSansFallback'
		Label:
		    id:ult3value
			text:'0'
		Label:
		    text:'超声4'
		    font_name:'DroidSansFallback'
		Label:
		    id:ult4value
			text:'0'
		Label:
		    text:'超声5'
		    font_name:'DroidSansFallback'
		Label:
		    id:ult5value
			text:'0'
		Label:
		    text:'超声6'
		    font_name:'DroidSansFallback'
		Label:
		    id:ult6value
			text:'0'
		Label:
		    text:'充电状态'
		    font_name:'DroidSansFallback'
		Label:
		    id:batstat
			text:'unknow'
			font_name:'DroidSansFallback'
		Label:
		    text:'电量'
		    font_name:'DroidSansFallback'
		Label:
		    id:batvalue
			text:'0'

		Label:
		    text:'俯仰角'
		    font_name:'DroidSansFallback'
		Label:
		    id:Pithvalue
			text:'0'
		Label:
		    text:'偏航角'
		    font_name:'DroidSansFallback'
		Label:
		    id:Yawvalue
			text:'0'
		Label:
		    text:'翻滚角'
		    font_name:'DroidSansFallback'
		Label:
		    id:rollvalue
			text:'0'
		Label:
		    text:'跌落检测'
		    font_name:'DroidSansFallback'
		Label:
		    id:fallstat
			text:'unknow'
			font_name:'DroidSansFallback'

		Label:
		    text:'上限位'
		    font_name:'DroidSansFallback'
		Label:
		    id:switchup
		    text:'unknow'
		    font_name:'DroidSansFallback'
		Label:
		    text:'下限位'
		    font_name:'DroidSansFallback'
		Label:
		    id:switchdown
		    text:'unknow'
		    font_name:'DroidSansFallback'

		Label:
		    text:'碰撞检测'
		    font_name:'DroidSansFallback'
		Label:
		    id:pith
			text:'unknow'
			font_name:'DroidSansFallback'
		Label:
		    text:'电机状态'
		    font_name:'DroidSansFallback'
		Label:
		    id:motorstat
		    text:'unknow'
		    font_name:'DroidSansFallback'
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
		ToggleButton:
	        id:front
	        text:'前进'
	        font_name:'DroidSansFallback'
	        on_press:root.ActionFront()
	    ToggleButton:
	        id:back
	        text:'后退'
	        font_name:'DroidSansFallback'
	        on_press:root.ActionBack()
	    ToggleButton:
	        id:turnleft
	        text:'左掉头'
	        font_name:'DroidSansFallback'
	        on_press:root.Actionleft()
	    ToggleButton:
	        id:turnright
	        text:'右掉头'
	        font_name:'DroidSansFallback'
	        on_press:root.Actionright()
	    ToggleButton:
	        id:turnrun
	        text:'转圈'
	        font_name:'DroidSansFallback'
	        on_press:root.Actionturn()
	    Button:
            text:"+"
            on_press:root.MaxSpeed()
        Button:
            text:"-"
            on_press:root.MinSpeed()
        Label:
            id:speed
            text:'0'

        ToggleButton:
	        id:ControlStart
	        text:'控制'
	        font_name:'DroidSansFallback'
	        on_release:root.mainany()
	    ToggleButton:
	        id:motorenable
	        text:'电机释放'
	        font_name:'DroidSansFallback'

        Button:
            id:duoji
            text:"门机控制"
            font_name:'DroidSansFallback'
            on_press:root.manager.current="sub"

        Button:
            id:udsfind
            text:"诊断"
            font_name:'DroidSansFallback'
            on_press:root.manager.current="UDS"

        Button:
            id:motorcontrol
            text:"转盘遥控"
            font_name:'DroidSansFallback'
            on_press:root.manager.current="Motor"

        ToggleButton:
	        id:MonitorControl
	        text:'监控'
	        font_name:'DroidSansFallback'
	        on_release:root.monitor()

<TwoScreen>
    GridLayout:
        cols:4
		Label:
			text:'左上舵机'
			font_name:'DroidSansFallback'
		Switch:
	        id:leftupduoji
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:leftupduojistate
	        text:'unknow'
		    font_name:'DroidSansFallback'
		Label:
		    text:'左下舵机'
		    font_name:'DroidSansFallback'
		Switch:
	        id:leftdownduoji
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:leftdownduojistate
	        text:'unknow'
		    font_name:'DroidSansFallback'
		Label:
		    text:'右上舵机'
		    font_name:'DroidSansFallback'
		Switch:
	        id:rightupduoji
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:rightupduojistate
	        text:'unknow'
		    font_name:'DroidSansFallback'
		Label:
		    text:'右下舵机'
		    font_name:'DroidSansFallback'
		Switch:
	        id:rightdownduoji
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:rightdownduojistate
	        text:'unknow'
		    font_name:'DroidSansFallback'
		Label:
			text:'上盒锁'
			font_name:'DroidSansFallback'
		ToggleButton:
	        id:upbox
	        on_release:root.upboxcontrol()
		Label:
		    text:'下盒锁'
		    font_name:'DroidSansFallback'
		ToggleButton:
	        id:downbox
	        on_release:root.downboxcontrol()
		Label:
		    text:'左上门'
		    font_name:'DroidSansFallback'
		Switch:
	        id:leftupdoor
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:leftupstate
	        text:'unknow'
		    font_name:'DroidSansFallback'
	    Label:
		    text:'右上门'
		    font_name:'DroidSansFallback'
		Switch:
	        id:rightupdoor
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:rightupstate
	        text:'unknow'
		    font_name:'DroidSansFallback'
	    Label:
		    text:'左下门'
		    font_name:'DroidSansFallback'
		Switch:
	        id:leftdowndoor
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:leftdownstate
	        text:'unknow'
		    font_name:'DroidSansFallback'
	    Label:
		    text:'右下门'
		    font_name:'DroidSansFallback'
		Switch:
	        id:rightdowndoor
	    Label:
		    text:'状态'
		    font_name:'DroidSansFallback'
		Label:
	        id:rightdownstate
	        text:'unknow'
		    font_name:'DroidSansFallback'
		Label:
		    text:'上门'
		    font_name:'DroidSansFallback'
		ToggleButton:
	        id:updoor
	        on_release:root.updoorcontrol()
		Label:
		    text:'下门'
		    font_name:'DroidSansFallback'
		ToggleButton:
	        id:downdoor
            on_release:root.downdoorcontrol()
	    Label:
			text:'左上灯'
			font_name:'DroidSansFallback'
		Switch:
	        id:leftuplight
		Label:
		    text:'左下灯'
		    font_name:'DroidSansFallback'
		Switch:
	        id:leftdownlight
		Label:
		    text:'右上灯'
		    font_name:'DroidSansFallback'
		Switch:
	        id:rightuplight
		Label:
		    text:'右下灯'
		    font_name:'DroidSansFallback'
		Switch:
	        id:rightdownlight

	    Label:
		    text:'左上称重'
		    font_name:'DroidSansFallback'
		Label:
		    id:leftupwei
		    text:'0'
		Label:
		    text:'右上称重'
		    font_name:'DroidSansFallback'
		Label:
		    id:rightupwei
		    text:'0'
		Label:
		    text:'左下称重'
		    font_name:'DroidSansFallback'
		Label:
		    id:leftdownwei
		    text:'0'
		Label:
		    text:'右下称重'
		    font_name:'DroidSansFallback'
		Label:
		    id:rightdownwei
		    text:'0'
		Label:
		    text:'上盒重量'
		    font_name:'DroidSansFallback'
		Label:
		    id:upboxwei
		    text:'0'
		Label:
		    text:'下盒重量'
		    font_name:'DroidSansFallback'
		Label:
		    id:downboxwei
		    text:'0'

	    ToggleButton:
	        id:start
	        text:'控制'
	        font_name:'DroidSansFallback'
	        on_release:root.subany()

        Button:
            id:return
            text:"返回"
            font_name:'DroidSansFallback'
            on_press:root.manager.current="main"
            #on_press:root.stop()

        ToggleButton:
	        id:dmonitor
	        text:'监控'
	        font_name:'DroidSansFallback'
	        on_release:root.doormonitor()

<ThrScreen>
    GridLayout:
        cols:4
		Label:
		    text:'红外1'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf1state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外2'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf2state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外3'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf3state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外4'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf4state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外5'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf5state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外6'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf6state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外7'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf7state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外8'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf8state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外9'
		    font_name:'DroidSansFallback'
		Label:
		    id:inf9state
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'红外10'
		    font_name:'DroidSansFallback'
		Label:
		    id:infastate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'IMU'
		    font_name:'DroidSansFallback'
		Label:
		    id:imustate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'C板'
		    font_name:'DroidSansFallback'
		Label:
		    id:cboardstate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'左上门'
		    font_name:'DroidSansFallback'
		Label:
		    id:leftupstate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'左下门'
		    font_name:'DroidSansFallback'
		Label:
		    id:leftdownstate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'右上门'
		    font_name:'DroidSansFallback'
		Label:
		    id:rightupstate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'右下门'
		    font_name:'DroidSansFallback'
		Label:
		    id:rightdownstate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'左箱体'
		    font_name:'DroidSansFallback'
		Label:
		    id:leftduojistate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'右箱体'
		    font_name:'DroidSansFallback'
		Label:
		    id:rightduojistate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'左电机'
		    font_name:'DroidSansFallback'
		Label:
		    id:leftmotorstate
		    font_name:'DroidSansFallback'
			text:'unknow'
		Label:
		    text:'右电机'
		    font_name:'DroidSansFallback'
		Label:
		    id:rightmotorstate
		    font_name:'DroidSansFallback'
			text:'unknow'

		ToggleButton:
	        id:select
	        text:'查询'
	        font_name:'DroidSansFallback'
	        on_release:root.subany()
        Button:
            id:return
            text:"返回"
            font_name:'DroidSansFallback'
            on_press:root.manager.current="main"
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
            Label:
                id:threadnum
                text:'0'
''')

class OneScreen(Screen):

    def __init__(self, **kwargs):
        super(OneScreen, self).__init__(**kwargs)
        
    def mainany(self):
        if self.ids['ControlStart'].state=='down':
            self.ids['duoji'].disabled=True
            self.ids['udsfind'].disabled=True
            self.ids['MonitorControl'].disabled=True
        else:
            self.ids['duoji'].disabled=False
            self.ids['udsfind'].disabled=False
            self.ids['MonitorControl'].disabled=False
        t= threading.Thread(target=self.start)
        t.setDaemon(True)
        t.start()

    def monitor(self):
        if self.ids['MonitorControl'].state=='down':
            self.ids['duoji'].disabled=True
            self.ids['udsfind'].disabled=True
            self.ids['ControlStart'].disabled=True
        else:
            self.ids['duoji'].disabled=False
            self.ids['udsfind'].disabled=False
            self.ids['ControlStart'].disabled=False
        t= threading.Thread(target=self.monitorstart)
        t.setDaemon(True)
        t.start()

    def start(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['ControlStart'].state=='normal':
                break
            else:
                data=self.tock()
                #print(data)
                udpclient.sendto(data.decode('hex'),('192.168.80.201',6650))
                try:
                    mess=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag==1:
                    result=mess.encode('hex')
                    self.motorany(result)
                    self.infany(result)
                    self.ultrany(result)
                    self.imuany(result)
                    self.inchany(result[14:16])
                    self.batany(result[82:86])
                    self.fallany(result[74:76])
                    self.motorableany(result[16:18])
                    self.switchany(result[80:82])
        udpclient.close()

    def monitorstart(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['MonitorControl'].state=='normal':
                break
            else:
                udpclient.sendto('hello',('192.168.80.201',6650))
                try:
                    mess=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag==1:
                    result=mess.encode('hex')
                    self.motorany(result)
                    self.infany(result)
                    self.ultrany(result)
                    self.imuany(result)
                    self.inchany(result[14:16])
                    self.batany(result[82:86])
                    self.fallany(result[74:76])
                    self.motorableany(result[16:18])
                    self.switchany(result[80:82])
        udpclient.close()

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

    def infany(self,result):
        inf1=int(result[102:104],16)
        inf2=int(result[104:106],16)
        inf3=int(result[106:108],16)
        inf4=int(result[108:110],16)
        inf5=int(result[110:112],16)
        inf6=int(result[112:114],16)
        inf7=int(result[114:116],16)
        inf8=int(result[116:118],16)
        inf9=int(result[118:120],16)
        infa=int(result[120:122],16)
        self.ids['inf1value'].text=str(inf1)
        self.ids['inf2value'].text=str(inf2)
        self.ids['inf3value'].text=str(inf3)
        self.ids['inf4value'].text=str(inf4)
        self.ids['inf5value'].text=str(inf5)
        self.ids['inf6value'].text=str(inf6)
        self.ids['inf7value'].text=str(inf7)
        self.ids['inf8value'].text=str(inf8)
        self.ids['inf9value'].text=str(inf9)
        self.ids['infavalue'].text=str(infa)

    def ultrany(self,result):
        ul1=int(result[90:92],16)
        ul2=int(result[92:94],16)
        ul3=int(result[94:96],16)
        ul4=int(result[96:98],16)
        ul5=int(result[98:100],16)
        ul6=int(result[100:102],16)
        self.ids['ult1value'].text=str(ul1)
        self.ids['ult2value'].text=str(ul2)
        self.ids['ult3value'].text=str(ul3)
        self.ids['ult4value'].text=str(ul4)
        self.ids['ult5value'].text=str(ul5)
        self.ids['ult6value'].text=str(ul6)

    def imuany(self,result):
        pithhex=result[64]+result[65]+result[62]+result[63]
        tempith=int(pithhex,16)
        if tempith>=32768:
            pith='-'+str(float((65536-tempith)*0.01))
        else:
            pith=float(tempith*0.01)
        yawhex=result[68]+result[69]+result[66]+result[67]
        tempyaw=int(yawhex,16)
        if tempyaw>=32768:
            yaw='-'+str(float((65536-tempyaw)*0.01))
        else:
            yaw=float(tempyaw*0.01)
        rollhex=result[72]+result[73]+result[70]+result[71]
        temproll=int(rollhex,16)
        if temproll>=32768:
            roll='-'+str(float((65536-temproll)*0.01))
        else:
            roll=float(temproll*0.01)
        self.ids['Pithvalue'].text=str(pith)
        self.ids['rollvalue'].text=str(roll)
        self.ids['Yawvalue'].text=str(yaw)

    def inchany(self,data):
        pithcode=int(data,16)
        if pithcode==1:
            self.ids['pith'].text=u'右侧'
        elif pithcode==2:
            self.ids['pith'].text=u'中间'
        elif pithcode==3:
            self.ids['pith'].text=u'右，中'
        elif pithcode==4:
            self.ids['pith'].text=u'左侧'
        elif pithcode==5:
            self.ids['pith'].text=u'左，右侧'
        elif pithcode==6:
            self.ids['pith'].text=u'左，中'
        elif pithcode==7:
            self.ids['pith'].text=u'左中右'
        else:
            self.ids['pith'].text=u'正常'

    def batany(self,data):
        batstat=data[0:2]
        batvol=data[2:4]
        if batstat=='00':
            self.ids['batstat'].text=u'未知状态'
        elif batstat=='01':
            self.ids['batstat'].text=u'正常放电'
        elif batstat=='02':
            self.ids['batstat'].text=u'正在充电'
        elif batstat=='03':
            self.ids['batstat'].text=u'充满电'
        elif batstat=='ff':
            self.ids['batstat'].text=u'异常状态'
        else:
            self.ids['batstat'].text=u'非法值'+batstat
        batvalue=int(batvol,16)
        self.ids['batvalue'].text=str(batvalue)

    def motorableany(self,data):
        if data=='00':
            self.ids['motorstat'].text=u'释放'
        else:
            self.ids['motorstat'].text=u'使能'

    def switchany(self,data):
        temp=int(data,16)
        if temp&64==64:
            self.ids['switchup'].text=u'到位'
        else:
            self.ids['switchup'].text=u'未到位'
        if temp&128==128:
            self.ids['switchdown'].text=u'到位'
        else:
            self.ids['switchdown'].text=u'未到位'

    def fallany(self,data):
        if data=='00' or data=='01':
            self.ids['fallstat'].text=u'正常'
        elif data=='02':
            self.ids['fallstat'].text=u'异常'
        elif data=='04':
            self.ids['fallstat'].text=u'失重'
        else:
            self.ids['fallstat'].text=u'电梯'

    def tock(self):
        motorvol='00000000'
        if self.ids['front'].state=='down':
            targetspeed=int(self.ids['speed'].text)
            hexspeed=hex(targetspeed).lstrip('0x')
            for i in range(0,4-len(hexspeed)):
                hexspeed='0'+hexspeed
            motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if self.ids['back'].state=='down':
            if self.ids['speed'].text=='0':
                motorvol='00000000'
            else:
                targetspeed=65536-int(self.ids['speed'].text)
                hexspeed=hex(targetspeed).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if self.ids['turnleft'].state=='down':
                targetspeed=int(self.ids['speed'].text)
                hexspeed=hex(targetspeed).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                motorvol='0000'+hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]
        else:
            pass
        if self.ids['turnright'].state=='down':
                targetspeed=int(self.ids['speed'].text)
                hexspeed=hex(targetspeed).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+'0000'
        else:
            pass
        if self.ids['turnrun'].state=='down':
            if self.ids['speed'].text=='0':
                motorvol='00000000'
            else:
                targetspeed=65536-int(self.ids['speed'].text)
                hexspeed=hex(targetspeed).lstrip('0x')
                for i in range(0,4-len(hexspeed)):
                    hexspeed='0'+hexspeed
                rightspeed=int(self.ids['speed'].text)
                hexright=hex(rightspeed).lstrip('0x')
                for i in range(0,4-len(hexright)):
                    hexright='0'+hexright
                motorvol=hexspeed[2]+hexspeed[3]+hexspeed[0]+hexspeed[1]+hexright[2]+hexright[3]+hexright[0]+hexright[1]
        else:
            pass
        if self.ids['motorenable'].state=='down':
            motorcmd='00'
        else:
            motorcmd='11'
        mess='59'+'ee'+'ee'+'11'+'10'+motorvol+motorcmd+'0000'+'000F00'+'000000000000'+'00'
        CRCHi,CRCLo=self.calc(mess.decode('hex'))
        if len(CRCHi)==0:
            CRCHi='00'
        if len(CRCHi)==1:
            CRCHi='0'+CRCHi

        if len(CRCLo)==0:
            CRCLo='00'
        if len(CRCLo)==1:
            CRCLo='0'+CRCLo

        tockmess=mess+CRCLo+CRCHi+'47'
        return tockmess

    def ActionFront(self):
        self.ids['back'].state='normal'
        self.ids['turnleft'].state='normal'
        self.ids['turnright'].state='normal'
        self.ids['turnrun'].state='normal'

    def ActionBack(self):
        self.ids['front'].state='normal'
        self.ids['turnleft'].state='normal'
        self.ids['turnright'].state='normal'
        self.ids['turnrun'].state='normal'

    def Actionleft(self):
        self.ids['back'].state='normal'
        self.ids['front'].state='normal'
        self.ids['turnright'].state='normal'
        self.ids['turnrun'].state='normal'

    def Actionright(self):
        self.ids['back'].state='normal'
        self.ids['front'].state='normal'
        self.ids['turnleft'].state='normal'
        self.ids['turnrun'].state='normal'

    def Actionturn(self):
        self.ids['back'].state='normal'
        self.ids['front'].state='normal'
        self.ids['turnleft'].state='normal'
        self.ids['turnright'].state='normal'

    def MaxSpeed(self):
        currentspeed=self.ids['speed'].text
        tarspeed=int(currentspeed)+10
        self.ids['speed'].text=str(tarspeed)

    def MinSpeed(self):
        currentspeed=self.ids['speed'].text
        if currentspeed=='0':
            pass
        else:
            tarspeed=int(currentspeed)-10
            self.ids['speed'].text=str(tarspeed)

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

class TwoScreen(Screen):

    def __init__(self, **kwargs):
        super(TwoScreen, self).__init__(**kwargs)

    def subany(self):
        if self.ids['start'].state=='down':
            self.ids['return'].disabled=True
            self.ids['dmonitor'].disabled=True
            self.ids['leftupduoji'].active=True
            self.ids['rightupduoji'].active=True
            self.ids['leftdownduoji'].active=True
            self.ids['rightdownduoji'].active=True
        else:
            self.ids['return'].disabled=False
            self.ids['dmonitor'].disabled=False
        t= threading.Thread(target=self.start)
        t.setDaemon(True)
        t.start()

    def doormonitor(self):
        if self.ids['dmonitor'].state=='down':
            self.ids['return'].disabled=True
            self.ids['start'].disabled=True
        else:
            self.ids['start'].disabled=False
            self.ids['return'].disabled=False
        t= threading.Thread(target=self.nonStart)
        t.setDaemon(True)
        t.start()

    def nonStart(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['dmonitor'].state=='down':
                udpclient.sendto('hello',('192.168.80.201',6650))
                try:
                    recv=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag:
                    result=recv.encode('hex')
                    self.weiany(result)
                    self.duojiany(result[80:82])
                    self.doorany(result[78:80])
            else:
                break
        udpclient.close()

    def upboxcontrol(self):
        if self.ids['upbox'].state=='down':
            self.ids['leftupduoji'].active=True
            self.ids['rightupduoji'].active=True
        else:
            self.ids['leftupduoji'].active=False
            self.ids['rightupduoji'].active=False

    def downboxcontrol(self):
        if self.ids['downbox'].state=='down':
            self.ids['leftdownduoji'].active=True
            self.ids['rightdownduoji'].active=True
        else:
            self.ids['leftdownduoji'].active=False
            self.ids['rightdownduoji'].active=False

    def updoorcontrol(self):
        if self.ids['updoor'].state=='down':
            self.ids['leftupdoor'].active=True
            self.ids['rightupdoor'].active=True
        else:
            self.ids['leftupdoor'].active=False
            self.ids['rightupdoor'].active=False

    def downdoorcontrol(self):
        if self.ids['downdoor'].state=='down':
            self.ids['leftdowndoor'].active=True
            self.ids['rightdowndoor'].active=True
        else:
            self.ids['leftdowndoor'].active=False
            self.ids['rightdowndoor'].active=False

    def start(self):
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['start'].state=='down':
                data=self.tock()
                #print(data)
                udpclient.sendto(data.decode('hex'),('192.168.80.201',6650))
                try:
                    recv=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag:
                    result=recv.encode('hex')
                    self.weiany(result)
                    self.duojiany(result[80:82])
                    self.doorany(result[78:80])
            else:
                break
        udpclient.close()

    def tock(self):
        motorcmd='00000000'
        carbinedoor=0
        carbinlock=0
        lightcmd=0
        if self.ids['leftupduoji'].active:
            carbinlock=carbinlock | 1
        if self.ids['leftdownduoji'].active:
            carbinlock=carbinlock | 4
        if self.ids['rightupduoji'].active:
            carbinlock=carbinlock | 2
        if self.ids['rightdownduoji'].active:
            carbinlock=carbinlock | 8

        if carbinlock==0:
            hexlock='00'
        else:
            hexlock=hex(carbinlock).lstrip('0x')
            if len(hexlock)==1:
                hexlock='0'+hexlock

        if self.ids['leftupdoor'].active:
            carbinedoor=carbinedoor | 1
        if self.ids['leftdowndoor'].active:
            carbinedoor=carbinedoor | 4
        if self.ids['rightupdoor'].active:
            carbinedoor=carbinedoor | 2
        if self.ids['rightdowndoor'].active:
            carbinedoor=carbinedoor | 8

        if carbinedoor==0:
            hexdoor='00'
        else:
            hexdoor=hex(carbinedoor).lstrip('0x')
            if len(hexdoor)==1:
                hexdoor='0'+hexdoor

        if self.ids['leftuplight'].active:
            lightcmd=lightcmd | 1
        if self.ids['leftdownlight'].active:
            lightcmd=lightcmd | 4
        if self.ids['rightuplight'].active:
            lightcmd=lightcmd | 2
        if self.ids['rightdownlight'].active:
            lightcmd=lightcmd | 8

        if lightcmd==0:
            hexlight='00'
        else:
            hexlight=hex(lightcmd).lstrip('0x')
            if len(hexlight)==1:
                hexlight='0'+hexlight
        mess='59'+'ee'+'ee'+'11'+'10'+motorcmd+'110000'+hexdoor+hexlock+hexlight+'000000000000'+'00'
        CRCHi,CRCLo=self.calc(mess.decode('hex'))
        if len(CRCHi)==0:
            CRCHi='00'
        if len(CRCHi)==1:
            CRCHi='0'+CRCHi

        if len(CRCLo)==0:
            CRCLo='00'
        if len(CRCLo)==1:
            CRCLo='0'+CRCLo

        tockmess=mess+CRCLo+CRCHi+'47'
        return tockmess

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

    def duojiany(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp&1==1:
            leftup=u'锁定'
        else:
            leftup=u'未锁'
        if temp&4==4:
            leftdown=u'锁定'
        else:
            leftdown=u'未锁'
        if temp&2==2:
            rightup=u'锁定'
        else:
            rightup=u'未锁'
        if temp&8==8:
            rightdown=u'锁定'
        else:
            rightdown=u'未锁'

        self.ids['leftupduojistate'].text=leftup
        self.ids['leftdownduojistate'].text=leftdown
        self.ids['rightupduojistate'].text=rightup
        self.ids['rightdownduojistate'].text=rightdown

    def doorany(self,data):
        try:
            temp=int(data,16)
        except:
            temp=0
        if temp==0:
            leftup=u'打开'
            leftdown=u'打开'
            rightup=u'打开'
            rightdown=u'打开'
        else:
            if temp&1==1:
                rightup=u'中间'
            if temp&2==2:
                rightup=u'关闭'
            if temp&1!=1 and temp&2!=2:
                rightup=u'打开'

            if temp&4==4:
                leftup=u'中间'
            if temp&8==8:
                leftup=u'关闭'
            if temp&4!=4 and temp&8!=8:
                leftup=u'打开'

            if temp&16==16:
                rightdown=u'中间'
            if temp&32==32:
                rightdown=u'关闭'
            if temp&16!=16 and temp&32!=32:
                rightdown=u'打开'

            if temp&64==64:
                leftdown=u'中间'
            if temp&128==128:
                leftdown=u'关闭'
            if temp&64!=64 and temp&128!=128:
                leftdown=u'打开'

        self.ids['leftupstate'].text=leftup
        self.ids['leftdownstate'].text=leftdown
        self.ids['rightupstate'].text=rightup
        self.ids['rightdownstate'].text=rightdown

    def weiany(self,frame):
        temp1=int((frame[132]+frame[133]+frame[130]+frame[131]),16)
        temp2=int((frame[136]+frame[137]+frame[134]+frame[135]),16)
        temp3=int((frame[140]+frame[141]+frame[138]+frame[139]),16)
        temp4=int((frame[144]+frame[145]+frame[142]+frame[143]),16)
        if temp1>32767:
            tempdata=65536-temp1
            leftup='-'+str(tempdata)
        else:
            leftup=str(temp1)

        if temp2>32767:
            tempdata=65536-temp2
            rightup='-'+str(tempdata)
        else:
            rightup=str(temp2)

        if temp1>32767 and temp2>32767:
            totaltemp=(65536-temp1)+(65536-temp2)
            uptotal='-'+str(totaltemp)
        elif temp1>32767 and temp2<32767:
            if (65536-temp1)>temp2:
                totaltemp=65536-temp1-temp2
                uptotal='-'+str(totaltemp)
            else:
                totaltemp=temp2-(65536-temp1)
                uptotal=str(totaltemp)
        elif temp1<32767 and temp2>32767:
            if (65536-temp2)>temp1:
                totaltemp=(65536-temp2)-temp1
                uptotal='-'+str(totaltemp)
            else:
                totaltemp=temp1-(65536-temp2)
                uptotal=str(totaltemp)
        else:
            totaltemp=temp1+temp2
            uptotal=str(totaltemp)

        if temp3>32767:
            tempdata=65536-temp3
            leftdown='-'+str(tempdata)
        else:
            leftdown=str(temp3)

        if temp4>32767:
            tempdata=65536-temp4
            rightdown='-'+str(tempdata)
        else:
            rightdown=str(temp4)

        if temp3>32767 and temp4>32767:
            totaltemp=(65536-temp3)+(65536-temp4)
            downtotal='-'+str(totaltemp)
        elif temp3>32767 and temp4<32767:
            if (65536-temp3)>temp4:
                totaltemp=65536-temp3-temp4
                downtotal='-'+str(totaltemp)
            else:
                totaltemp=temp4-(65536-temp3)
                downtotal=str(totaltemp)
        elif temp3<32767 and temp4>32767:
            if (65536-temp4)>temp3:
                totaltemp=(65536-temp4)-temp3
                downtotal='-'+str(totaltemp)
            else:
                totaltemp=temp3-(65536-temp4)
                downtotal=str(totaltemp)
        else:
            totaltemp=temp3+temp4
            downtotal=str(totaltemp)

        if uptotal[0]=='-':
            totalup=str((int(str(uptotal).lstrip('-')))*0.38)
        else:
            totalup='-'+str((int(str(uptotal).lstrip('-')))*0.38)

        if downtotal[0]=='-':
            totaldown=str((int(str(downtotal).lstrip('-')))*0.38)
        else:
            totaldown='-'+str((int(str(downtotal).lstrip('-')))*0.38)


        self.ids['leftupwei'].text=leftup
        self.ids['leftdownwei'].text=leftdown
        self.ids['rightupwei'].text=rightup
        self.ids['rightdownwei'].text=rightdown
        self.ids['upboxwei'].text=totalup+'g'
        self.ids['downboxwei'].text=totaldown+'g'

class ThrScreen(Screen):

    def __init__(self, **kwargs):
        super(ThrScreen, self).__init__(**kwargs)

    def subany(self):
        if self.ids['select'].state=='down':
            self.ids['return'].disabled=True
        else:
            self.ids['return'].disabled=False
        subt= threading.Thread(target=self.subtart)
        subt.setDaemon(True)
        subt.start()

    def subtart(self):
        bid=0
        udpclient=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpclient.settimeout(1)
        while True:
            if self.ids['select'].state=='down':
                data=self.tock(bid)
                #print(data)
                udpclient.sendto(data.decode('hex'),('192.168.80.201',6650))
                try:
                    mess=udpclient.recv(1024)
                    flag=1
                except:
                    flag=0
                if flag==1:
                    result=mess.encode('hex')
                    self.errany(result)
                bid+=1
                if bid>19:
                    bid=0
            else:
                break
        udpclient.close()


    def tock(self,flag):
        tockmessage='00000000'+'11'+'0000'+'00'+'0F'+'0F'+'000000000000'
        if flag==0:
            bid='51'
        elif flag==1:
            bid='52'
        elif flag==2:
            bid='53'
        elif flag==3:
            bid='54'
        elif flag==4:
            bid='55'
        elif flag==5:
            bid='56'
        elif flag==6:
            bid='57'
        elif flag==7:
            bid='58'
        elif flag==8:
            bid='59'
        elif flag==9:
            bid='5a'
        elif flag==10:
            bid='e1'
        elif flag==11:
            bid='ee'
        elif flag==12:
            bid='25'
        elif flag==13:
            bid='26'
        elif flag==14:
            bid='27'
        elif flag==15:
            bid='28'
        elif flag==16:
            bid='61'
        elif flag==17:
            bid='62'
        elif flag==18:
            bid='11'
        elif flag==19:
            bid='12'
        else:
            bid='ee'
        mess='59'+bid+'80'+'13'+'10'+tockmessage+'3D01'+'01'
        CRCHi,CRCLo=self.calc(mess.decode('hex'))

        if len(CRCHi)==0:
            CRCHi='00'
        if len(CRCHi)==1:
            CRCHi='0'+CRCHi

        if len(CRCLo)==0:
            CRCLo='00'
        if len(CRCLo)==1:
            CRCLo='0'+CRCLo

        tockmess=mess+CRCLo+CRCHi+'47'
        return tockmess

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

    def errany(self,result):
        bid=result[2:4]
        code=result[-10:-8]
        if bid=='ee':
            if result[6:8]=='49':
                if code=='00':
                    errcode=u'正常'
                elif code=='01':
                    errcode=u'左轮毂电机连接不上'
                elif code=='02':
                    errcode=u'右轮毂电机连接不上'
                elif code=='03':
                    errcode=u'直流电机1连接不上'
                elif code=='04':
                    errcode=u'直流电机2连接不上'
                elif code=='05':
                    errcode=u'直流电机3连接不上'
                elif code=='06':
                    errcode=u'直流电机4连接不上'
                elif code=='07':
                    errcode=u'超声波1连接不上'
                elif code=='08':
                    errcode=u'超声波2连接不上'
                elif code=='09':
                    errcode=u'超声波3连接不上'
                elif code=='0a':
                    errcode=u'超声波4连接不上'
                elif code=='0b':
                    errcode=u'超声波5连接不上'
                elif code=='0c':
                    errcode=u'超声波6连接不上'
                elif code=='0d':
                    errcode=u'左箱体板连接不上'
                elif code=='0e':
                    errcode=u'右箱体板连接不上'
                elif code=='0f':
                    errcode=u'BMS连接不上'
                elif code=='10':
                    errcode=u'IMU连接不上'
                elif code=='11':
                    errcode=u'红外1连接不上'
                elif code=='12':
                    errcode=u'红外2连接不上'
                elif code=='13':
                    errcode=u'红外3连接不上'
                elif code=='14':
                    errcode=u'红外4连接不上'
                elif code=='15':
                    errcode=u'红外5连接不上'
                elif code=='16':
                    errcode=u'红外6连接不上'
                elif code=='17':
                    errcode=u'红外7连接不上'
                elif code=='18':
                    errcode=u'红外8连接不上'
                elif code=='19':
                    errcode=u'红外9连接不上'
                elif code=='1a':
                    errcode=u'红外10连接不上'
                elif code=='1b':
                    errcode=u'ARM连接不上'
                else:
                    errcode=u'非法值'
                self.ids['cboardstate'].text=errcode
            else:
                pass
        elif bid=='11' or bid=='12':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'速度偏差故障'
            elif code=='02':
                errcode=u'霍尔故障'
            elif code=='04':
                errcode=u'编码器故障'
            elif code=='08':
                errcode=u'静态电流故障'
            elif code=='10':
                errcode=u'欠压故障'
            elif code=='20':
                errcode=u'过压故障'
            elif code=='40':
                errcode=u'堵转故障'
            elif code=='80':
                errcode=u'上下桥故障'
            else:
                errcode=u'非法值'+code
            if bid=='11':
                self.ids['leftmotorstate'].text=errcode
            else:
                self.ids['rightmotorstate'].text=errcode
        elif bid=='61' or bid=='62':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'上盒子舵机关不到位'
            elif code=='02':
                errcode=u'下盒子舵机关不到位'
            elif code=='03':
                errcode=u'上盒子舵机开不到位'
            elif code=='04':
                errcode=u'下盒子舵机开不到位'
            elif code=='05':
                errcode=u'上盒子称重数值异常'
            elif code=='06':
                errcode=u'下盒子称重数值异常'
            elif code=='07':
                errcode=u'上盒子开门电机过流'
            elif code=='08':
                errcode=u'下盒子开门电机过流'
            elif code=='09':
                errcode=u'上盒子开门电机堵转'
            elif code=='0a':
                errcode=u'下盒子开门电机堵转'
            elif code=='0b':
                errcode=u'上盒子开门电机门开不到位'
            elif code=='0c':
                errcode=u'下盒子开门电机门开不到位'
            elif code=='0d':
                errcode=u'上盒子开门电机门关不到位'
            elif code=='0e':
                errcode=u'下盒子开门电机门关不到位'
            elif code=='0f':
                errcode=u'上盒子电机供电欠压'
            elif code=='10':
                errcode=u'下盒子电机供电欠压'
            elif code=='11':
                errcode=u'上盒子电机供电过压'
            elif code=='12':
                errcode=u'下盒子电机供电过压'
            elif code=='13':
                errcode=u'上盒子电机失位置'
            elif code=='14':
                errcode=u'下盒子电机失位置'
            else:
                errcode=u'非法值'
            if bid=='61':
                self.ids['leftduojistate'].text=errcode
            else:
                self.ids['rightduojistate'].text=errcode
        elif bid=='51' or bid=='52' or bid=='53' or bid=='54' or bid=='55' or bid=='56' or bid=='57' or bid=='58' or bid=='59' or bid=='5a':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'红外传感器异常'
            else:
                errcode=u'非法值'
            if bid=='51':
                self.ids['inf1state'].text=errcode
            elif bid=='52':
                self.ids['inf2state'].text=errcode
            elif bid=='53':
                self.ids['inf3state'].text=errcode
            elif bid=='54':
                self.ids['inf4state'].text=errcode
            elif bid=='55':
                self.ids['inf5state'].text=errcode
            elif bid=='56':
                self.ids['inf6state'].text=errcode
            elif bid=='57':
                self.ids['inf7state'].text=errcode
            elif bid=='58':
                self.ids['inf8state'].text=errcode
            elif bid=='59':
                self.ids['inf9state'].text=errcode
            else:
                self.ids['infastate'].text=errcode

        elif bid=='25' or bid=='27' or bid=='26' or bid=='28':
            if code=='00':
                errcode=u'无故障'
            elif code=='01':
                errcode=u'程序初始化错误'
            elif code=='02':
                errcode=u'电机停止错误'
            elif code=='03':
                errcode=u'电机启动错误'
            elif code=='04':
                errcode=u'PWM波丢失'
            elif code=='05':
                errcode=u'PWM脉冲过宽'
            elif code=='06':
                errcode=u'PWM脉冲过窄'
            elif code=='07':
                errcode=u'电机A相开路'
            elif code=='08':
                errcode=u'电机B相开路'
            elif code=='09':
                errcode=u'电机C相开路'
            elif code=='0a':
                errcode=u'电机A相与GND短路'
            elif code=='0b':
                errcode=u'电机B相与GND短路'
            elif code=='0c':
                errcode=u'电机C相与GND短路'
            elif code=='0d':
                errcode=u'电机A相与电池正极短路'
            elif code=='0e':
                errcode=u'电机B相与电池正极短路'
            elif code=='0f':
                errcode=u'电机C相与电池正极短路'
            elif code=='10':
                errcode=u'电机A相过流'
            elif code=='11':
                errcode=u'电机B相过流'
            elif code=='12':
                errcode=u'电机C相过流'
            elif code=='13':
                errcode=u'硬件错误'
            elif code=='14':
                errcode=u'硬件错误'
            elif code=='15':
                errcode=u'硬件错误'
            elif code=='16':
                errcode=u'硬件错误'
            elif code=='17':
                errcode=u'硬件错误'
            elif code=='18':
                errcode=u'硬件错误'
            elif code=='19':
                errcode=u'硬件错误'
            elif code=='1a':
                errcode=u'硬件错误'
            elif code=='1b':
                errcode=u'电池电压过低'
            elif code=='1c':
                errcode=u'电池电压过高'
            elif code=='1d':
                errcode=u'电机1关门位置严重错误'
            elif code=='1e':
                errcode=u'电机1关门角度太小'
            elif code=='1f':
                errcode=u'电机1关门角度太大'
            elif code=='20':
                errcode=u'电机2关门位置严重错误'
            elif code=='21':
                errcode=u'电机2关门角度太小'
            elif code=='22':
                errcode=u'电机2关门角度太大'
            else:
                errcode=u'非法值'+code

            if bid=='25':
                self.ids['leftupstate'].text=errcode
            elif bid=='26':
                self.ids['leftdownstate'].text=errcode
            elif bid=='27':
                self.ids['rightupstate'].text=errcode
            else:
                self.ids['rightdownstate'].text=errcode

        elif bid=='e1':
            if code=='00':
                errcode=u'正常'
            elif code=='01':
                errcode=u'无法获取数据'
            else:
                errcode=u'非法值'
            self.ids['imustate'].text=errcode
        else:
            pass

class FourScreen(Screen):

    def __init__(self, **kwargs):
        super(FourScreen, self).__init__(**kwargs)

        cb = CustomBtn()
        cb.bind(pressed=self.btn_pressed)

        cu = CustomUnBtn()
        cu.bind(pressed=self.btn_unpressed)

        self.add_widget(cb)
        self.add_widget(cu)

    def btn_pressed(self, instance, pos):
        thnum=int(self.ids['threadnum'].text)
        postion=str(int(pos[0]))+','+str(int(pos[1]))
        if int(pos[0])<=390 and int(pos[0]) >=220 and int(pos[1])>=165 and int(pos[1]) <=280:
            self.speedadd()
        elif int(pos[0])<=580 and int(pos[0]) >=390 and int(pos[1])>=165 and int(pos[1]) <=280:
            self.speedsub()
        elif int(pos[0])<=596 and int(pos[0]) >=196 and int(pos[1])>=710 and int(pos[1]) <=1110:
            self.ids['postion'].text=postion
            self.ids['controlstat'].text='开始'
            if thnum==0:
                t= threading.Thread(target=self.start)
                t.setDaemon(True)
                t.start()
            else:
                pass
        else:
            pass

    def btn_unpressed(self, instance, pos):
        self.ids['threadnum'].text='0'
        self.ids['controlstat'].text='停止'

    def start(self):
        thnum=int(self.ids['threadnum'].text)
        temp=thnum+1
        self.ids['threadnum'].text=str(temp)
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
                break
        udpclient.close()

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
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            # we consumed the touch. return False here to propagate
            # the touch further to the children.
            return True
        return super(CustomBtn, self).on_touch_down(touch)

    def on_touch_move(self, touch):
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
        sm = ScreenManager()
        scm = OneScreen(name="main")
        scs = TwoScreen(name="sub")
        sct = ThrScreen(name="UDS")
        scf = FourScreen(name="Motor")
        sm.add_widget(scm)
        sm.add_widget(scs)
        sm.add_widget(sct)
        sm.add_widget(scf)
        return sm

YopkApp().run()