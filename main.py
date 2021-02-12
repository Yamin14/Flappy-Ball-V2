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
		
		self.x, self.y = 50, 700
		self.score = 0
		
		self.speed = 3.5
		self.drop = 3.5
		self.jumping = False

		self.jump_count = 10
		self.neg = 1
		
		#ball
		with self.canvas:
			Color(rgb=(0, 1, 0))
			self.ball = Ellipse(size=(100, 100), pos=(self.x, self.y))
			
		#pillars
		self.pill_width = 300
		self.pill_up_height = random.randint(400, 700)
		self.pill_down_height = random.randint(400, 700)
		self.pill_up_y = 1400 - self.pill_up_height
		
		while (self.pill_up_y -  self.pill_down_height < 300) or (self.pill_up_y -  self.pill_down_height > 360):
			self.pill_up_height = random.randint(400, 700)
			self.pill_down_height = random.randint(400, 700)
			self.pill_up_y = 1400 - self.pill_up_height
		
		with self.canvas:
			Color(rgb=(1, 1, 0))
			self.pill_up = Rectangle(size=(self.pill_width, self.pill_up_height), pos=(500, self.pill_up_y))
			
		with self.canvas:
			Color(rgb=(1, 1, 0))
			self.pill_down = Rectangle(size=(self.pill_width, self.pill_down_height), pos=(500, 0))
			
		#score
		self.score_label = Label(text=(f"Score: {self.score}"), pos=(40, 1300), font_size=40)
		self.add_widget(self.score_label)
	
		Clock.schedule_interval(self.move, 0)

	def move(self, dt):
		self.x += self.speed
		#jump
		if self.jumping == False:
			self.y -= self.drop
			
		else:
			if self.jump_count >= -8:
				self.neg = 1
				
				if self.jump_count < 0:
					self.neg = -1
				self.y += (self.jump_count**2)/3 * self.neg
				self.jump_count -= 1
			else:
				self.jump_count = 10
				self.jumping = False

		#increment score
		if self.x > 714:
			self.x = 0
			self.score += 1
			self.speed += 0.005
			
			#new pillars
			self.pill_up_height = random.randint(400, 700)
			self.pill_down_height = random.randint(400, 700)
			self.pill_up_y = 1400 - self.pill_up_height
		
			while (self.pill_up_y -  self.pill_down_height < 300) or (self.pill_up_y -  self.pill_down_height > 360):
				self.pill_up_height = random.randint(400, 700)
				self.pill_down_height = random.randint(400, 700)
				self.pill_up_y = 1400 - self.pill_up_height
				
			self.pill_up.size = (self.pill_width, self.pill_up_height)
			self.pill_up.pos = (500, self.pill_up_y)
			
			self.pill_down.size = (self.pill_width, self.pill_down_height)
		
		#change ball position and score label
		self.ball.pos = (self.x, self.y)
		self.score_label.text = f"Score: {self.score}"
		
		#check collision
		if (self.x + 100 > 500) and (self.y + 100> self.pill_up_y or self.y < self.pill_down_height):
			self.game_over()
				
	def game_over(self):
		self.speed = 0
		self.drop = 0
		self.acc = 0
		self.jump_count = -11
		
		#game over screen
		with self.canvas:
			Color(rgb=(0, 0, 0))
			Rectangle(size=(800, 1400), pos=(0, 0))
		
		#game over label
		with self.canvas:
			Color(rgb=(1, 1, 1))
			Label(text=f"""Game Over
Score: {self.score}""", pos=(300, 700), font_size=70)


	def on_touch_down(self, touch):
		self.jumping = True
		self.ground = self.y


class MyApp(App):
	def build(self):
		return Game()
	
if __name__ == "__main__":
	MyApp().run()
