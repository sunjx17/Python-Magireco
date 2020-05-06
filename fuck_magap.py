# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 20:35:26 2020

@author: a
"""

# -*- coding: utf-8 -*-
"""
@需要的环境：adb，四个场景要检测的五张png图片（可以从游戏界面截下来），手机打开开发者模式和USB调试

@author: a
"""
import time
import os
import cv2
def pull_screenshot():
	os.system('adb shell screencap -p /sdcard/scr.png ')
	os.system('adb pull /sdcard/scr.png .')
def click_loc(x,y):
	os.system('adb shell input swipe '+ \
			  str(x)+' '+str(y)+' '+ \
			  str(x)+' '+str(y)+' '+ \
			  '20')

exp_get = cv2.cvtColor(cv2.imread('exp_get.png'),cv2.COLOR_BGR2GRAY)
exp_get_size = exp_get.shape[:2]
exp_get_2 = cv2.cvtColor(cv2.imread('exp_get_2.png'),cv2.COLOR_BGR2GRAY)
exp_get_2_size = exp_get_2.shape[:2]


item_get = cv2.cvtColor(cv2.imread('item_get.png'),cv2.COLOR_BGR2GRAY)
item_get_size = item_get.shape[:2]
item_get_2 = cv2.cvtColor(cv2.imread('item_get_2.png'),cv2.COLOR_BGR2GRAY)
item_get_2_size = item_get_2.shape[:2]
#1107 644

s110 = cv2.cvtColor(cv2.imread('110.png'),cv2.COLOR_BGR2GRAY)
s110_size = s110.shape[:2]
#460 500

select_characters = cv2.cvtColor(cv2.imread('sel_char_bonus.png'),cv2.COLOR_BGR2GRAY)
select_characters_size = select_characters.shape[:2]
p60 = cv2.cvtColor(cv2.imread('plus60.png'),cv2.COLOR_BGR2GRAY)
p60_size = p60.shape[:2]
select_characters_mem = cv2.cvtColor(cv2.imread('sel_char_mem_bonus.png'),cv2.COLOR_BGR2GRAY)
select_characters_mem_size = select_characters_mem.shape[:2]
#949 108 点击的点为760 430 、737 591


start_game = cv2.cvtColor(cv2.imread('start.png'),cv2.COLOR_BGR2GRAY)
start_game_size = start_game.shape[:2]
#点击1223 675
atk_start = cv2.cvtColor(cv2.imread('attack_start.png'),cv2.COLOR_BGR2GRAY)
atk_start_size = atk_start.shape[:2]

AP= cv2.cvtColor(cv2.imread('AP.png'),cv2.COLOR_BGR2GRAY)
AP_size = AP.shape[:2]
AP_OK= cv2.cvtColor(cv2.imread('AP_OK.png'),cv2.COLOR_BGR2GRAY)
AP_OK_size = AP_OK.shape[:2]

def find_loc(screen,template,template_size):
	'''
	输入template和template_size,返回查找到的位置x，y和最小匹配的值（如果是0表示完美匹配）
	'''
	result = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
	return min_loc[0]+template_size[1]/2,min_loc[1]+template_size[0]/2,min_val

def startup():
	sleept1=6#再次挑战按钮之前那一屏的延时
	sleept=6#点再次挑战按钮之后的延时
	sleeps=6#选择助战后的延时
	sleepsg=20#开始之后等待的时间
	sleepi0=8#点开始攻击有弹幕的那一屏之后的延时
	ts=1
	dif=10000#门限值，从截屏中找到的子图与前面png里的子图的差异程度
	time_start=time.time()
	while(1):
		time.sleep(ts)
		ts=min(5,ts+0.2)
		pull_screenshot()
		sleeptimes='sleept='+str(sleept)+',sleept1='+str(sleept1)+',sleeps='+str(sleeps)+',sleepsg='+str(sleepsg)+',sleepi0='+str(sleepi0)
		screen=cv2.cvtColor(cv2.imread('scr.png'),cv2.COLOR_BGR2GRAY)
		
		x,y,res=find_loc(screen,p60,p60_size)
		print('匹配+60:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			time_dur=time_end-time_start
			sleepi0=min((sleepi0*0.3+(time_dur-ts)*0.5),2)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_end-time_start)+',('+str(x)+','+str(y)+')选择助战中...')
			time_start=time_end
			time.sleep(sleeps)
			ts=0.2
			continue
		
		x,y,res=find_loc(screen,select_characters_mem,select_characters_mem_size)
		print('匹配select_characters_mem:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			time_dur=time_end-time_start
			sleepi0=min((sleepi0*0.3+(time_dur-ts)*0.5),2)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_end-time_start)+',('+str(x)+','+str(y)+')选择助战中_mem...')
			time_start=time_end
			time.sleep(sleeps)
			ts=0.2
			continue
		
		x,y,res=find_loc(screen,select_characters,select_characters_size)
		print('匹配select_characters:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			time_dur=time_end-time_start
			sleepi0=min((sleepi0*0.3+(time_dur-ts)*0.5),2)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_end-time_start)+',('+str(x)+','+str(y)+')选择助战中...')
			time_start=time_end
			time.sleep(sleeps)
			ts=0.2
			continue
		
		
		x,y,res=find_loc(screen,start_game,start_game_size)
		print('匹配start_game:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			time_dur=time_end-time_start
			sleeps=min((sleeps*0.3+(time_dur-ts)*0.5),2)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_dur)+',('+str(x)+','+str(y)+')开始战斗...')
			time_start=time_end
			time.sleep(sleepsg)
			ts=0.2
			continue
			
		
		
		x,y,res=find_loc(screen,exp_get,exp_get_size)
		print('匹配exp get:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			time_dur=time_end-time_start
			sleepsg=(sleepsg*0.3+(time_dur-ts)*0.6)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_end-time_start)+',('+str(x)+','+str(y)+')已结束，将继续...')
			time_start=time_end
			time.sleep(sleept1)
			ts=0.2
			continue
		else:
			x,y,res=find_loc(screen,exp_get_2,exp_get_2_size)
			print('匹配exp get2:'+str(res),end='\r')
			if res<dif:
				time_end=time.time()
				time_dur=time_end-time_start
				sleepsg=(sleepsg*0.3+(time_dur-ts)*0.6)
				click_loc(x,y)
				print(sleeptimes+'\n历时'+str(time_end-time_start)+',('+str(x)+','+str(y)+')已结束，将继续...')
				time_start=time_end
				time.sleep(sleept1)
				ts=0.2
				continue
			
		x,y,res=find_loc(screen,item_get,item_get_size)
		print('匹配item get:'+str(res),end='\r')
		if res<dif:
			x=1161
			y=641
			time_end=time.time()
			time_dur=time_end-time_start
			sleept1=min((sleept1*0.3+(time_dur-ts)*0.5),2)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_dur)+',('+str(x)+','+str(y)+')继续...')
			time_start=time_end
			time.sleep(sleept)
			ts=0.2
			continue
		else:
			x,y,res=find_loc(screen,item_get_2,item_get_2_size)
			print('匹配item get:'+str(res),end='\r')
			if res<dif:
				x=1161
				y=641
				time_end=time.time()
				time_dur=time_end-time_start
				sleept1=min((sleept1*0.3+(time_dur-ts)*0.5),2)
				click_loc(x,y)
				print(sleeptimes+'\n历时'+str(time_dur)+',('+str(x)+','+str(y)+')继续...')
				time_start=time_end
				time.sleep(sleept)
				ts=0.2
				continue
		
		x,y,res=find_loc(screen,atk_start,atk_start_size)
		print('匹配atk_start:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			time_dur=time_end-time_start
			sleept=min((sleept*0.3+(time_dur-ts)*0.5),2)
			click_loc(x,y)
			print(sleeptimes+'\n历时'+str(time_dur)+',('+str(x)+','+str(y)+')开始attack...')
			time_start=time_end
			time.sleep(sleepi0)
			ts=0.2
			continue
		
		x,y,res=find_loc(screen,AP,AP_size)
		print('AP回复:'+str(res),end='\r')
		if res<dif:
			time.sleep(1)
			click_loc(x,y)
			while 1:
				time.sleep(1)
				pull_screenshot()
				screen=cv2.cvtColor(cv2.imread('scr.png'),cv2.COLOR_BGR2GRAY)
				x,y,res=find_loc(screen,AP_OK,AP_OK_size)
				if res<dif:
					click_loc(x,y)
					print(sleeptimes+'\n历时'+str(time_dur)+',('+str(x)+','+str(y)+')已经回复AP...')
					break
			time_start=time.time()
			ts=0.2
			continue
		
		x,y,res=find_loc(screen,s110,s110_size)
		print('匹配110:'+str(res),end='\r')
		if res<dif:
			time_end=time.time()
			x=500
			y=500
			click_loc(x,y)
			#print(sleeptimes+'\n历时'+str(time_dur)+',('+str(x)+','+str(y)+')开始战斗...')
			time_start=time_end
			#time.sleep(sleepsg)
			#ts=1
			continue
		
		
if __name__ == "__main__":
	startup()