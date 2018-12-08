import numpy as np
import random
import copy
import pickle
import sys

INIT_X = 350 # position of the initial reference point 
INIT_Y = 70 
CAR_LENGTH = 9 
CAR_WIDTH = 9 
L = 30*CAR_WIDTH # length between two circles
D = CAR_LENGTH # width of the road
BAR = 2*CAR_WIDTH # distance between a circle and a square 
ORIENTATION = [[1,0],[-1,0],[0,-1],[0,1]] #orientation,[1,0]:up, [-1,0]:down, [0,-1]:left, [0,1]:right


#positions of traffic lights, format: point1_x, point1_y, point2_x, point2_y
#move into traffic light class later on
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
vertical_lights = [tl for tl in traffic_lights_vertices if tl[1] == tl[3]]
horizontal_lights = [tl for tl in traffic_lights_vertices if tl[0] == tl[2]]



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

# four destinations
destinations2 = [[INIT_X - CAR_LENGTH-L-D-D, INIT_Y - D - BAR,
				 INIT_X - CAR_LENGTH-L-D-D, INIT_Y - BAR,
				 INIT_X - CAR_LENGTH-L-D, INIT_Y - BAR,
				 INIT_X - CAR_LENGTH-L-D, INIT_Y - D - BAR],#left bottom corner
				[INIT_X + CAR_LENGTH + L+D,     INIT_Y - 2*D+ 3*2*D + 2*L + BAR -2*D,
				 INIT_X + CAR_LENGTH + L+D,     INIT_Y - 2*D+ 3*2*D + 2*L + BAR - D,
				 INIT_X + CAR_LENGTH + L + D+D, INIT_Y - 2*D+ 3*2*D + 2*L + BAR - D,
				 INIT_X + CAR_LENGTH + L + D+D, INIT_Y - 2*D+ 3*2*D + 2*L + BAR -2*D],#right top corner
				[INIT_X + CAR_LENGTH + L +BAR, INIT_Y - D - D,
				 INIT_X + CAR_LENGTH + L +BAR, INIT_Y - D,
				 INIT_X + CAR_LENGTH + L + D+BAR, INIT_Y - D,
				 INIT_X + CAR_LENGTH + L + D+BAR, INIT_Y-D- D],#right bottowm corner
				[INIT_X - CAR_LENGTH-L-D-BAR,     INIT_Y + L + 2*D + L + D ,
				 INIT_X - CAR_LENGTH-L-D-BAR,     INIT_Y + L + 2*D + L +D + D,
				 INIT_X - CAR_LENGTH-L-D-BAR+D,   INIT_Y + L + 2*D + L +D + D,
				 INIT_X - CAR_LENGTH-L-D-BAR+D,     INIT_Y + L + 2*D + L + D]]#left top corner 



# include all the info about a car
class Car(object):
	def __init__(self):
		self.position = []# position, vertices
		self.orientation = random.choice(ORIENTATION) 
		self.velocity = 0 #vel
		self.at_intersection = False 
		self.adj_intersection = None # the nearest intersection
		self.actions = []
		self.departure_pt = None # to see if a car is at destination: |car.departure_pt - destination_pt| == 1
		self.destination_pt = None # put the index of the destination
		self.destination = None #put map of destination
		self.at_destination = False
		self.map = [0,0] # [0,0] is the index in the map, use the index to update map[0][0] = True/False when car moves
		self.color = None # use different color for cars from different departures
		self.steps = 0
		self.table_index = None #to index which q-table should use
		self.intersection_id = None
		self.distance_to_destination = 0
		self.next_action = None # to put action for next step 
		self.waiting_time = 0
		self.S = None 
		self.A = None 
		self.S_prime = None
		self.A_prime = None 

	def check_orientation(self,orientation):
		if (orientation[0]==0 and abs(orientation[1])==1) or (orientation[1]==0 and abs(orientation[0])==1):
			pass
		else:
			raise Exception('orientation has incorrect format')


