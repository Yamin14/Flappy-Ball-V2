import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.clock import Clock
from kivy.uix.label import Label
import random

class Game(Widget):
	def __init__(self, **kwargs):
		super(Game, self).__init__(**kwargs)
		self.play()
		
	def play(self):
		self.x, self.y = 50, 700
		self.score = 0
		
		self.speed = 3
		self.drop = 7
		self.jumping = False

		self.jump_count = 10
		self.neg = 1
		
		self.game_over_bool = False
		self.game_start = False
		
		self.bg_color = (0, 0.5, 0.5)
		self.pill_color = (1, 1, 0)
		self.ball_color = (0, 1, 0)
		self.label_color = (1, 0.5, 0.5, 1)

		#background
		with self.canvas:
			Color(rgb=self.bg_color)
			Rectangle(size=(800, 1400), pos=(0, 0))
		
		#ball
		with self.canvas:
			Color(rgb=self.ball_color)
			self.ball = Ellipse(size=(100, 100), pos=(self.x, self.y))
			
		#pillars
		self.pill_width = 200
		self.pill_x = 700
		
		self.pill_up_height = random.randint(200, 900)
		self.pill_down_height = random.randint(200, 900)
		self.pill_up_y = 1400 - self.pill_up_height
		
		while (self.pill_up_y -  self.pill_down_height < 330) or (self.pill_up_y -  self.pill_down_height > 360):
			self.pill_up_height = random.randint(200, 900)
			self.pill_down_height = random.randint(200, 900)
			self.pill_up_y = 1400 - self.pill_up_height
		
		with self.canvas:
			Color(rgb=self.pill_color)
			self.pill_up = Rectangle(size=(self.pill_width, self.pill_up_height), pos=(self.pill_x, self.pill_up_y))
			
		with self.canvas:
			Color(rgb=self.pill_color)
			self.pill_down = Rectangle(size=(self.pill_width, self.pill_down_height), pos=(self.pill_x, 0))
			
		#score
		self.score_label = Label(text=(f"Score: {self.score}"), pos=(40, 1300), font_size=40, color=self.label_color)
		self.add_widget(self.score_label)
		
		#ground
		with self.canvas:
			Color(rgb=(0.4, 0.4, 0))
			self.ground = Rectangle(size=(800, 70), pos=(0, 0))
	
		Clock.schedule_interval(self.move, 0)

	def move(self, dt):
		if self.game_start == True:
			
			if self.x < 150:
				self.x += self.speed
			self.pill_x -= self.speed
			
		#jump
			if self.jumping == False:
				self.y -= self.drop
				self.drop += 0.5
			
			else:
				self.drop = 7
				if self.jump_count >= -3:
					self.neg = 1
					if self.jump_count < 0:
						self.neg = -1
					self.y += (self.jump_count**2)/3 * self.neg
					self.jump_count -= 1
				else:
					self.jump_count = 10
					self.jumping = False

		#increment score
			if self.pill_x + self.pill_width < self.x:
				self.pill_x = 700
				self.score += 1
				self.speed += 0.005
			
			#new pillars
				self.pill_up_height = random.randint(200, 900)
				self.pill_down_height = random.randint(200, 900)
				self.pill_up_y = 1400 - self.pill_up_height
		
				while (self.pill_up_y -  self.pill_down_height < 330) or (self.pill_up_y -  self.pill_down_height > 360):
					self.pill_up_height = random.randint(200, 900)
					self.pill_down_height = random.randint(200, 900)
					self.pill_up_y = 1400 - self.pill_up_height
				
			self.pill_up.size = (self.pill_width, self.pill_up_height)
			self.pill_up.pos = (self.pill_x, self.pill_up_y)
			
			self.pill_down.size = (self.pill_width, self.pill_down_height)
			self.pill_down.pos = (self.pill_x, 0)
		
		#change ball position and score label
		self.ball.pos = (self.x, self.y)
		self.score_label.text = f"Score: {self.score}"
		
		#check collision
		if self.y <= 70:
			self.game_over_bool = True
			self.game_over()

		if (self.x + 100 > self.pill_x and self.x < self.pill_x + self.pill_width) and (self.y + 100> self.pill_up_y or self.y < self.pill_down_height):
			self.game_over_bool = True
			self.game_over()
				
	def game_over(self):
		if self.game_over_bool == True:
		
			self.speed = 0
			self.drop = 0
			self.acc = 0
			self.jump_count = -11
		
		#game over screen
			with self.canvas:
				Color(rgb=self.bg_color)
				Rectangle(size=(800, 1400), pos=(0, 0))
		
		#game over label
			with self.canvas:
				Color(rgba=self.label_color)
				Label(text=f"""Game Over
Score: {self.score}""", pos=(300, 700), font_size=70, color=self.label_color)


	def on_touch_down(self, touch):
		self.jumping = True
		self.game_start = True
		self.ground = self.y

class MyApp(App):
	def build(self):
		return Game()
	
if __name__ == "__main__":
	MyApp().run()
