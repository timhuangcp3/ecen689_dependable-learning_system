import numpy as np
import pyglet
from pyglet.gl import *
import random
from Cars import Car, Tools 
import math
import copy



INIT_X = 350 # position of the initial reference point 
INIT_Y = 70 
CAR_LENGTH = 9 
CAR_WIDTH = 9 
L = 30*CAR_WIDTH # length between two circles
D = CAR_LENGTH # width of the road
BAR = 2*CAR_WIDTH # distance between a circle and a square 
ORIENTATION = [[1,0],[-1,0],[0,-1],[0,1]] #orientation,[1,0]:up, [-1,0]:down, [0,-1]:left, [0,1]:right

light = [None]*28
light[0] = [INIT_X - CAR_LENGTH, INIT_Y + L, INIT_X + CAR_LENGTH,   INIT_Y + L] # light1
light[1] = [INIT_X - CAR_LENGTH, INIT_Y + L, INIT_X - CAR_LENGTH, INIT_Y + L + 2*D] # light2 #
light[2] = [INIT_X - CAR_LENGTH, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH + 2*D, INIT_Y + L + 2*D] # light3
light[3] = [INIT_X + CAR_LENGTH , INIT_Y + L, INIT_X + CAR_LENGTH,   INIT_Y + L + 2*D] # light4
light[4] = [INIT_X - CAR_LENGTH - L - 2*D, INIT_Y - D*2, INIT_X - CAR_LENGTH - L, INIT_Y - D*2] # light5
light[5] = [INIT_X - CAR_LENGTH - L - 2*D, INIT_Y, INIT_X - CAR_LENGTH - L, INIT_Y] # light6
light[6] = [INIT_X - CAR_LENGTH - L, INIT_Y - D*2, INIT_X - CAR_LENGTH - L, INIT_Y] # light7
light[7] = [INIT_X - CAR_LENGTH - L - 2*D, INIT_Y + L, INIT_X - CAR_LENGTH - L, INIT_Y + L] # light8
light[8] = [INIT_X - CAR_LENGTH - L - 2*D, INIT_Y + L+2*D, INIT_X - CAR_LENGTH - L, INIT_Y + L+2*D] # light9
light[9] = [INIT_X - CAR_LENGTH - L, INIT_Y + L, INIT_X - CAR_LENGTH - L, INIT_Y + L+2*D] # light10
light[10] = [INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 2*D] # light11
light[11] = [INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 4*D] # light 12
light[12] = [INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 4*D] # light13
light[13] = [INIT_X - CAR_LENGTH, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH + 2*D, INIT_Y + 2*L + 2*D] # light14
light[14] = [INIT_X - CAR_LENGTH, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH, INIT_Y + 2*L + 4*D] # light15
light[15] = [INIT_X - CAR_LENGTH+2*D, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH+2*D, INIT_Y + 2*L + 4*D] # light16
light[16] = [INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH+2*D+L+2*D, INIT_Y + 2*L + 2*D] # light17
light[17] = [INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 4*D] # light18
light[18] = [INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH+2*D+L+2*D, INIT_Y + 2*L + 4*D] # light19
light[19] = [INIT_X - CAR_LENGTH+L+2*D, INIT_Y + L, INIT_X + CAR_LENGTH+L+2*D,   INIT_Y + L] # light20
light[20] = [INIT_X - CAR_LENGTH+L+2*D, INIT_Y + L, INIT_X - CAR_LENGTH+L+2*D, INIT_Y + L + 2*D] # light21
light[21] = [INIT_X - CAR_LENGTH+L+2*D, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH + 2*D+L+2*D, INIT_Y + L + 2*D] # light22
light[22] = [INIT_X - CAR_LENGTH+L+2*D, INIT_Y - 2*D, INIT_X - CAR_LENGTH+L+2*D, INIT_Y] # light23
light[23] = [INIT_X - CAR_LENGTH+L+2*D, INIT_Y, INIT_X - CAR_LENGTH + 2*D+L+2*D, INIT_Y] # light24
light[24] = [INIT_X - CAR_LENGTH + 2*D+L+2*D, INIT_Y - 2*D, INIT_X - CAR_LENGTH + 2*D+L+2*D, INIT_Y] #light25
light[25] = [INIT_X - CAR_LENGTH, INIT_Y - 2*D, INIT_X - CAR_LENGTH, INIT_Y] # light26
light[26] = [INIT_X - CAR_LENGTH, INIT_Y, INIT_X - CAR_LENGTH + 2*D, INIT_Y] # light27
light[27] = [INIT_X - CAR_LENGTH + 2*D, INIT_Y, INIT_X - CAR_LENGTH + 2*D, INIT_Y - 2*D]
traffic_lights_vertices = light.copy()

