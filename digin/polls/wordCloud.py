from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
import matplotlib.pyplot as plt


class wordCloud:
	def __init__(self, width=800, height=400):
		self.width = width 
		self.height = height

	def check_grid(self, grid, font, x, y, offset_y, word):
		'''
		params:
			grid: indicates which index is occupied
			fontsize: object to get size of each character
			x, y: initial offset
			word: word to check size
		checks if each character intersects with the existing model
		'''
		tx = x
		for char in word:
			(_, _), (_, offset_y_) = font.font.getsize(char)
			for i in range(font.getsize(char)[0]):
				for j in range(font.getsize(char)[1]-offset_y_):
					if grid[i+tx][y+j+offset_y_] == 1:
						return False
			tx += font.getsize(char)[0]
		return True

	def check_grid_vertical(self, grid, font, x, y, offset_y, word):
		'''
		params:
			grid: indicates which index is occupied
			fontsize: tuple of size (width, height)
			x, y: initial offset
		checks if current fontsize interesect with existing words
		'''
		ty = y
		(_, _), (_, offset_y_) = font.font.font.getsize(word)
		for char in word[::-1]:
			(_, _), (_, offset_y_local) = font.font.font.getsize(char)
			for i in range(offset_y_local-offset_y_, font.getsize(char)[0]-offset_y_):
				for j in range(font.getsize(char)[1]):
					if grid[i+x][ty+j] == 1:
						return False
								
			ty += font.getsize(char)[1]
		return True
	
	def get_wordCloud(self, freq):	
		sorted_freq = sorted(freq.items(), key=lambda kv: kv[1], reverse=True)
		#image = Image.open("background.png").convert('RGBA')
		img = Image.new("RGBA", (self.width, self.height), color="white").convert('RGBA')

		draw = ImageDraw.Draw(img)
		orientation = Image.ROTATE_90
		font = ImageFont.truetype('Roboto-Bold.ttf', size=45)

		# initial size
		size = self.height // 4 * 2
		# initial grd
		grid = np.zeros((self.width, self.height))
		random_count = 100
		# loop thru words
		for test, value in sorted_freq:
			# randomly choose a color
			color = (random.randint(0, 225), random.randint(0, 225), random.randint(0, 225))
			# font initial size
			font = ImageFont.truetype('Roboto-Bold.ttf', size=size)
			# random offset
			(x,y) = (random.randint(0,self.width-1), random.randint(0,self.height-1))

			transposed = False

			ascent, descent = font.getmetrics()
			(w, baseline), (offset_x, offset_y) = font.font.getsize(test)
			print(w, baseline, offset_x, offset_y)
			#  finds the right size
			while(True):
				# boolean to quit loop
				new_size_working = False
				x_sum = 0
				y_sum = 0
				(width, baseline), (offset_x, offset_y) = font.font.getsize(test)
				# check initial font is okay
				for char in test:
					char_size = font.getsize(char)
					x_sum += char_size[0]
					y_sum = max(y_sum, char_size[1])
		
				if (x_sum + x < self.width and y + y_sum < self.height and self.check_grid(grid, font, x, y, offset_y, test)):
					new_size_working = True
					break
				############# HORITZONAL FONT ##########################
				for i in range(10):
					(x, y) = (random.randint(0,self.width-1), random.randint(0,self.height-1))
					# check right bottom is in range and no intersection
					x_sum = 0
					y_sum = 0
					for char in test:
						char_size = font.getsize(char)
						x_sum += char_size[0]
						y_sum = max(y_sum, char_size[1])
					if (x_sum + x < self.width and y + y_sum < self.height and self.check_grid(grid, font, x, y, offset_y, test)):
						new_size_working = True

						break
				# if horizontal work, then fill text
				if (new_size_working):
					break

				############# VERTICAL FONT ###############################
				font = ImageFont.TransposedFont(font, orientation=orientation)
				for i in range(random_count):
					(x, y) = (random.randint(0,self.width), random.randint(0,self.height))
					# check right bottom is in range and no intersection
					if (font.getsize(test)[0] + x <= self.width and font.getsize(test)[1] + y  <= self.height and self.check_grid_vertical(grid, font, x, y, offset_y, test)):
						new_size_working = True
						transposed = True
						break
				# decrase size if neither work
				if (new_size_working == False):
					size -= 1
					font = ImageFont.truetype('Roboto-Bold.ttf', size=size)
				else:
					break

			# mark the occupied blocks
			if (transposed == False):
				tx = x
				for char in test:
					(_, _), (_, offset_y_) = font.font.getsize(char)
					for i in range(font.getsize(char)[0]):
						for j in range(font.getsize(char)[1]-offset_y_):
							grid[i+tx][y+offset_y_+j] = 1.
					tx += font.getsize(char)[0]
				print(test, font.getsize(test)[0], font.getsize(test)[0]+x, font.getsize(test)[1], font.getsize(test)[1]+y)
				# draw text
			
				draw.text((x,y), test, fill=color, font=font)
			else:
				
				ty = y
				(_, _), (_, offset_y_) = font.font.font.getsize(test)
				for char in test[::-1]:
					(_, _), (_, offset_y_local) = font.font.font.getsize(char)
					# print(test, char, w,b,offset_x_, offset_y_)
					for i in range(offset_y_local-offset_y_, font.getsize(char)[0]-offset_y_):
						for j in range(font.getsize(char)[1]):
							grid[i+x][ty+j] = 1.
								
					ty += font.getsize(char)[1]
				# for i in range(font.getsize(test)[0]-offset_y):
				# 	for j in range(font.getsize(test)[1]):
				# 		grid[i+x][j+y] = 1.
				print(test, font.getsize(test)[0], font.getsize(test)[0]+x, font.getsize(test)[1], font.getsize(test)[1]+y)

				draw.text((x,y), test, fill=color, font=font)

		# pixels = img.load()
		# for i in range(img.size[0]):
		# 	for j in range(img.size[1]):
		# 		if (grid[i][j] == 0):
		# 			pixels[i,j] = (0, 0, 0)

		# show image
		return img
		