import random
import numpy as np

random.seed(10)

TRANSITIONS = { 0 : [[0.1, 0.5, 0.4], [0.3, 0.3, 0.4], [0.7, 0.1, 0.2]],
                1 : [[0.4, 0.1, 0.5], [0.6, 0.3, 0.1], [0.2, 0.5, 0.3]]}
REWARD = { 0 : [[0.7, 0.2, 0.1], [0.5, 0.6, -0.1], [0.2, 0.8, 0.0]],
           1 : [[0.1, 0.8, 0.1], [-0.2, 0.5, 0.7], [0.9, -0.4, 0.5]]}
FEATURES = { 0 : [[0, 1, 1], [1, 0, 1], [1, 1, 0]], 
             1 : [[0, 0, 1], [1, 0, 0], [0, 1, 0]] }


NUM_OF_STATES = 3
ACTIONS = [0, 1]
EPSILON = 0.1
LEARNING_RATE = 0.2
DISCOUNT_FACTOR = 0.5
LAMBDA = 0.5



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




def Linear_Gradient_Descent_Q_Lambda(K,H) :
  #Initialize Theta arbitrarily and e=0
  Theta = [1, 1, 1]
  e     = [0, 0, 0]

  visit =    [[0, 0],
              [0, 0],
              [0, 0]]

  q_matrix = [[0, 0],
              [0, 0],
              [0, 0]]

  #Repeat for each episode
  for i in range(K):
      # Initialize s
      cur_state = i%3
      print('episode',i)
      
      for a in range(len(ACTIONS)):
               q_matrix[cur_state][a] = sum(FEATURES[a][cur_state][s1] * Theta[s1] for s1 in range(NUM_OF_STATES) )
            
      # Repeat for each step of episode
      for j in range (H):
           if random.uniform(0,1) < EPSILON:
                  action = random.choice(ACTIONS)
                  e      = [0, 0, 0]
           else:
                  action =  np.argmax(q_matrix[cur_state])
                  for b in range(len(e)) :
                          e[b] = DISCOUNT_FACTOR*LAMBDA *e[b]
    
           for n in range(len(e)) :
                   if(FEATURES[action][cur_state][n] == 1) :                           
                          e[n] = e[n] + 1
           
           visit[cur_state][action] = visit[cur_state][action] + 1
           #print("state:",cur_state)
           #print("action:",action)

           #Take action a, observe r, s'
           next_state, reward = get_env_feedback(cur_state, action)

           TD_error = reward - q_matrix[cur_state][action]


           for a in range(len(ACTIONS)):
                    q_matrix[next_state][a] = sum(FEATURES[a][next_state][s1] * Theta[s1] for s1 in range(NUM_OF_STATES) )

           next_action =  np.argmax(q_matrix[next_state])
           TD_error    =  TD_error + LAMBDA*q_matrix[next_state][next_action] 
           for g in range(len(e)) :
                   Theta[g]    =  Theta[g] + LEARNING_RATE*TD_error*e[g] 

           cur_state = next_state
  print("Q(S,A)")        
  print(q_matrix)
  print("Visit")
  print(visit)


if __name__ == '__main__':
      K = 9
      H = 9
  
      print('=====Linear Gradient-Descent Q(Lambda) with Binary Features')
      Linear_Gradient_Descent_Q_Lambda(K,H)


      K=27
      H=27
 
      print('=====Linear Gradient-Descent Q(Lambda) with Binary Features')
      Linear_Gradient_Descent_Q_Lambda(K,H)