# four destinations
destinations = [[INIT_X - CAR_LENGTH-L-D-D, INIT_Y - 2*D - BAR,
				 INIT_X - CAR_LENGTH-L-D-D, INIT_Y - D - BAR,
				 INIT_X - CAR_LENGTH-L-D, INIT_Y - D - BAR,
				 INIT_X - CAR_LENGTH-L-D, INIT_Y - 2*D - BAR],#left bottom corner
				[INIT_X + CAR_LENGTH + L+D,     INIT_Y - 2*D+ 3*2*D + 2*L + BAR -D,
				 INIT_X + CAR_LENGTH + L+D,     INIT_Y - 2*D+ 3*2*D + 2*L + BAR,
				 INIT_X + CAR_LENGTH + L + D+D, INIT_Y - 2*D+ 3*2*D + 2*L + BAR,
				 INIT_X + CAR_LENGTH + L + D+D, INIT_Y - 2*D+ 3*2*D + 2*L + BAR-D],#right top corner
				[INIT_X + CAR_LENGTH + L + D+BAR, INIT_Y - D - D,
				 INIT_X + CAR_LENGTH + L + D+BAR, INIT_Y - D,
				 INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y - D,
				 INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y-D- D],#right bottowm corner
				[INIT_X - CAR_LENGTH-L-2*D-BAR,     INIT_Y + L + 2*D + L + D ,
				 INIT_X - CAR_LENGTH-L-2*D-BAR,     INIT_Y + L + 2*D + L +D + D,
				 INIT_X - CAR_LENGTH-L-2*D-BAR+D,   INIT_Y + L + 2*D + L +D + D,
				 INIT_X - CAR_LENGTH-L-2*D-BAR+D,     INIT_Y + L + 2*D + L + D]]#left top corner 

