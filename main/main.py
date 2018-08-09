"""
# -*- coding: utf-8 -*-
# @Author: Clarence
# @Date:   2018-03-11 09:18:23
# @Last Modified by:   Clarence
# @Last Modified time: 2018-03-21 21:22:49
"""
"""
游戏的基本设定
敌方共有大中小3款飞机，分为高中低三种速度;
子弹的射程并非全屏，而大概是屏幕长度的80%;
消灭小飞机需要1发子弹，中飞机6000分，打飞机10000分；
每隔30秒有一个随机的道具补给，分为两种道具，全屏炸弹和双倍子弹;
全屏炸弹最多只能存放3枚，双倍子弹可以维持18秒钟的效果;
游戏将根据分数来逐步提高难度，难度的提高表现为飞机数量的增多以及速度的加快。
为中飞机和打飞机增加了血槽的显示，这样我们可以直观的知道敌机快被消灭了没有;
我方有三次机会，每次被敌人消灭，新诞生的飞机会有3秒钟的安全期;
游戏结束后会显示历史最高分数;
绘制小型机和中型机和大型机的顺序也很重要。先绘制大的，后绘制小的，这样不会遮挡
在敌机和自己飞机类中放入毁灭图片的Surface对象,设置它们的存活状态
main()中需要检测各种机的active属性的值，判断飞机是否受到撞击，根据不同值绘制不同的图片
pygame.sprite.spritecollide(sprite, group, dokill, collided = None) -> Sprite_list
Returns a list containing all Sprites in a Group that intersect with another Sprite.
Intersection is determinded by comparing the Sprite.rect attribute of each Sprite.
The dokill argument is a bool. If set to True, all Sprites that collide will be removed from the Group.
The collided argument is a callback function used to calculate if two sprites are colliding. it 
should take two sprites as values, and return a bool value indicating if they are colliding. If 
collided is not passed, all sprites musc have a "rect" value, which is a rectangle of the 
sprite area, which will be used to calculate the collision.
注意spritecollide()方法默认情况是以Sprite.rect attribute of each Sprite也就是精灵的rect属性作为比较看是否重叠

也就是碰撞检测是以精灵的矩形区域作为检测标准，这样导致飞机没有撞击到敌机就会爆炸了
那么我们可以使用pygame.mask.from_surface(Surface, threshold = 127) -> Mask
	Makes the transparent parts of the Surface not set, and the opaque parts set.
	The alpha of each pixel is checked to see if it it greateer than the given treshold.
	If the Surface is color-keyed, the thredshold is not used.
这个方法返回传入Surface对象的非透明部分
我们可以在pygame.sprite.spritecollide()中将collided设置成pygame.sprite.collide_mask()
注意在使用这个回调函数的时候精灵(飞机)必须要有"rect"属性，可选择的mask属性
Pygame默认情况下只有八条通道音效
设置通过pygame.mixer.set_num_channels()方法
	Sets the number of available channels for the mixer. The default 
value is 8. The value can be increased or decreased. If the value 
is decreased, sounds playing on the truncated channels are stopped.

关于子弹的分为两种类型 一种是一次只能发射一颗子弹，另一种是一次发射两颗子弹
编写子弹类，子弹的初始位置在飞机上方的位置 绘制子弹之后进行碰撞检测
给中大型敌机添加血量，每当被集中的时候中大型敌机对象的energy属性减一
血量大于百分之二十的时候是绿色状态，如果是小于百分之二十则是红色

在游戏界面上显示得分
pygame.font.Font(filename, size) -> Font
	Load a new font form a given filename or a python file object.
The size is the height of the font in pixels. If the filename is 
None the pygame default font will be loaded. 
pygame.font.Font(filename, size).render(text, antialias, color, background = None) -> Surface
	Draw text on a new Surface antialias参数是是否抗锯齿(布尔类型)

为游戏添加暂停按钮:
鼠标悬浮在按钮上方的时候按钮颜色变深

让游戏难度随着玩家得分增加而增加 
增加敌机速度或者改变敌机的数量
一共有四种难度级别

使用空格键来释放炸弹，飞机最多携带3枚炸弹 
炸弹可以将屏幕内所有的敌机毁灭
游戏设计每三十秒就随机发送一个补给包(炸弹或者子弹包)
可以通过设置自定义事件和time模块来定时发放补给
pygame.time.set_timer(eventid, milliseconds) -> None
	Set an event type to appear on the event queue every
given number of milliseconds. The first event will not appear
until the amount of time has passed.
	Every event type can have a separate timer attached to it.
It is best to use the value between pygame.USEREVENT and pygame
.NUMEVENTS. To disable the timer for an event, set the milliseconds argument to 0.
every
检测我方飞机是否和补给发生碰撞
pygame.sprite.collide_mask(SpriteLeft, SpriteRight) > point
	Returns first point on the mask where the masks collided, or None if there was no collision.

暂停音效区分pygame.mixer.stop()和pygame.mixer.pause()
pgyame.mixer.stop(): stop playback of all sound channels 
pygame.mixer.pause(): temporarily top playback of all sound channels.
我们暂停音效之后点击开始按钮还要继续播放音乐，因此选择pygame.mixer.pause()就行了

当玩家接到超级子弹补给包之后每次同时发射两颗子弹，并且子弹的速度会加快
使用超级子弹的时间是18秒(需要一个定时器来控制)并且使用超级子弹时间到了之后会切换成普通子弹

玩家飞机总共有三条命，在窗口右下角绘制我方剩余生命数量，如果发生碰撞，则少绘制一个小飞机
如果玩家重新诞生的地方正好有敌机的话，我方会落地成盒，因此要给我重生之后三秒钟的安全期

游戏结束之后会显示一个界面，显示你的历史最高分 并显示你当前的分数
显示两个按钮，点击之后可以结束游戏或者重新开始游戏
"""