class Tools(object):
	# generate new cars
	def __init__(self):
		self.success = 0
		self.fail = 0
		self.flag = True
		self.need_a_car = True 
		self.current_episode = 0
		self.Trained_Q = None
		self.time = 0

	def car_generator(self, traffic_map):
		# four departures/destinations
		colors = [(204,255,153), (255,153,153), (96,96,96), (204,204,0)] #4 colors for 4 departures
		departures = [[INIT_X - CAR_LENGTH-L-D, INIT_Y - 2*D - BAR,
					   INIT_X - CAR_LENGTH-L-D, INIT_Y - D - BAR,
					   INIT_X - CAR_LENGTH-L, INIT_Y - D - BAR,
					   INIT_X - CAR_LENGTH-L, INIT_Y - 2*D - BAR],#left bottom corner
					  [INIT_X + CAR_LENGTH + L,     INIT_Y - 2*D+ 3*2*D + 2*L + BAR -D,
					   INIT_X + CAR_LENGTH + L,     INIT_Y - 2*D+ 3*2*D + 2*L + BAR,
					   INIT_X + CAR_LENGTH + L + D, INIT_Y - 2*D+ 3*2*D + 2*L + BAR,
					   INIT_X + CAR_LENGTH + L + D, INIT_Y - 2*D+ 3*2*D + 2*L + BAR-D],#right top corner
					  [INIT_X + CAR_LENGTH + L + D+BAR, INIT_Y - D,
					   INIT_X + CAR_LENGTH + L + D+BAR, INIT_Y,
					   INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y,
					   INIT_X + CAR_LENGTH + L + 2*D+BAR, INIT_Y-D],#right bottowm corner
					  [INIT_X - CAR_LENGTH-L-2*D-BAR,     INIT_Y + L + 2*D + L ,
					   INIT_X - CAR_LENGTH-L-2*D-BAR,     INIT_Y + L + 2*D + L +D,
					   INIT_X - CAR_LENGTH-L-2*D-BAR+D,   INIT_Y + L + 2*D + L +D,
					   INIT_X - CAR_LENGTH-L-2*D-BAR+D,     INIT_Y + L + 2*D + L]]#left top corner 
		#map_init = [[3,69], [66,0], [69,66], [0,3]]# [0,0] [0,1]
		map_init = [[69,3], [0,66], [66,69], [3,0]]#map for departures
		#map_end =  [[69,2], [0,67], [67,69], [2,0]]#map for destinations
		map_end =  [[0,67], [69,2], [2,0], [67,69]]
		#print(traffic_map[map_init[2][0]][map_init[2][1]])
		#car = Car()
		available_spots = [i for i in range(4) if not traffic_map[map_init[i][0]][map_init[i][1]]]

		#if not traffic_map[map_init[0][0]][map_init[0][1]]:
		if available_spots:
			place = random.choice(available_spots)
			car = Car()
			car.position = departures[place] #random.choice(departures) 
			car.departure_pt = place 
			car.orientation = ORIENTATION[place]
			car.map = map_init[place]
			traffic_map[car.map[0]][car.map[1]] = car #update traffic_map
			car.color = colors[place]
			car.table_index = place # used to index q-table
			car.destination = map_end[place]
			return car
		else:
			#print('No spots available')
			pass

	def car_move(self, car, vel, traffic_map):
		delta_x = car.orientation[1]*vel*D
		delta_y = car.orientation[0]*vel*D
		traffic_map[car.map[0]][car.map[1]] = None #update traffic_map, delete old car position
		car.map[0] = car.map[0] - car.orientation[0]*vel
		car.map[1] = car.map[1] + car.orientation[1]*vel
		for i in range(4):
			car.position[i*2] = car.position[i*2] + delta_x
			car.position[i*2+1] = car.position[i*2+1] + delta_y
		traffic_map[car.map[0]][car.map[1]] = car #update traffic_map, add new car position
		car.steps += 1
		car.velocity = vel
		#print(car.map)

	def at_intersection(self,car):
		#print('biu')
		if car.orientation[0] != 0: # going vertical
			find_lights = sorted(vertical_lights, key=lambda x: [x[1], x[0]]) #sort by y, then by x
			by_x = [tl for tl in find_lights if abs(tl[0]-car.position[0]) <= D] #shrink x #2*D
			if car.orientation[0] > 0: #going up, need to find the smallest
				nearest_light = [tl for tl in by_x if tl[1] >= car.position[car.orientation[0]+2]] #find the closest y, if car.orientation[0]=1, go up, top vertice is car.position[3], otherwise is[1] 
				if nearest_light:
					nearest_light = nearest_light[0]
				else:
					pass
					#print('no lights')
			elif car.orientation[0] < 0: #going down, need to find the largest
				nearest_light = [tl for tl in by_x if tl[1] <= car.position[car.orientation[0]+2]] #find the closest y, if car.orientation[0]=1, go up, top vertice is car.position[3], otherwise is[1] 
				if nearest_light:
					nearest_light = nearest_light[-1]
				else:
					pass
					#print('no lights')
			else:
				raise Exception('orientation error in vertical')
			if nearest_light:
				if car.position[car.orientation[0]+2] == nearest_light[1]: # #1, #3 are y coordinates, #0,#2 are x , nearest_light[1] is the y coord of the lower vertice
					car.at_intersection = True
					car.velocity = 0
				return car.at_intersection
			else:
				car.at_intersection = False # no available lights, near destination
		#car.at_intersection = True
		elif car.orientation[1] != 0: # going horizontal
			find_lights = sorted(horizontal_lights, key=lambda x: [x[0], x[1]]) #sort by x, then by y
			by_y = [tl for tl in find_lights if abs(tl[1]-car.position[1]) <= D] #shrink y
			if car.orientation[1] > 0: #going right, find the smallest
				nearest_light = [tl for tl in by_y if tl[0] >= car.position[car.orientation[1]*2+2]] #find the closest x 
				if nearest_light:
					nearest_light = nearest_light[0]
				else:
					pass
					#print('no lights')
			elif car.orientation[1] < 0: #going left, find the largest
				nearest_light = [tl for tl in by_y if tl[0] <= car.position[car.orientation[1]*2+2]] #find the closest x 
				if nearest_light:
					nearest_light = nearest_light[-1]
				else:
					pass
					#print('no lights')
			else:
				raise Exception('orientation error in horizontal')
			if nearest_light:
				if car.position[car.orientation[1]*2+2] == nearest_light[0]: # #1, #3 are y coordinates, #0,#2 are x
					car.at_intersection = True
					#print('stop')
					car.velocity = 0
				return car.at_intersection
			else:
				car.at_intersection = False # no available lights, near destination

	def adjacent_intersection(self,car):
		#only call this when at intersection
		#coords are all in global frame
		rect = [None]*4 # four vertices of current intersection, a rectangular 
		#calculate the four vertices of the rectangular
		if car.orientation[0] != 0:#going vertical
			rect[0] = [car.position[0]-D/2+car.orientation[0]*(-D/2),       car.position[1]-(D/2)+car.orientation[0]*(3*D/2)]
			rect[1] = [car.position[0]-D/2+car.orientation[0]*(-D/2),       car.position[1]-(D/2)+car.orientation[0]*(3*D/2)+(2*D)]
			rect[2] = [car.position[0]-D/2+car.orientation[0]*(-D/2)+(2*D), car.position[1]-(D/2)+car.orientation[0]*(3*D/2)+(2*D)]
			rect[3] = [car.position[0]-D/2+car.orientation[0]*(-D/2)+(2*D), car.position[1]-(D/2)+car.orientation[0]*(3*D/2)]
		elif car.orientation[1] != 0:#going horizontal
			rect[0] = [car.position[0]-D/2+car.orientation[1]*(3*D/2),       car.position[1]-D/2+car.orientation[1]*(D/2)]
			rect[1] = [car.position[0]-D/2+car.orientation[1]*(3*D/2),       car.position[1]-D/2+car.orientation[1]*(D/2)+(2*D)]
			rect[2] = [car.position[0]-D/2+car.orientation[1]*(3*D/2)+(2*D), car.position[1]-D/2+car.orientation[1]*(D/2)+(2*D)]
			rect[3] = [car.position[0]-D/2+car.orientation[1]*(3*D/2)+(2*D), car.position[1]-D/2+car.orientation[1]*(D/2)]
		else:
			raise Exception('orientation error in finding adjacent_intersection')
		rect = [[int(j) for j in i] for i in rect]
		rect = sorted(rect, key=lambda x: [x[0], x[1]])
		lights_from_rect = [rect[0]+rect[1],rect[2]+rect[3],rect[0]+rect[2],rect[1]+rect[3]]#possible lights from rect, from - to + for both vertical and horizontal lights  
		available_lights = [i for j in light for i in lights_from_rect if i == j] # find the common elements with the whole lights list
		car.adj_intersection = available_lights

	def available_actions(self, car, traffic_map_old):
		###light also needs to be a class with color, position properties, before a class is available, assume all of them are green
		green = (0, 255, 0)  # RGB code
		red = (255, 0, 0)  # RGB code
		action = []
		v = [l for l in car.adj_intersection if l[0] == l[2]] #vertical
		v = sorted(v, key=lambda x: x[0])
		h = [l for l in car.adj_intersection if l[1] == l[3]] #horizontal
		h = sorted(h, key=lambda x: x[1])
		# use the position relationship to determine which action is valid, use this method before a light class is ready to use
		#print(car.map)
		#sprint(traffic_map_old[68][3])
		if car.orientation[0] != 0:#vertical
			#print(traffic_map_old[car.map[0]-car.orientation[0]][car.map[1]].light)
			if traffic_map_old[car.map[0]-car.orientation[0]][car.map[1]].light == 1:#green:
				if car.orientation[0] > 0: #going up
					if traffic_map_old[car.map[0]-2][car.map[1]] and not traffic_map_old[car.map[0]-1][car.map[1]+1]:
						action.append('right')
					if traffic_map_old[car.map[0]-1][car.map[1]-1] and not traffic_map_old[car.map[0]-2][car.map[1]-2]:
						action.append('left')
					if traffic_map_old[car.map[0]-2][car.map[1]-1] and not traffic_map_old[car.map[0]-3][car.map[1]]: #h[-1] is the light with larger y, reference to lights11, 24, car.position[3] is top side 
						action.append('up')
				elif car.orientation[0] < 0:#going down
					#print(traffic_map_old[-car.map[0]][-car.map[1]])
					if traffic_map_old[car.map[0]+1][car.map[1]+1] and not traffic_map_old[car.map[0]+2][car.map[1]+2]:
						action.append('left')
					if traffic_map_old[car.map[0]+2][car.map[1]] and not traffic_map_old[car.map[0]+1][car.map[1]-1]:
						action.append('right')
					#traffic_map_old[car.map[0]-car.orientation[0]*2][car.map[1]-car.orientation[0]]:make sure there is a road, traffic_map_old[car.map[0]+3][car.map[1]]: to see if there is a car
					if traffic_map_old[car.map[0]+2][car.map[1]+1] and not traffic_map_old[car.map[0]+3][car.map[1]]:
						action.append('up')
				else:
					pass
					#raise Exception('No action available')
			elif traffic_map_old[car.map[0]-car.orientation[0]][car.map[1]].light == 0:#red:
				#print('red light') # light is red
				pass
			else:
				raise Exception('Unknown traffic light')
		elif car.orientation[1] != 0:#horizontal
			#print(car.map)
			if traffic_map_old[car.map[0]][car.map[1]+car.orientation[1]].light == 1:#green:
				if car.orientation[1] > 0:
					if traffic_map_old[car.map[0]-1][car.map[1]+1] and not traffic_map_old[car.map[0]-2][car.map[1]+2]:
						action.append('left')
					if traffic_map_old[car.map[0]][car.map[1]+2] and not traffic_map_old[car.map[0]+1][car.map[1]+1]:
						action.append('right')
					if traffic_map_old[car.map[0]-1][car.map[1]+2] and not traffic_map_old[car.map[0]][car.map[1]+3]: # v[-1] is the light with larger x, reference to lights10, 2, 4, 21, car.position[4]: right side
						action.append('up')
				elif car.orientation[1] < 0:
					if traffic_map_old[car.map[0]][car.map[1]-2] and not traffic_map_old[car.map[0]-1][car.map[1]-1]:
						action.append('right')
					if traffic_map_old[car.map[0]+1][car.map[1]-1] and not traffic_map_old[car.map[0]+2][car.map[1]-2]:
						action.append('left')
					if traffic_map_old[car.map[0]+1][car.map[1]-2] and not traffic_map_old[car.map[0]][car.map[1]-3]:#car.position[0]: left side
						action.append('up')
				else:
					pass
					#raise Exception('No action available')
			elif traffic_map_old[car.map[0]][car.map[1]+car.orientation[1]].light == 0:#red:
				#print('red light')
				pass
			else:
				raise Exception('Unknown traffic light')
		car.actions = action
		#print(car.actions)

	def turn(self, car, action, traffic_map):
		#print(action)
		traffic_map[car.map[0]][car.map[1]] = None #update traffic_map, delete old
		if action == 'up':
			if car.orientation[0] != 0: #vertical
				car.position = [y + car.orientation[0]*(3*D) if x % 2 == 1 else y for x,y in enumerate(car.position)] #change y coords(in odd position of the list)
				car.map[0] -= car.orientation[0]*3 #update map coords

			elif car.orientation[1] != 0: # horizontal
				car.position = [y + car.orientation[1]*(3*D) if x % 2 == 0 else y for x,y in enumerate(car.position)] #change x coords(in even position)
				car.map[1] += car.orientation[1]*3
		elif action == 'left':
			if car.orientation[0] != 0: #vertical
				car.position = [y + car.orientation[0]*(-2*D) if x % 2 == 0 else y for x,y in enumerate(car.position)] #change x coords
				car.position = [y + car.orientation[0]*(2*D) if x % 2 == 1 else y for x,y in enumerate(car.position)] #change y coords(in odd position of the list)
				car.map[1] = car.map[1] - car.orientation[0]*2
				car.map[0] = car.map[0] - car.orientation[0]*2
				car.orientation = [0, -car.orientation[0]] # change the position and then change the orientation
				
			elif car.orientation[1] != 0: # horizontal
				car.position = [y + car.orientation[1]*(2*D) if x % 2 == 0 else y for x,y in enumerate(car.position)] #change x coords
				car.position = [y + car.orientation[1]*(2*D) if x % 2 == 1 else y for x,y in enumerate(car.position)] #change y coords(in odd position of the list)
				car.map[1] = car.map[1] + car.orientation[1]*2
				car.map[0] = car.map[0] - car.orientation[1]*2
				car.orientation = [car.orientation[1],0] # change the position and then change the orientation
				
		elif action == 'right':
			if car.orientation[0] != 0: #vertical
				car.position = [y + car.orientation[0]*D if x % 2 == 0 else y for x,y in enumerate(car.position)] #change x coords
				car.position = [y + car.orientation[0]*D if x % 2 == 1 else y for x,y in enumerate(car.position)] #change y coords(in odd position of the list)
				car.map[1] = car.map[1] + car.orientation[0]*1
				car.map[0] = car.map[0] - car.orientation[0]*1
				car.orientation = [0, car.orientation[0]] # change the position and then change the orientation
				
			elif car.orientation[1] != 0: # horizontal
				car.position = [y + car.orientation[1]*(D) if x % 2 == 0 else y for x,y in enumerate(car.position)] #change x coords
				car.position = [y + car.orientation[1]*(-D) if x % 2 == 1 else y for x,y in enumerate(car.position)] #change y coords(in odd position of the list)
				car.map[1] = car.map[1] + car.orientation[1]*1
				car.map[0] = car.map[0] + car.orientation[1]*1
				car.orientation = [-car.orientation[1],0] # change the position and then change the orientation
		else:
			raise Exception('Invalid action')
		traffic_map[car.map[0]][car.map[1]] = car	#update traffic_map, add new
		car.velocity = 1 # simply means car is moving
		car.steps += 1 # not using
		#car.waiting_time = 0

	def pre_destination(self, car):
		if car.position in destinations2:
			return True
		else:
			return False

	def at_destination(self, car):
		if car.position in destinations:
			car.at_destination = True
			car.destination_pt = destinations.index(car.position)
			match = set([car.departure_pt,car.destination_pt]) == set([0,1]) or set([car.departure_pt,car.destination_pt]) == set([2,3])
			if match: #departure and destination are next to each other in the list
				self.success += 1 
			else:
				self.fail += 1
		else:
			car.at_destination = False
		#print('Success: '+str(self.success)+' Fail: '+str(self.fail))
		#print('Throughtput: ' + str(self.success/float(self.time/3600)))
		return car.at_destination


	def blocked(self, car, traffic_map_old):
		if car.orientation[0] != 0:
			#print(car.map)
			if traffic_map_old[car.map[0]-car.orientation[0]*1][car.map[1]]:
				blocked = True
			else:
				blocked = False
		elif car.orientation[1] != 0:
			if traffic_map_old[car.map[0]][car.map[1]+car.orientation[1]*1]:
				blocked = True
			else:
				blocked = False
		else:
			raise Exception('orientation error')
		return blocked

	def run_cars(self, car_list, traffic_map, car_reach_destination_list, intersection_list, tables, training):
		self.time += 2
		EPISODE = 3000 # from start to end is one episode 
		#current_episode = 0
		'''
		#generate only one car
		if self.flag:
			new_car = self.car_generator(traffic_map)
			car_list.append(new_car)
			self.flag = False
		#self.car_list[0].car_move(1)
		'''

		
		#generate cars constantly
		new_car = self.car_generator(traffic_map)
		if new_car != None:
			car_list.append(new_car)
		'''
		#generate a car only when previous car has reached destination(one car per episode)
		if self.need_a_car:
			print('Episode:'+str(self.current_episode))
			new_car = self.car_generator(traffic_map)
			if new_car != None:
				car_list.append(new_car)
				self.need_a_car = False
		else:
			pass
		'''
		
		map_old = copy.deepcopy(traffic_map)
		self.intersection_traffic(car_list, intersection_list) #update intersection traffic jam
		#1126, using sarsa
		#i = 0
		if training == True:
			if self.current_episode < EPISODE:
				for car in car_list[:]: #take a copy of car_list so that it can pop out cars that are at destinations
					#print('#'+str(i+1)+'in total'+str(len(car_list)))
					if self.at_intersection(car):
						#print('intersection')
						self.adjacent_intersection(car)
						self.available_actions(car, map_old)
						if car.actions:
							self.get_intersection_id(car)
							self.sarsa(car, traffic_map, tables)
						else:
							#pass#count waiting time
							car.waiting_time += 1 #1 # not using
						car.at_intersection = False
					else:
						#print('others')
						if self.pre_destination(car):
							self.car_move(car, 1, traffic_map)
						elif not self.blocked(car, map_old):
							self.car_move(car, 1, traffic_map)
						else:
							self.car_move(car, 0, traffic_map)
							car.waiting_time += 1#1 
					if self.at_destination(car):
						car_list.remove(car) #remove the car no matter it's at the right destination or the wrong one
						self.current_episode += 1 # when finish one, count one episode
						self.need_a_car = True
						car_reach_destination_list.append(car)
			else:
				print('saving Q tables...')
				name = 'Cars_Q_tables'
				with open(name + '.pkl', 'wb') as f:
				#with open('obj/'+ name + '.pkl', 'wb') as f:
					pickle.dump(tables, f, pickle.HIGHEST_PROTOCOL)
				sys.exit()
		else:
			# load trained Q table
			if self.flag:
				name = 'Cars_Q_tables'
				with open(name + '.pkl', 'rb') as f:
					self.Trained_Q = pickle.load(f)
				self.flag = False
			for car in car_list[:]: #take a copy of car_list so that it can pop out cars that are at destinations
					if self.at_intersection(car):
						self.adjacent_intersection(car)
						self.available_actions(car, map_old)
						if car.actions:
							self.get_intersection_id(car)
							action_to_take = self.greedy(car, self.Trained_Q, 0.0)
							self.turn(car, action_to_take, traffic_map)
						else:
							pass
						car.at_intersection = False
					else:
						if self.pre_destination(car):
							self.car_move(car, 1, traffic_map)
						elif not self.blocked(car, map_old):
							self.car_move(car, 1, traffic_map)
						else:
							self.car_move(car, 0, traffic_map)
					if self.at_destination(car):
						car_list.remove(car) #remove the car no matter it's at the right destination or the wrong one
						car_reach_destination_list.append(car)

			#i += 1

	def get_intersection_id(self, car):
		#print(car.map)
		if (car.map[1]==35 and car.map[0]>=36 and car.map[0]<=65) or (car.map[0]==35 and car.map[1]>=4 and car.map[1]<=33) or (car.map[1]==34 and car.map[0]>=4 and car.map[0]<=33) or (car.map[0]==34 and car.map[1]>=36 and car.map[1]<=65):
			car.intersection_id = 0
		elif (car.map[1]==3 and car.map[0]>=68 and car.map[0]<=69) or (car.map[1]==2 and car.map[0]>=36 and car.map[0]<=65) or (car.map[0]==66 and car.map[1]>=4 and car.map[1]<=33):
			car.intersection_id = 1
		elif (car.map[1]==3 and car.map[0]>=36 and car.map[0]<=65) or (car.map[1]==2 and car.map[0]>=4 and car.map[0]<=33) or (car.map[0]==34 and car.map[1]>=4 and car.map[1]<=33):
			car.intersection_id = 2
		elif (car.map[1]==3 and car.map[0]>=4 and car.map[0]<=33) or (car.map[0]==3 and car.map[1]>=0 and car.map[1]<=1) or (car.map[0]==2 and car.map[1]>=4 and car.map[1]<=33):
			car.intersection_id = 3
		elif (car.map[1]==35 and car.map[0]>=4 and car.map[0]<=33) or (car.map[0]==3 and car.map[1]>=4 and car.map[1]<=33) or (car.map[0]==2 and car.map[1]>=36 and car.map[1]<=65):
			car.intersection_id = 4
		elif (car.map[1]==67 and car.map[0]>=4 and car.map[0]<=33) or (car.map[0]==3 and car.map[1]>=36 and car.map[1]<=65) or (car.map[1]==66 and car.map[0]>=0 and car.map[0]<=1):
			car.intersection_id = 5
		elif (car.map[1]==67 and car.map[0]>=36 and car.map[0]<=65) or (car.map[0]==35 and car.map[1]>=36 and car.map[1]<=65) or (car.map[1]==66 and car.map[0]>=4 and car.map[0]<=33):
			car.intersection_id = 6
		elif (car.map[0]==67 and car.map[1]>=36 and car.map[1]<=65) or (car.map[1]==66 and car.map[0]>=36 and car.map[0]<=65) or (car.map[0]==66 and car.map[1]>=68 and car.map[1]<=69):
			car.intersection_id = 7
		elif (car.map[0]==67 and car.map[1]>=4 and car.map[1]<=33) or (car.map[1]==34 and car.map[0]>=36 and car.map[0]<=65) or (car.map[0]==66 and car.map[1]>=36 and car.map[1]<=65):
			car.intersection_id = 8
		else:
			raise Exception('intersection_id error')

	# cars at each lane, update each time step
	def intersection_traffic(self, car_list, intersection_list):
		for i in range(9):
			intersection_list[i].up = 0
			intersection_list[i].down = 0
			intersection_list[i].right = 0
			intersection_list[i].left = 0
		for car in car_list:
			#intersection 1 (light 1~4)
			if (car.map[1]==34 and car.map[0]>=36 and car.map[0]<=65):
				intersection_list[0].down += 1
			elif (car.map[0]==34 and car.map[1]>=4 and car.map[1]<=33):
				intersection_list[0].left += 1
			elif (car.map[1]==35 and car.map[0]>=4 and car.map[0]<=33):
				intersection_list[0].up += 1
			elif (car.map[0]==35 and car.map[1]>=36 and car.map[1]<=65):
				intersection_list[0].right += 1
			
			#intersection 2 (light 5~7)
			if (car.map[1]==2 and car.map[0]>=68 and car.map[0]<=69): 
				intersection_list[1].down += 1
			elif (car.map[1]==3 and car.map[0]>=36 and car.map[0]<=65): 
				intersection_list[1].up += 1
			elif (car.map[0]==67 and car.map[1]>=4 and car.map[1]<=33):
				intersection_list[1].right += 1
			
			#intersection 3 (light 8~10)
			if (car.map[1]==2 and car.map[0]>=36 and car.map[0]<=65): 
				intersection_list[2].down += 1
			elif (car.map[1]==3 and car.map[0]>=4 and car.map[0]<=33):
				intersection_list[2].up += 1
			elif (car.map[0]==35 and car.map[1]>=4 and car.map[1]<=33):
				intersection_list[2].right += 1

			#intersection 4 (light 11~13)
			if (car.map[1]==2 and car.map[0]>=4 and car.map[0]<=33): 
				intersection_list[3].down += 1
			elif (car.map[0]==2 and car.map[1]>=0 and car.map[1]<=1): 
				intersection_list[3].left += 1
			elif (car.map[0]==3 and car.map[1]>=4 and car.map[1]<=33):
				intersection_list[3].right += 1
				
			#intersection 5 (light 14~16)
			if (car.map[1]==34 and car.map[0]>=4 and car.map[0]<=33): 
				intersection_list[4].down += 1
			elif (car.map[0]==2 and car.map[1]>=4 and car.map[1]<=33): 
				intersection_list[4].left += 1
			elif (car.map[0]==3 and car.map[1]>=36 and car.map[1]<=65):
				intersection_list[4].right += 1
			
			#intersection 6 (light 17~19)
			if (car.map[1]==66 and car.map[0]>=4 and car.map[0]<=33): 
				intersection_list[5].down += 1
			elif (car.map[0]==2 and car.map[1]>=36 and car.map[1]<=65): 
				intersection_list[5].left += 1
			elif (car.map[1]==67 and car.map[0]>=0 and car.map[0]<=1):
				intersection_list[5].up += 1
				
			#intersection 7 (light 20~22)
			if (car.map[1]==66 and car.map[0]>=36 and car.map[0]<=65):
				intersection_list[6].down += 1
			elif (car.map[0]==34 and car.map[1]>=36 and car.map[1]<=65): 
				intersection_list[6].left += 1
			elif (car.map[1]==67 and car.map[0]>=4 and car.map[0]<=33):
				intersection_list[6].up += 1
				
			#intersection 8 (light 23~25)
			if (car.map[0]==66 and car.map[1]>=36 and car.map[1]<=65): 
				#print(car.map)
				intersection_list[7].left += 1
				#print(queue_length[22]==self.intersection_list[7].left)
			elif (car.map[1]==67 and car.map[0]>=36 and car.map[0]<=65):
				intersection_list[7].up += 1
				#print(queue_length[23]==self.intersection_list[7].up)
			elif (car.map[0]==67 and car.map[1]>=68 and car.map[1]<=69):
				intersection_list[7].right += 1
				#print(queue_length[24]==self.intersection_list[7].right)
		
			#intersection 9 (light 26~28)
			if (car.map[0]==66 and car.map[1]>=4 and car.map[1]<=33):
				intersection_list[8].left += 1
			elif (car.map[1]==35 and car.map[0]>=36 and car.map[0]<=65): 
				intersection_list[8].up += 1
			elif (car.map[0]==67 and car.map[1]>=36 and car.map[1]<=65):
				intersection_list[8].right += 1
	

	def sarsa(self, car, traffic_map, tables):
		#car.A_prime = self.greedy(car, tables) # choose action based on greedy policy
		action_to_take = self.greedy(car, tables, 0.1) # choose action based on greedy policy
		car.S_prime = str(car.intersection_id) #duplicate with the one below
		reward_waiting_time = car.waiting_time
		self.update_Q(car, reward_waiting_time, tables)

		self.turn(car, action_to_take, traffic_map)

		car.A = car.A_prime
		car.S = car.S_prime 

		if self.pre_destination(car):
			if car.orientation[0] != 0:
				if car.map[0] - car.orientation[0] == car.destination[0]:
					reward_destination = -600#-120  #-10#reward for the right destination
				else:
					reward_destination = 600#120  #wrong destination
			elif car.orientation[1] != 0:
				if car.map[1] + car.orientation[1] == car.destination[1]:
					reward_destination = -600#-120  #right
				else:
					reward_destination = 600#120 
			reward_destination 
			car.A = car.A_prime
			car.S = car.S_prime
			car.A_prime = None
			car.S_prime = None # terminal state
			self.update_Q(car, reward_destination, tables)
		else:
			pass

		
		car.waiting_time = 0


	def greedy(self, car, tables, epsi):
		#epsi = 0.1#0.2#0.3
		random_num = np.random.uniform()
		absolute = ['up','down','left','right']
		s_a_pairs = tables[car.table_index][str(car.intersection_id)] #get the s-a pairs of the car at current intersection
		if car.orientation[0] == 1:
			actions = ['up','down','left','right'] # intersection frame to car frame
		elif car.orientation[0] == -1:
			actions = ['down','up','right','left']
		elif car.orientation[1] == 1:
			actions = ['left','right','down','up']
		elif car.orientation[1] == -1:
			actions = ['right','left','up','down']
		else:
			raise Exception('error converting directions')
		if random_num >= epsi:
			#print(car.actions)
			available_index = [i for j in car.actions for i, e in enumerate(actions) if e == j ] # available car actions in intersection frame
			available_q_values = [s_a_pairs[absolute[i]] for i in available_index] #actions[i] is car.action in interaction frame
			min_actions = [actions[i] for i in available_index if s_a_pairs[absolute[i]] == min(available_q_values)]#find the least reward action
			if len(min_actions) > 1:
				A_prime = random.choice(min_actions)
			elif len(min_actions) == 1:
				A_prime = min_actions[0]
			else:
				raise Exception('greedy error')
		else:
			A_prime = random.choice(car.actions)
		car.A_prime = absolute[actions.index(A_prime)]
		#print(A_prime)
		return A_prime

	def next_intersection(self, car):
		local_car = copy.deepcopy(car) #to calculate car.map in the end of current lane
		local_car.map[0] = car.map[0] + (-car.orientation[0])*29
		local_car.map[1] = car.map[1] + ( car.orientation[1])*29
		self.get_intersection_id(local_car)
		next_intersection_id = local_car.intersection_id
		return str(next_intersection_id)


	def update_Q(self, car, rewards, tables):
		if car.A != None and car.S != None and car.S_prime != None and car.A_prime != None:#not start point
			updated_value = tables[car.table_index][car.S][car.A] + 0.3*(rewards + 0.3*tables[car.table_index][car.S_prime][car.A_prime] - tables[car.table_index][car.S][car.A]) 
			tables[car.table_index][car.S][car.A] = updated_value
		elif car.S_prime != None and car.A_prime != None and car.A == None and car.S == None: #just arrived 1st intersection
			pass
		elif car.S_prime != None and car.A_prime == None and car.A != None and car.S != None: #between intersections
			pass
		elif car.A == None and car.S == None and car.S_prime == None and car.A_prime == None: #departure point
			pass # stopped at departure point
		elif car.S_prime == None and car.A_prime == None and car.A != None and car.S != None: # end 
			tables[car.table_index][car.S][car.A] = tables[car.table_index][car.S][car.A] + 0.5*(rewards-tables[car.table_index][car.S][car.A])
		else:
			raise Exception('updating error')