#use this class to generate new cars, change traffic light light, update car_list and traffic_light_list
class Traffic(object):
	viewer = None
	tools = None
	def __init__(self):
		self.car_list = [] # put all cars in this list
		self.car_reach_destination_list = [] # put all cars reaching the destination in this list
		self.traffic_lights_list = [] # put all traffic light light in this list
		self.intersection_list = [] # put all intersections in this list
		self.traffic_light_object_list = [] #put all traffic light object in this list
		self.flag = True
		self.success = 0
		self.fail = 0
		self.map = [[None for x in range(70)] for y in range(70)]
		self.reach_destination = 0
		self.car_waiting_time = {} #put the updated waiting time for each car
		self.count_car_duplicate_position = {}
		self.num_of_collisions = 0
		self.check_red_light_violation_list = []
		self.num_of_red_light_violations = 0
		self.time = 0
		directions = ['up','down','left','right']
		table = {}
		for i in range(9):
			p = {}
			for j in directions:
				p[j] = 0.0
			table[str(i)] = p
		self.tables = [table, copy.deepcopy(table), copy.deepcopy(table), copy.deepcopy(table)]
		

	#manage car list
	def manage_cars(self, training):
		self.tools.run_cars(self.car_list, self.map, self.car_reach_destination_list, self.intersection_list, self.tables, training)
		
	def create_traffic_lights(self):
		i1 = Intersection(4) # crossroad
		i2 = Intersection(2) # t-junction
		i3 = Intersection(3) # t-junction
		i4 = Intersection(2) # t-junction
		i5 = Intersection(3) # t-junction
		i6 = Intersection(2) # t-junction
		i7 = Intersection(3) # t-junction
		i8 = Intersection(2) # t-junction
		i9 = Intersection(3) # t-junction
		
		l1 = Traffic_Lights()
		l1.direction = 0 #either vertical(0) or horizontal(1)
		l1.light = 0 #either green(1) or red(0)
		l1.position = [35, 35]
		
		l2 = Traffic_Lights()
		l2.direction = 1 #either vertical or horizontal
		l2.light = 0 #either green or red
		l2.position = [35, 34]
                
		
		l3 = Traffic_Lights()
		l3.direction = 0 #either vertical or horizontal
		l3.light = 0 #either green or red
		l3.position = [34, 34]
		
		l4 = Traffic_Lights()
		l4.direction = 1 #either vertical or horizontal
		l4.light = 0 #either green or red
		l4.position = [34, 35]
		
		l5 = Traffic_Lights()
		l5.direction = 0 #either vertical or horizontal
		l5.light = 0 #either green or red
		l5.position = [67, 3]
		
		l6 = Traffic_Lights()
		l6.direction = 0 #either vertical or horizontal
		l6.light = 0 #either green or red
		l6.position = [66, 2]
		
		l7 = Traffic_Lights()
		l7.direction = 1 #either vertical or horizontal
		l7.light = 0 #either green or red
		l7.position = [66, 3]
		
		l8 = Traffic_Lights()
		l8.direction = 0 #either vertical or horizontal
		l8.light = 0 #either green or red
		l8.position = [35, 3]
		
		l9 = Traffic_Lights()
		l9.direction = 0 #either vertical or horizontal
		l9.light = 0 #either green or red
		l9.position = [34, 2]
		
		l10 = Traffic_Lights()
		l10.direction = 1 #either vertical or horizontal
		l10.light = 0 #either green or red
		l10.position = [34, 3]
		
		l11 = Traffic_Lights()
		l11.direction = 0 #either vertical or horizontal
		l11.light = 0 #either green or red
		l11.position = [3, 3]
		
		l12 = Traffic_Lights()
		l12.direction = 1 #either vertical or horizontal
		l12.light = 0 #either green or red
		l12.position = [3, 2]
		
		l13 = Traffic_Lights()
		l13.direction = 1 #either vertical or horizontal
		l13.light = 0 #either green or red
		l13.position = [2, 3]
		
		l14 = Traffic_Lights()
		l14.direction = 0 #either vertical or horizontal
		l14.light = 0 #either green or red
		l14.position = [3, 35]
		
		l15 = Traffic_Lights()
		l15.direction = 1 #either vertical or horizontal
		l15.light = 0 #either green or red
		l15.position = [3, 34]
		
		l16 = Traffic_Lights()
		l16.direction = 1 #either vertical or horizontal
		l16.light = 0 #either green or red
		l16.position = [2, 35]
		
		l17 = Traffic_Lights()
		l17.direction = 0 #either vertical or horizontal
		l17.light = 0 #either green or red
		l17.position = [3, 67]
		
		l18 = Traffic_Lights()
		l18.direction = 1 #either vertical or horizontal
		l18.light = 0 #either green or red
		l18.position = [3, 66]
		
		l19 = Traffic_Lights()
		l19.direction = 0 #either vertical or horizontal
		l19.light = 0 #either green or red
		l19.position = [2, 66]
		
		l20 = Traffic_Lights()
		l20.direction = 0 #either vertical or horizontal
		l20.light = 0 #either green or red
		l20.position = [35, 67]
		
		l21 = Traffic_Lights()
		l21.direction = 1 #either vertical or horizontal
		l21.light = 0 #either green or red
		l21.position = [35, 66]
		
		l22 = Traffic_Lights()
		l22.direction = 0 #either vertical or horizontal
		l22.light = 0 #either green or red
		l22.position = [34, 66]
		
		l23 = Traffic_Lights()
		l23.direction = 1 #either vertical or horizontal
		l23.light = 0 #either green or red
		l23.position = [67, 66]
		
		l24 = Traffic_Lights()
		l24.direction = 0 #either vertical or horizontal
		l24.light = 0 #either green or red
		l24.position = [66, 66]
		
		l25 = Traffic_Lights()
		l25.direction = 1 #either vertical or horizontal
		l25.light = 0 #either green or red
		l25.position = [66, 67]
		
		l26 = Traffic_Lights()
		l26.direction = 1 #either vertical or horizontal
		l26.light = 0 #either green or red
		l26.position = [67, 34]
		
		l27 = Traffic_Lights()
		l27.direction = 0 #either vertical or horizontal
		l27.light = 0 #either green or red
		l27.position = [66, 34]
		
		l28 = Traffic_Lights()
		l28.direction = 1 #either vertical or horizontal
		l28.light = 0 #either green or red
		l28.position = [66, 35]

		self.intersection_list.append(i1)
		self.intersection_list.append(i2)
		self.intersection_list.append(i3)
		self.intersection_list.append(i4)
		self.intersection_list.append(i5)
		self.intersection_list.append(i6)
		self.intersection_list.append(i7)
		self.intersection_list.append(i8)
		self.intersection_list.append(i9)

		self.traffic_light_object_list.append(l1)
		self.traffic_light_object_list.append(l2)
		self.traffic_light_object_list.append(l3)
		self.traffic_light_object_list.append(l4)
		self.traffic_light_object_list.append(l5)
		self.traffic_light_object_list.append(l6)
		self.traffic_light_object_list.append(l7)
		self.traffic_light_object_list.append(l8)
		self.traffic_light_object_list.append(l9)
		self.traffic_light_object_list.append(l10)
		self.traffic_light_object_list.append(l11)
		self.traffic_light_object_list.append(l12)
		self.traffic_light_object_list.append(l13)
		self.traffic_light_object_list.append(l14)
		self.traffic_light_object_list.append(l15)
		self.traffic_light_object_list.append(l16)
		self.traffic_light_object_list.append(l17)
		self.traffic_light_object_list.append(l18)
		self.traffic_light_object_list.append(l19)
		self.traffic_light_object_list.append(l20)
		self.traffic_light_object_list.append(l21)
		self.traffic_light_object_list.append(l22)
		self.traffic_light_object_list.append(l23)
		self.traffic_light_object_list.append(l24)
		self.traffic_light_object_list.append(l25)
		self.traffic_light_object_list.append(l26)
		self.traffic_light_object_list.append(l27)
		self.traffic_light_object_list.append(l28)
	

	#manage traffic light colors
	def manage_traffic_lights(self):
		green = (0,255,0) # RGB code
		red   = (255,0,0) # RGB code
		
		self.time += 2
		print('Time: '+str(float(self.time/3600))+' hr')		
		
		# Evaluating the number of cars reach the destination
		for car in self.car_reach_destination_list:
			if car.position in destinations:
				index = destinations.index(car.position)
				match = set([car.departure_pt,index]) == set([0,1]) or set([car.departure_pt,index]) == set([2,3]) # to see if departure and destination match
			#print(match)
			if match: 
				self.reach_destination += 1 

		print('Throughtput: ' + str(self.reach_destination/float(self.time/3600)))	
		self.car_reach_destination_list.clear()

		
		for j in self.intersection_list:
			j.choose_action()
			#print(j.action)

		self.traffic_lights_list.clear()
		#Acting accordingly
		# light 1~4 (intersection 1)
		if self.intersection_list[0].action == 1:
			self.intersection_list[0].phase = (self.intersection_list[0].phase+1)%4
		elif self.intersection_list[0].action == 0:
			self.intersection_list[0].phase = self.intersection_list[0].phase

		if self.intersection_list[0].phase == 0:
			self.traffic_lights_list.append(green)
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(red)
			
			self.traffic_light_object_list[0].light = 1
			self.traffic_light_object_list[1].light = 0
			self.traffic_light_object_list[2].light = 0
			self.traffic_light_object_list[3].light = 0
		elif self.intersection_list[0].phase == 1:
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(green)
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(red)
			
			self.traffic_light_object_list[0].light = 0
			self.traffic_light_object_list[1].light = 1
			self.traffic_light_object_list[2].light = 0
			self.traffic_light_object_list[3].light = 0
		elif self.intersection_list[0].phase == 2:
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(green)
			self.traffic_lights_list.append(red)
			
			self.traffic_light_object_list[0].light = 0
			self.traffic_light_object_list[1].light = 0
			self.traffic_light_object_list[2].light = 1
			self.traffic_light_object_list[3].light = 0
		elif self.intersection_list[0].phase == 3: 
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(red)
			self.traffic_lights_list.append(green)
			
			self.traffic_light_object_list[0].light = 0
			self.traffic_light_object_list[1].light = 0
			self.traffic_light_object_list[2].light = 0
			self.traffic_light_object_list[3].light = 1
		
		# light 5~28 (intersection 2~9)
		for j in range(1,9):
				if self.intersection_list[j].action == 1:
					self.intersection_list[j].phase = (self.intersection_list[j].phase+1)%3
				elif self.intersection_list[j].action ==0:
					self.intersection_list[j].phase = self.intersection_list[j].phase

				if self.intersection_list[j].phase == 0:
					self.traffic_lights_list.append(green)
					self.traffic_lights_list.append(red)
					self.traffic_lights_list.append(red)
					
					self.traffic_light_object_list[3*(j-1)+4].light = 1
					self.traffic_light_object_list[3*(j-1)+5].light = 0
					self.traffic_light_object_list[3*(j-1)+6].light = 0
				elif self.intersection_list[j].phase == 1:
					self.traffic_lights_list.append(red)
					self.traffic_lights_list.append(green)
					self.traffic_lights_list.append(red)
					
					self.traffic_light_object_list[3*(j-1)+4].light = 0
					self.traffic_light_object_list[3*(j-1)+5].light = 1
					self.traffic_light_object_list[3*(j-1)+6].light = 0
				elif self.intersection_list[j].phase == 2:
					self.traffic_lights_list.append(red)
					self.traffic_lights_list.append(red)
					self.traffic_lights_list.append(green)
					
					self.traffic_light_object_list[3*(j-1)+4].light = 0
					self.traffic_light_object_list[3*(j-1)+5].light = 0
					self.traffic_light_object_list[3*(j-1)+6].light = 1
					

		for car in self.car_list:
			# Collision Detection
			# create a count dict that will store the count of the duplicate car's position in the dictionary
			self.count_car_duplicate_position.clear()
			count = self.count_car_duplicate_position.get(int(str(car.map[0])+'1'+str(car.map[1])))
			if count == None:
				self.count_car_duplicate_position.update({int(str(car.map[0])+'1'+str(car.map[1])) : 1})
			else:
				self.count_car_duplicate_position.update({int(str(car.map[0])+'1'+str(car.map[1])) : count+1})
				self.num_of_collisions += 1 
		

			# Evaluating red light violation
			# put car object in check_car_red_light_list if car is at intersection and the traffic light is red
			self.check_red_light_violation_list.clear()
			
			#intersection 1 (light 1~4)
			if (car.map[1]==35 and car.map[0]==36 and self.traffic_light_object_list[0].light==0) or (car.map[0]==35 and car.map[1]==33 and self.traffic_light_object_list[1].light==0) or (car.map[1]==34 and car.map[0]==33 and self.traffic_light_object_list[2].light==0) or (car.map[0]==34 and car.map[1]==36 and self.traffic_light_object_list[3].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 2 (light 5~7)
			elif (car.map[1]==3 and car.map[0]==68 and self.traffic_light_object_list[4].light==0) or (car.map[1]==2 and car.map[0]==65 and self.traffic_light_object_list[5].light==0) or (car.map[0]==66 and car.map[1]==4 and self.traffic_light_object_list[6].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 3 (light 8~10)
			elif (car.map[1]==3 and car.map[0]==36 and self.traffic_light_object_list[7].light==0) or (car.map[1]==2 and car.map[0]==33 and self.traffic_light_object_list[8].light==0) or (car.map[0]==34 and car.map[1]==4 and self.traffic_light_object_list[9].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 4 (light 11~13)
			elif (car.map[1]==3 and car.map[0]==4 and self.traffic_light_object_list[10].light==0) or (car.map[0]==3 and car.map[1]==1 and self.traffic_light_object_list[11].light==0) or (car.map[0]==2 and car.map[1]==4 and self.traffic_light_object_list[12].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 5 (light 14~16)
			elif (car.map[1]==35 and car.map[0]==4 and self.traffic_light_object_list[13].light==0) or (car.map[0]==3 and car.map[1]==33 and self.traffic_light_object_list[14].light==0) or (car.map[0]==2 and car.map[1]==36 and self.traffic_light_object_list[15].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 6 (light 17~19)
			elif (car.map[1]==67 and car.map[0]==4 and self.traffic_light_object_list[16].light==0) or (car.map[0]==3 and car.map[1]==65 and self.traffic_light_object_list[17].light==0) or (car.map[1]==66 and car.map[0]==1 and self.traffic_light_object_list[18].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 7 (light 20~22)
			elif (car.map[1]==67 and car.map[0]==36 and self.traffic_light_object_list[19].light==0) or (car.map[0]==35 and car.map[1]==65 and self.traffic_light_object_list[20].light==0) or (car.map[1]==66 and car.map[0]==33 and self.traffic_light_object_list[21].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 8 (light 23~25)
			elif (car.map[0]==67 and car.map[1]==65 and self.traffic_light_object_list[22].light==0) or (car.map[1]==66 and car.map[0]==65 and self.traffic_light_object_list[23].light==0) or (car.map[0]==66 and car.map[1]==68 and self.traffic_light_object_list[24].light==0):
				self.check_red_light_violation_list.append(car)
			#intersection 9 (light 26~28)
			elif (car.map[0]==67 and car.map[1]==33 and self.traffic_light_object_list[25].light==0) or (car.map[1]==34 and car.map[0]==65 and self.traffic_light_object_list[26].light==0) or (car.map[0]==66 and car.map[1]==36 and self.traffic_light_object_list[27].light==0):
				self.check_red_light_violation_list.append(car)
		
		#print('the num of collisions: '+str(self.num_of_collisions))
		
		# Update map
		for traffic_light_object in self.traffic_light_object_list:
			self.map[traffic_light_object.position[0]][traffic_light_object.position[1]] = traffic_light_object #traffic light 


		
	def manage_traffic_lights_step(self):
		# Evaluating red light violation
		# check the car's velocity to see if it ran a red light
		for car in self.check_red_light_violation_list:
			if car.velocity !=0:  # Not stop at the intersection
				self.num_of_red_light_violations += 1
		#print('the num of red-light violations: '+str(self.num_of_red_light_violations)+'\n')				
		

	#update traffic using car_list and traffic_light_list
	def render(self,dt):
		training = True#False#False#
		if self.viewer is None:
			self.viewer = Viewer(self.car_list, self.traffic_lights_list)
		if self.tools is None:
			self.tools = Tools()
		self.manage_traffic_lights()
		self.manage_cars(training)
		self.manage_traffic_lights_step()
		self.viewer.update(dt)

#This class is used to draw the whole traffic system: cars, lights, roads.
#Lines and squares are used to represent roads and cars respectively. Traffic lights are simplified as lines also.
class Viewer(pyglet.window.Window):
	def __init__(self, car_list, traffic_lights_list):
		super().__init__(width=700, height=700, resizable=False, caption='Traffic', vsync=False)
		pyglet.gl.glClearColor(0.8, 0.8, 0.8, 1) #background light
		self.batch = pyglet.graphics.Batch() #put all roads, cars, traffic lights into one batch, and draw 
		self.car_batch = None
		self.car_list = car_list 
		self.traffic_lights_list = traffic_lights_list
		#self.map = [[None for x in range(70)] for y in range(70)]
		#coordinates of road vertices, format: point1_x, point1_y, point2_x, point2_y
		road_vertices = \
		[INIT_X - CAR_LENGTH, INIT_Y, INIT_X - CAR_LENGTH, INIT_Y + L, #1
		 INIT_X + CAR_LENGTH, INIT_Y, INIT_X + CAR_LENGTH, INIT_Y + L, #2
		 INIT_X - CAR_LENGTH, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH, INIT_Y + 2*L + 2*D, #3
		 INIT_X - CAR_LENGTH + 2*D, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH + 2*D, INIT_Y + 2*L + 2*D, #4
		 INIT_X - CAR_LENGTH, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH - L, INIT_Y + L + 2*D, #5
		 INIT_X - CAR_LENGTH, INIT_Y + L, INIT_X - CAR_LENGTH - L, INIT_Y + L, #6
		 INIT_X - CAR_LENGTH + 2*D, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH + 2*D + L, INIT_Y + L + 2*D, #7
		 INIT_X + CAR_LENGTH,   INIT_Y + L, INIT_X + CAR_LENGTH+L, INIT_Y + L,#8
		 INIT_X - CAR_LENGTH, INIT_Y, INIT_X - CAR_LENGTH-L, INIT_Y, #21
		 INIT_X - CAR_LENGTH, INIT_Y - D*2,INIT_X - CAR_LENGTH - L, INIT_Y - D*2, #22
		 INIT_X + CAR_LENGTH, INIT_Y, INIT_X + CAR_LENGTH + L, INIT_Y, #23
		 INIT_X + CAR_LENGTH, INIT_Y - 2*D, INIT_X + CAR_LENGTH + L, INIT_Y - 2*D, #24
		 INIT_X - CAR_LENGTH, INIT_Y - D*2, INIT_X + CAR_LENGTH, INIT_Y - 2*D, #patch1
		 INIT_X - CAR_LENGTH, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 2*D, #31
		 INIT_X - CAR_LENGTH, INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 4*D, #32
		 INIT_X - CAR_LENGTH + 2*D, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH + 2*D + L, INIT_Y + 2*L + 2*D, #33
		 INIT_X - CAR_LENGTH+2*D,   INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 4*D, #34
		 INIT_X - CAR_LENGTH, INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 4*D, #patch2
		 INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 4*D, #41
		 INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH-L-2*D, INIT_Y - 2*D - BAR, #42
		 INIT_X - CAR_LENGTH-L-2*D, INIT_Y - 2*D - BAR, INIT_X - CAR_LENGTH-L, INIT_Y - 2*D - BAR, #43
		 INIT_X - CAR_LENGTH-L, INIT_Y - 2*D - BAR, INIT_X - CAR_LENGTH-L, INIT_Y - 2*D, #44
		 INIT_X - CAR_LENGTH-L, INIT_Y, INIT_X - CAR_LENGTH-L, INIT_Y + L, #45
		 INIT_X - CAR_LENGTH-L, INIT_Y + L + 2*D, INIT_X - CAR_LENGTH-L, INIT_Y + 2*L + 2*D, #46
		 INIT_X + CAR_LENGTH + L, INIT_Y - 2*D, INIT_X + CAR_LENGTH + L + 2*D, INIT_Y - 2*D, #51
		 INIT_X + CAR_LENGTH + L + 2*D, INIT_Y , INIT_X + CAR_LENGTH + L + 2*D, INIT_Y + 2*2*D + 2*L + BAR, #52
		 INIT_X + CAR_LENGTH + L + 2*D, INIT_Y + 2*2*D + 2*L + BAR, INIT_X + CAR_LENGTH + L, INIT_Y + 2*2*D + 2*L + BAR, #53
		 INIT_X + CAR_LENGTH + L, INIT_Y + 2*2*D + 2*L + BAR, INIT_X + CAR_LENGTH + L, INIT_Y + 2*2*D + 2*L, #54
		 INIT_X - CAR_LENGTH+2*D+L, INIT_Y + 2*L + 2*D , INIT_X - CAR_LENGTH+2*D+L, INIT_Y + L + 2*D, #55
		 INIT_X - CAR_LENGTH+2*D+L, INIT_Y + L , INIT_X - CAR_LENGTH+2*D+L, INIT_Y, #56
		 INIT_X + CAR_LENGTH + L + 2*D,     INIT_Y - 2*D, INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y - 2*D, #61
		 INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y - 2*D, INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y, #62
		 INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y, INIT_X + CAR_LENGTH + L + 2*D, INIT_Y, #63
		 INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH-L-2*D-BAR, INIT_Y + 2*L + 4*D, #71
		 INIT_X - CAR_LENGTH-L-2*D-BAR, INIT_Y + 2*L + 4*D, INIT_X - CAR_LENGTH-L-2*D-BAR, INIT_Y + 2*L + 2*D, #72
		 INIT_X - CAR_LENGTH-L-2*D-BAR, INIT_Y + 2*L + 2*D, INIT_X - CAR_LENGTH-L-2*D, INIT_Y + 2*L + 2*D]#73
		line_num = int(len(road_vertices)/4)
		#print(line_num)
		#put lines in a batch
		for i in range(line_num):
			self.batch.add(2, pyglet.gl.GL_LINES, None,
				('v2f', [road_vertices[i*4], road_vertices[i*4+1], road_vertices[i*4+2], road_vertices[i*4+3]]),
				('c3B', (86, 10, 29)*2))
		
		#lights_num = int(len(traffic_lights_vertices))
		#print(lights_num)
		#for j in range(lights_num):
		#	light = self.batch.add(2, pyglet.gl.GL_LINES, None,
		#				('v2f', traffic_lights_vertices[j]),
		#				('c3B', self.traffic_lights_list[0]*2))
		#	self.traffic_lights_list.append(light)
		#self.traffic_lights_list[1].colors = green*2 #can be used to change traffic light light 
		
	#draw the batch
	def on_draw(self):
		self.clear()
		self.batch.draw()
		self.car_batch.draw()
		self.traffic_lights_batch.draw()
	#update info of cars and traffic lights, called at time interval defined in function: pyglet.clock.schedule_interval()
	def update(self,dt):
		car_batch = pyglet.graphics.Batch()
		traffic_lights_batch = pyglet.graphics.Batch()
		for i in range(len(self.car_list)):
			car_batch.add(4, pyglet.gl.GL_QUADS, None,
	                             ('v2f', self.car_list[i].position), 
	                             ('c3B', self.car_list[i].color*4))
		lights_num = int(len(traffic_lights_vertices))
		for j in range(lights_num):
			traffic_lights_batch.add(2, pyglet.gl.GL_LINES, None,
						('v2f', traffic_lights_vertices[j]),
						('c3B', self.traffic_lights_list[j]*2))
		self.car_batch = car_batch
		self.traffic_lights_batch = traffic_lights_batch



class Traffic_Lights(object):
	def __init__(self):
		self.direction = None #either vertical or horizontal
		self.light = None #either green or red
		self.position = []
		
class Intersection(object):
	def __init__(self,num_of_lanes):
		self.num_of_lanes = num_of_lanes # 4: crossroad, 3: t-junction
		self.action = 0
		self.phase = 0

		self._NUM_OF_STATES = 9
		#  a=0: keep the current phase, a=1: change the light to next phase
		self._ACTIONS =[0,1] 
		self.count = 0
		self.green_duration = 6 # default traffic lights duration=6
		

	def choose_action(self):
		if (self.count%(self.green_duration)) < (self.green_duration-1) :
			self.action = 0
			self.count += 1
		elif (self.count%(self.green_duration))==(self.green_duration-1) :
			self.action = 1
			self.count += 1   


if __name__ == '__main__':
	env = Traffic()
	env.create_traffic_lights()
	while True:
		pyglet.clock.schedule_interval(env.render,0.1) #1.0 is the update time interval
		pyglet.app.run()