import pygame
from pygame.locals import *
import sys
import traceback
import myplane
import enemy
import bullet
import supply
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战 -- Clarence")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.mixer.set_num_channels(50)
# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2) 

def add_small_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.SmallEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def add_mid_enemies(group1, group2, num):
	for i in range(num):
		e2 = enemy.MidEnemy(bg_size)
		group1.add(e2)
		group2.add(e2)

def add_big_enemies(group1, group2, num):
	for i in range(num):
		e3 = enemy.BigEnemy(bg_size)
		group1.add(e3)
		group2.add(e3)

def inc_speed(target, inc):
	for each in target:
		each.speed += inc

def main():
	'''
	pygame.mixer.music.play(loops = 0, start = 0.0) -> None
	The loops arguments controls the number of repeats a music will play. play(5) 
	will cause the music to played once, then repeated five times, for a total
	of six. If the loops is -1 then teh music will repeat indefinitely.
	'''
	pygame.mixer.music.play(-1)

	#生成我方飞机
	me = myplane.MyPlane(bg_size)

	#所有敌机放入到组里面
	enemies = pygame.sprite.Group()

	# 生成敌方小型飞机 随着难度增加会增加飞机数量
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies, enemies, 15)

	# 生成敌方中型飞机 随着难度增加会增加飞机数量
	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies, enemies, 4)

	# 生成敌方大型飞机 随着难度增加会增加飞机数量
	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies, enemies, 15)

	#生成普通子弹
	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4
	for i in range(BULLET1_NUM):
		#子弹生成位置是飞机顶部中央 midtop表示顶部中央的意思 4*12 = 48
		bullet1.append(bullet.Bullet1(me.rect.midtop))

	#生成超级子弹
	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 8
	for i in range(BULLET2_NUM // 2):
		# 飞机左右两边发射子弹
		bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
		bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

	clock = pygame.time.Clock()

	# 中弹图片索引
	e1_destroy_index = 0
	e2_destroy_index = 0
	e3_destroy_index = 0
	me_destroy_index = 0

	# 统计得分
	score = 0
	score_font = pygame.font.Font("font/font.ttf", 36)

	# 标志是否暂停游戏
	paused = False
	pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
	pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
	resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
	resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
	paused_rect = pause_nor_image.get_rect()
	paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
	paused_image = pause_nor_image

	# 设置难度级别
	level = 1

	#全屏炸弹
	bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_font = pygame.font.Font("font/font.ttf", 48)
	bomb_num = 3

	# 每30秒触发发放一个补给包
	bullet_supply = supply.Bullet_Supply(bg_size)
	bomb_supply = supply.Bomb_Supply(bg_size)
	# 自定义事件
	SUPPLY_TIMER = USEREVENT
	pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)

	# 超级子弹定时器
	DOUBLE_BULLET_TIMER = USEREVENT + 1

	# 标记是否使用超级子弹
	is_double_bullet = False

	# 接触我方无敌状态定时器
	INVINCIBLE_TIMER = USEREVENT + 2

	# 用于切换飞机图片
	switch_image = True

	# 飞机生命数量
	life_image = pygame.image.load("images/life.png").convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3

	# 用于阻止重复打开读写文件
	recorded = False

	# 游戏结束画面

	gameover_font = pygame.font.Font("font/font.ttf", 48)
	again_image = pygame.image.load("images/again.png").convert_alpha()
	again_rect = again_image.get_rect()
	gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
	gameover_rect = gameover_image.get_rect()

	# 用于飞机切换时间延时
	delay = 100

	running = True

	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()

			elif event.type == MOUSEBUTTONDOWN:
				# collidepoint() test if a point is inside a rectangle
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused
					'''
					按下暂停键停止一切音效
					'''
					if paused:
						# 停止计时器计时
						pygame.time.set_timer(SUPPLY_TIMER, 0)
						# 停止背景音乐的播放
						pygame.mixer.music.pause()
						# 停止大飞机出现后的音效
						pygame.mixer.pause() 
					else:
						pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()
				

			elif event.type == MOUSEMOTION:
				"""
				如果鼠标在按钮区域内移动，如果是暂停状态，则设置深色暂停按钮，否则设置深色正常按钮
				如果鼠标不在按钮区域内，如果是暂停状态，则设置浅色暂停按钮，否则设置浅色正常按钮
				"""
				if paused_rect.collidepoint(event.pos):
					if paused:
						paused_image = resume_pressed_image
					else:
						paused_image = pause_pressed_image
				else:
					if paused:
						paused_image = resume_nor_image
					else:
						paused_image = pause_nor_image

			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if bomb_num:
						bomb_num -= 1
						bomb_sound.play()
						#所有在屏幕中的敌机都毁灭了
						for each in enemies:
							if each.rect.bottom > 0:
								each.active = False

			elif event.type == SUPPLY_TIMER:
				# 播放发放补给的声音
				supply_sound.play()
				if choice([True, False]):
					bomb_supply.reset()
				else:
					bullet_supply.reset()

			elif event.type == DOUBLE_BULLET_TIMER:
				# 定时器时间到了之后切换成普通子弹
				is_double_bullet = False
				pygame.time.set_timer(DOUBLE_BULLET_TIMER, 0)

			elif event.type == INVINCIBLE_TIMER:
				# 取消无敌状态并停止计时器
				me.invincible = False
				pygame.time.set_timer(INVINCIBLE_TIMER, 0)


		# 根据用户的得分增加难度:
		if level == 1 and score > 50000:
			level = 2
			# 播放增加难度音效
			upgrade_sound.play()
			# 增加三架小型敌机，两架中型敌机和一架大型敌机
			add_small_enemies(small_enemies, enemies, 3)
			add_mid_enemies(mid_enemies, enemies, 2)
			add_big_enemies(big_enemies, enemies, 1)
			# 提升小型敌机的速度
			inc_speed(small_enemies, 1)

		elif level == 2 and score > 300000:
			level = 3
			# 播放增加难度音效
			upgrade_sound.play()
			# 增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			# 提升小型敌机的速度
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		elif level == 3 and score > 600000:
			level = 4
			# 播放增加难度音效
			upgrade_sound.play()
			# 增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			# 提升小型中型敌机的速度
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		elif level == 4 and score > 1000000:
			level = 5
			# 播放增加难度音效
			upgrade_sound.play()
			# 增加5架小型敌机，3架中型敌机和2架大型敌机
			add_small_enemies(small_enemies, enemies, 5)
			add_mid_enemies(mid_enemies, enemies, 3)
			add_big_enemies(big_enemies, enemies, 2)
			# 提升小型中型敌机的速度
			inc_speed(small_enemies, 1)
			inc_speed(mid_enemies, 1)

		# 暂停之后将看不到飞机，这样增加游戏的难度和趣味性
		screen.blit(background, (0, 0))
		if life_num and not paused:
			#检测用户的键盘操作
			key_pressed = pygame.key.get_pressed()

			#如果键盘上的W和方向上键被按下 飞机向上走
			if key_pressed[K_w] or key_pressed[K_UP]:
				me.moveUp()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.moveDown()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.moveLeft()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.moveRight()

			# 绘制全屏炸弹补给并检测补给是否获得
			if  bomb_supply.active:
				bomb_supply.move()
				screen.blit(bomb_supply.image, bomb_supply.rect)
				if pygame.sprite.collide_mask(bomb_supply, me):
					# 播放我方飞机捡到补给的声音
					get_bomb_sound.play()
					if bomb_num < 3:
						bomb_num += 1
					bomb_supply.active = False

			# 绘制超级子弹补给并检测补给是否获得
			if  bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image, bullet_supply.rect)
				if pygame.sprite.collide_mask(bullet_supply, me):
					# 播放我方飞机捡到补给的声音
					get_bullet_sound.play()
					is_double_bullet = True
					pygame.time.set_timer(DOUBLE_BULLET_TIMER, 18 * 1000)
					# 补给包消逝
					bullet_supply.active = False


			# 发射子弹
			if not(delay % 10):
				# 播放子弹的声音
				bullet_sound.play()
				# 超级子弹模式
				if is_double_bullet:
					bullets = bullet2
					bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
					bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
					bullet2_index = (bullet2_index + 2) % BULLET2_NUM
				# 普通子弹模式
				else:
					bullets = bullet1
					bullets[bullet1_index].reset(me.rect.midtop)
					bullet1_index = (bullet1_index + 1) % BULLET1_NUM

			# 绘制子弹并检测子弹是否击中敌机
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image, b.rect)
					enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
					if enemy_hit:
						b.active = False
						for e in enemy_hit:
							# 如果是中大型敌机被击中
							if e in mid_enemies or e in big_enemies:
								e.hit = True
								e.energy -= 1
								if e.energy == 0:
									e.active = False
							else:
								e.active = False
			# 绘制大型敌机
			for each in big_enemies:
				if each.active:	
					each.move()
					if each.hit:
						# 绘制被打到的特效
						screen.blit(each.image_hit, each.rect)
						each.hit = False 
					else:
						if switch_image:
							screen.blit(each.image1, each.rect)
						else:
							screen.blit(each.image2, each.rect)

					# 绘制血槽 两个像素的宽度
					pygame.draw.line(screen, BLACK, \
						(each.rect.left, each.rect.top - 5),\
						(each.rect.right, each.rect.top - 5),\
						2)
					#当生命大于%20显示绿色，否则显示红色
					energy_remain = each.energy / enemy.BigEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color,\
						(each.rect.left, each.rect.top - 5),\
						(each.rect.left + each.rect.width * energy_remain,\
							each.rect.top - 5), 2)

					# 即将出现在画面中,播放音效enemy3_fly_sound.wav
					if each.rect.bottom == -50:
						enemy3_fly_sound.play(-1)
				else:
					# 毁灭
					# 一秒帧
					if not(delay % 3):
						#刚开始音乐播放一次就行了
						if e3_destroy_index == 0:
							enemy3_down_sound.play()
						# e3_destroy_index索引在0-5之间,因此依次播放6章图片
						screen.blit(each.destroy_images[e3_destroy_index], each.rect)
						#e3_destroy_index范围在0-5之间
						e3_destroy_index  = (e3_destroy_index + 1) % 6
						if e3_destroy_index == 0:
							enemy3_fly_sound.stop()
							score += 10000
							each.reset()


			# 绘制中型敌机:
			for each in mid_enemies:
				if each.active:
					each.move()
					if each.hit:
						screen.blit(each.image_hit, each.rect)
						each.hit = False
					else:
						screen.blit(each.image, each.rect)

					# 绘制血槽 两个像素的宽度
					pygame.draw.line(screen, BLACK, \
						(each.rect.left, each.rect.top - 5),\
						(each.rect.right, each.rect.top - 5),\
						2)
					#当生命大于%20显示绿色，否则显示红色
					energy_remain = each.energy / enemy.MidEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color,\
						(each.rect.left, each.rect.top - 5),\
						(each.rect.left + each.rect.width * energy_remain,\
							each.rect.top - 5), 2)

				else:
					# 毁灭
					if not (delay % 3):
						#刚开始音乐播放一次就行了
						if e3_destroy_index == 0:
							enemy2_down_sound.play()
						screen.blit(each.destroy_images[e2_destroy_index], each.rect)
						e2_destroy_index = (e2_destroy_index + 1) % 4
						if e2_destroy_index == 0:
							score += 6000
							each.reset()

			# 绘制小型敌机
			for each in small_enemies:
				if each.active:		
					each.move()
					screen.blit(each.image, each.rect)
				else:
					# 毁灭
					if not(delay % 3):
						#刚开始音乐播放一次就行了
						if e3_destroy_index == 0:
							enemy1_down_sound.play()
						screen.blit(each.destroy_images[e1_destroy_index], each.rect)
						e1_destroy_index = (e1_destroy_index + 1) % 4
						if e1_destroy_index == 0:
							score += 1000
							each.reset()

			# 检测我方飞机是否被撞
			enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
			# 如果列表中有精灵存在，并且我方飞机不处于无敌状态.则将被撞的敌机和我方飞机的active属性设置成False
			if enemies_down and not me.invincible:
				me.active = False
				for e in enemies_down:
					e.active = False

			# 绘制我方飞机
			if me.active:
				if switch_image:
					screen.blit(me.image1, me.rect)
				else:
					screen.blit(me.image2, me.rect)
			else:
				# 毁灭
				if not(delay % 3):
					if me_destroy_index == 0:
						me_down_sound.play()
					screen.blit(me.destroy_images[me_destroy_index], me.rect)
					me_destroy_index = (me_destroy_index + 1) % 4
					if me_destroy_index == 0:
						life_num -= 1
						me.reset()
						# reset()方法将飞机设置成无敌，三秒之后解除无敌状态
						pygame.time.set_timer(INVINCIBLE_TIMER, 3 * 1000)

			# 绘制全屏炸弹数量
			bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
			text_rect = bomb_text.get_rect()
			screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
			screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

			# 绘制剩余生命数量
			if life_num:
				for i in range(life_num):
					screen.blit(life_image,\
						(width-10-(i+1) * life_rect.width,\
							height - 10 - life_rect.height))

			# 绘制得分
			score_text = score_font.render("Score : %s" % str(score), True, WHITE)
			screen.blit(score_text, (10, 5))

		# 绘制游戏结束画面
		elif life_num == 0:
			# 背景音乐停止
			pygame.mixer.music.stop()

			# 停止全部音效
			pygame.mixer.stop()

			# 停止发放补给
			pygame.time.set_timer(SUPPLY_TIMER, 0)

			if not recorded:
				recorded = True
				# 读取历史最高得分
				with open("record.txt", "r") as fileobject:
					record_score = int(fileobject.read())

				# 如果玩家得分高于历史最高得分，则存档
				if score > record_score:
					with open("record.txt", "w") as fileobject:
						fileobject.write(str(score))

			# 绘制结束界面
			record_score_text = score_font.render("Best : %d" % record_score, True, WHITE)
			screen.blit(record_score_text, (50, 50))

			gameover_text1 = gameover_font.render("Your Score", True, WHITE)
			gameover_text1_rect = gameover_text1.get_rect()
			gameover_text1_rect.left, gameover_text1_rect.top = \
			(width - gameover_text1_rect.width) // 2, height // 3
			screen.blit(gameover_text1, gameover_text1_rect)

			gameover_text2 = gameover_font.render(str(score), True, WHITE)
			gameover_text2_rect = gameover_text2.get_rect()
			gameover_text2_rect.left, gameover_text2_rect.top = \
			(width - gameover_text2_rect.width) // 2, \
			gameover_text1_rect.bottom + 10
			screen.blit(gameover_text2, gameover_text2_rect)

			again_rect.left, again_rect.top = \
			(width - again_rect.width) // 2, \
			gameover_text2_rect.bottom + 50
			screen.blit(again_image, again_rect)

			gameover_rect.left, gameover_rect.top = \
			(width - again_rect.width) // 2, \
			again_rect.bottom + 10
			screen.blit(gameover_image, gameover_rect)

			# 检测用户的鼠标操作
			# 如果用户按下鼠标左键
			if pygame.mouse.get_pressed()[0]:
				# 获取鼠标坐标
				pos = pygame.mouse.get_pos()
				# 如果用户点击"重新开始"
				if again_rect.left < pos[0] < again_rect.right and \
				again_rect.top < pos[1] < again_rect.bottom:
					#调用main函数，重新开始游戏
					main()
				# 如果用户点击"游戏结束"
				elif gameover_rect.left < pos[0] < gameover_rect.right and \
				gameover_rect.top < pos[1] < gameover_rect.bottom:
					#退出游戏
					pygame.quit()
					sys.exit()

		# 绘制暂停按钮
		screen.blit(paused_image, paused_rect)

		# 切换图片 每5帧切换一次，一秒钟切换12次
		if not(delay % 5):
			switch_image = not switch_image
		delay -= 1
		if not delay:
			delay = 100

		pygame.display.flip()

		clock.tick(60)

if __name__ == "__main__":
	try:
		main()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
		pygame.quit()
		input()