# -*- coding: utf-8 -*-
import time
import os
import cv2
import numpy as np
import sys
def pull_screenshot():
	os.system('adb  -s 192.168.43.1:5555 exec-out screencap -p > scr.png')
def click_loc(x,y):
	os.system('adb  -s 192.168.43.1:5555 shell input swipe '+ \
			  str(x)+' '+str(y)+' '+ \
			  str(x)+' '+str(y)+' '+ \
			  '20')
def cvtCL(img):
	im=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	im=im & 0xc0#(np.round(im/8)*8).astype(np.uint8)
	return im
def timesleep(sec):
	cv2.waitKey(int(sec*1000))
	
def find_loc(screen,template):#灰度图的比较
	'''
	返回查找到的位置x，y和最小匹配的值（如果是0表示完美匹配）
	'''
	result = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	return min_loc[0]+template.shape[1]/2,min_loc[1]+template.shape[0]/2,abs(min_val)/template.shape[1]/template.shape[0]*100


def startup():
	#按照优先级
	file_list=[
	"menu",
	"sel_OK","sel_OK_2",#这个因为有重叠
	"sel_game","sel_game_2",
	"sel_char_mem_bonus","sel_char_bonus",
	"start","start_2",
	"exp_get","exp_get_2",
	"item_get","item_get_2",
	"skip","skip_2",
	"110",
	"AP","AP_OK",
	"LVup","LVup_2"]
	
	#后面跟着该操作后的等待时间
	file_dict={
	#正在对战中
	"menu":{'delay':2,'x':1,'y':1},
	#选择活动剧情的关卡
	"sel_game":{'delay':1,'x':307,'y':193},"sel_game_2":{'delay':1,'x':307,'y':193},
	
	#之后还要点一下确定
	"sel_OK":{'delay':5,'x':0,'y':0},"sel_OK_2":{'delay':5,'x':1061,'y':549},
	
	#这才进入助战，优先级：特殊记忆bonus>bonus
	"sel_char_mem_bonus":{'delay':4,'x':0,'y':0},"sel_char_bonus":{'delay':4,'x':0,'y':0},
	
	#选好后进入编队界面，点开始
	"start":{'delay':40,'x':0,'y':0},"start_2":{'delay':40,'x':0,'y':0},
	
	#结束一场之后，进入exp界面
	"exp_get":{'delay':1,'x':0,'y':0},"exp_get_2":{'delay':1,'x':0,'y':0},
	
	#之后第二屏为掉落统计
	"item_get":{'delay':5,'x':0,'y':0},"item_get_2":{'delay':5,'x':0,'y':0},
	
	#跳过剧情
	"skip":{'delay':5,'x':0,'y':0},"skip_2":{'delay':5,'x':1218,'y':38},
	
	#110
	"110":{'delay':1,'x':0,'y':0},
	
	#AP回复第一屏
	"AP":{'delay':3,'x':0,'y':0},
	
	#AP回复第二屏
	"AP_OK":{'delay':3,'x':0,'y':0},
	
	#LVUP
	"LVup":{'delay':3,'x':0,'y':0},"LVup_2":{'delay':3,'x':0,'y':0}
	}
	
	img_dict={}
	for i in file_list:
		print('loading '+i)
		img_dict[i]=cvtCL(cv2.imread(i+".png"))
	'''
	正片开始
	'''
	#统计
	has=0
	#延时
	ts=1
	dif=1000#门限值，从截屏中找到的子图与前面png里的子图的差异程度
	time_start=time.time()
	cv2.namedWindow('scr')
	while(1):
		pull_screenshot()
		screen=cv2.imread("scr.png")
		
		scr0=cv2.resize(screen,(0,0),fx=0.4,fy=0.4)
		cv2.imshow("scr",scr0)
		
		scr=cvtCL(screen)
		
		for i in file_list:
			x,y,res=find_loc(scr,img_dict[i])
			print("匹配"+i+','+str(res))
			if res<dif:
				if file_dict[i]['x']>0:
					x=file_dict[i]['x']
					y=file_dict[i]['y']
				click_loc(x,y)
				print('成功，点击'+str(x)+','+str(y)+':等待'+str(file_dict[i]['delay']))
				if i=='exp_get' or i=='exp_get_2':
					has=has+1
					time_end=time.time()
					print('本次：'+str(time_end-time_start))
					time_start=time_end
				timesleep(file_dict[i]['delay'])
				ts=0.2
				break
		timesleep(ts)
		ts=min(5,ts+0.2)
if __name__ == "__main__":
	startup()
"""
@需要的环境：adb，四个场景要检测的五张png图片（可以从游戏界面截下来），手机打开开发者模式和USB调试

import time
import os
import cv2
import numpy as np
import sys
import json
ix=0
iy=0

def imgrayresize(img):
	im=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	im=im & 0xc0#(np.round(im/8)*8).astype(np.uint8)
	im=cv2.resize(im,(0,0),fx=0.4,fy=0.4)
	return im
def click0(event,x,y,flags,param):
	global ix, iy
	if event==cv2.EVENT_LBUTTONDOWN:
		ix, iy = x, y
		print("point:=", x, y)
		#click_loc(x,y)
	elif event==cv2.EVENT_LBUTTONUP:
		print("point2:=", x, y)
		print("width=",x-ix)
		print("height=", y - iy)
		ix*=2.5
		iy*=2.5
		x*=2.5
		y*=2.5
		cv2.rectangle(param, (ix, iy), (x, y), (0, 255, 0), 2)
		cv2.imshow("scr",param)
		
		im=param[int(iy):int(y),int(ix):int(x),:]
		name=sys.stdin.readline().strip("\n")
		cv2.imwrite(name+'.png',im)
def getlist(json_file):
	f=open(json_file,'r')
	json0=f.read()
	return json.loads(json0)
def putlist(json_file,dict0):
	f=open(json_file,'w')
	f.write(json.dumps(dict0))



"""
