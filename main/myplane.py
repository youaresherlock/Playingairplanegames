# -*- coding: utf-8 -*-
# @Author: Clarence
# @Date:   2018-03-17 23:45:29
# @Last Modified by:   Clarence
# @Last Modified time: 2018-03-21 20:28:59
"""
常用键盘事件的检响应有两种方法:
1.通过键盘事件的检测，执行相应的代码
2.pygame.key.get_pressed() 返回一个包含键盘上所有按键Bool类型值的序列
	Returns a sequence of boolean values representing the state of 
the every key on the keyboard. Use the key constant values to index 
the array.A True value means the that button is pressed.
建议对于偶然触发的事件用第一种方法，频繁触发的键盘事件使用第二种方法
控制飞机方向使用第二种方法
"""
import pygame

class MyPlane(pygame.sprite.Sprite):
	def __init__(self, bg_size):
		pygame.sprite.Sprite.__init__(self)
		#不断切换飞机的两张图片会产生喷气效果
		self.image1 = pygame.image.load("images/me1.png").convert_alpha()
		self.image2 = pygame.image.load("images/me2.png").convert_alpha()
		# 将受到撞击的图片Surface对象放入到列表中
		self.destroy_images = []
		self.destroy_images.extend([\
			pygame.image.load("images/me_destroy_1.png").convert_alpha(),\
			pygame.image.load("images/me_destroy_2.png").convert_alpha(),\
			pygame.image.load("images/me_destroy_3.png").convert_alpha(),\
			pygame.image.load("images/me_destroy_4.png").convert_alpha()\
			])

		self.rect  = self.image1.get_rect()
		self.width, self.height = bg_size[0], bg_size[1]
		#飞机的起始位置在屏幕的下方中央位置 距离底部状态栏大约60像素位置
		self.rect.left, self.rect.top=\
		(self.width - self.rect.width) // 2,\
		(self.height - self.rect.height - 60)

		self.speed = 10
		self.active = True
		self.invincible = False
		#将传进来的Surface对象中的非透明部分设置为mask 飞机边缘之外矩形之内的都是透明部分
		self.mask = pygame.mask.from_surface(self.image1)

	#定义四个方法描述飞机的上下左右移动
	def moveUp(self):
		if self.rect.top > 0:
			self.rect.top -= self.speed
		else:
			self.rect.top = 0

	def moveDown(self):
		if self.rect.bottom < self.height -60:
			self.rect.top += self.speed
		else:
			self.rect.bottom = self.height - 60

	def moveLeft(self):
		if self.rect.left > 0:
			self.rect.left -= self.speed
		else:
			self.rect.left = 0

	def moveRight(self):
		if self.rect.right < self.width:
			self.rect.left += self.speed
		else:
			self.rect.right = self.width

	def reset(self):	
		self.rect.left, self.rect.top = \
		(self.width - self.rect.width) // 2,\
		(self.height - self.rect.height - 60)

		self.active = True
		# 无敌状态只有三秒钟的时间
		self.invincible = True

