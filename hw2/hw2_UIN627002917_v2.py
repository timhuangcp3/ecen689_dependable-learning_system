import random
import numpy as np

random.seed(89)

TRANSITIONS = { 0 : [[0.1, 0.5, 0.4], [0.3, 0.3, 0.4], [0.7, 0.1, 0.2]],
                1 : [[0.4, 0.1, 0.5], [0.6, 0.3, 0.1], [0.2, 0.5, 0.3]]}
REWARD = { 0 : [[0.7, 0.2, 0.1], [0.5, 0.6, -0.1], [0.2, 0.8, 0.0]],
           1 : [[0.1, 0.8, 0.1], [-0.2, 0.5, 0.7], [0.9, -0.4, 0.5]]}

NUM_OF_STATES = 3
ACTIONS = [0, 1]
EPSILON = 0.2
LEARNING_RATE = 0.5
DISCOUNT_FACTOR = 0.5



def choose_action(state, q_table):
       if random.uniform(0,1) < EPSILON:
            return random.choice(ACTIONS)
       else:
            return np.argmax(q_table[state])


def get_env_feedback(S,A):
      value = random.uniform(0,1)
  
      if value >=0 and value<TRANSITIONS[A][S][0]:
           S_ = 0
           R  = sum (TRANSITIONS[A][S][S1]*REWARD[A][S][S1] for S1 in range(NUM_OF_STATES) )
      elif value >= TRANSITIONS[A][S][0] and value < TRANSITIONS[A][S][1]:
           S_ = 1
           R  = sum (TRANSITIONS[A][S][S1]*REWARD[A][S][S1] for S1 in range(NUM_OF_STATES) )
      elif value >= TRANSITIONS[A][S][1] and value < 1 :
           S_ = 2
           R  = sum (TRANSITIONS[A][S][S1]*REWARD[A][S][S1] for S1 in range(NUM_OF_STATES) )

      return S_,R

def Q_Learning(K,H) :
  #Initialize Q(s,a) arbitrarily
  q_matrix = [[0, 0],
              [0, 0],
              [0, 0]]

  visit    = [[0, 0],
              [0, 0],
              [0, 0]]

  for e in range(K):
      #Initiale s
      cur_pos = e%3
      
      #Repeat for each step of episode 
      for i in range (H):
          #Choose a according to epsilon-greedy method
          action = choose_action(cur_pos, q_matrix)
          # Take action a, observe r, s'
          next_state, reward = get_env_feedback(cur_pos, action)
          # update the q_matrix
          q_matrix[cur_pos][action] = q_matrix[cur_pos][action] + LEARNING_RATE *( reward +  DISCOUNT_FACTOR* max(q_matrix[next_state]) - q_matrix[cur_pos][action])
          visit[cur_pos][action] = visit[cur_pos][action] + 1
          cur_pos = next_state
      # print status
      #print("Episode ", e , " done")

  print(q_matrix)
  #print(visit)
  print("Training done...")

def Sarsa(K,H):
  #Initialize Q(s,a) arbitrarily
  q_matrix = [[0, 0],
              [0, 0],
              [0, 0]]

  visit    = [[0, 0],
              [0, 0],
              [0, 0]]

  #Repeat for each episode
  for e in range(K):
      # Initialize s
      cur_pos = e%3
      #Choose a according to epsilon-greedy method
      action = choose_action(cur_pos, q_matrix)
      
      # Repeat for each step of episode
      for i in range (H):
          #Take action a, observe r, s'
          next_state, reward = get_env_feedback(cur_pos, action)
          #Choose a' from s' according to epsilon-greedy method
          next_action = choose_action(next_state, q_matrix)
          # update the q_matrix
          q_matrix[cur_pos][action] = q_matrix[cur_pos][action] + LEARNING_RATE *( reward +  DISCOUNT_FACTOR* q_matrix[next_state][next_action] - q_matrix[cur_pos][action])
          visit[cur_pos][action] = visit[cur_pos][action] + 1      
  
          cur_pos = next_state
          action = next_action
      # print status
      #print("Episode ", e , " done")

  print(q_matrix)
  #print(visit)
  print("Training done...")




if __name__ == '__main__':
      K = 9
      H = 9

      print("=====Q-Learning=====")
      Q_Learning(K,H)

      print("=====Sarsa=====")
      Sarsa(K,H)
   

      K=27
      H=27
      print("=====Q-Learning=====")
      Q_Learning(K,H)

      print("=====Sarsa=====")
      Sarsa(K,H)


      K=3000
      H=27
      print("=====Q-Learning=====")
      Q_Learning(K,H)

      print("=====Sarsa=====")
      Sarsa(K,H)

 

