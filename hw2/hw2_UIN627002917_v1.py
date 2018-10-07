from random import seed
from random import random
from random import choice


#######################################################################################


TRANSITIONS = {'a1': [[0.1, 0.5, 0.4], [0.3, 0.3, 0.4], [0.7, 0.1, 0.2]],
               'a2': [[0.4, 0.1, 0.5], [0.6, 0.3, 0.1], [0.2, 0.5, 0.3]]}
REWARD = {'a1': [[0.7, 0.2, 0.1], [0.5, 0.6, -0.1], [0.2, 0.8, 0.0]],
          'a2': [[0.1, 0.8, 0.1], [-0.2, 0.5, 0.7], [0.9, -0.4, 0.5]]}

NUM_OF_STATES = 3
ACTIONS = ['a1', 'a2']
EPSILON = 0.2
LEARNING_RATE = 0.5
DISCOUNT_FACTOR = 0.5
#K = 9
#H = 9

seed(89)

def choose_action(state,q_table):
      
      value = random()
      #print(value)

      if (value < EPSILON) : # act non-greedy or state-action have no value
         action_name = choice(ACTIONS)
         #print("non_greedy")
      else:  # act greedy
         max_q = -99999
         for a in ACTIONS :
            if max_q < q_table[a][state] :
                max_q = q_table[a][state]
                max_action = a
         action_name =  max_action
         #print("greedy")
         
      #print("Take action ", action_name)
      return action_name


def get_env_feedback(S,A):
    
    value = random()
    #print(value)
     
    if value >= 0 and value < TRANSITIONS[A][S][0] :
          S_ = 0
          R  = sum(TRANSITIONS[A][S][S1]*REWARD[A][S][S1] for S1 in range(NUM_OF_STATES))
    elif value >= TRANSITIONS[A][S][0] and value < TRANSITIONS[A][S][1] :
          S_ = 1
          R  = sum(TRANSITIONS[A][S][S1]*REWARD[A][S][S1] for S1 in range(NUM_OF_STATES))
    elif value >= TRANSITIONS[A][S][1] and value < 1 :
          S_ = 2
          R  = sum(TRANSITIONS[A][S][S1]*REWARD[A][S][S1] for S1 in range(NUM_OF_STATES))
     
    return S_, R


def Q_Learning(K,H) :
    #Initialize Q(s,a) arbitrarily
    q_table= {'a1': [0 for i in range(NUM_OF_STATES)],
            'a2': [0 for i in range(NUM_OF_STATES)]}
    #print (q_table)
    #print("       a1    a2")    
    #for i in range(NUM_OF_STATES) :
     #  print("s",i+1,"  ",q_table['a1'][i],"  ",q_table['a2'][i])
 
    for episode in range(K) :  #Repeat (for each episode)
       state = episode%3            #Initialize s
       #total_reward = 0
       print("episode:", episode+1)
       print("Start with s", state+1)

       for i in range(H) :          #Repeat (for each step of episode)
           #print("Action:",i)
           action = choose_action(state,q_table)               #Choose a according to epsilon-greedy method
           next_state, reward =get_env_feedback(state,action)  #Take action a, observe reward and next state 
           #total_reward += reward
           #print("next_state: s",next_state+1)

           q_table[action][state] = q_table[action][state] + LEARNING_RATE * ( reward + DISCOUNT_FACTOR * max(q_table[a][next_state] for a in ACTIONS) -  q_table[action][state] )
           state = next_state
           #print (q_table)
       #print("Total Reward:", total_reward)
           
    return q_table


def Sarsa(K,H) :
    #Initialize Q(s,a) arbitrarily
    q_table= {'a1': [0 for i in range(NUM_OF_STATES)],
            'a2': [0 for i in range(NUM_OF_STATES)]}
    #print (q_table)
    #print("       a1    a2")    
    #for i in range(NUM_OF_STATES) :
     #  print("s",i+1,"  ",q_table['a1'][i],"  ",q_table['a2'][i])

    for episode in range(K) :  #Repeat (for each episode)
       state = episode%3                     #Initialize s
       #total_reward = 0
       print("episode:", episode+1)
       print("Start with s", state+1)
       action = choose_action(state,q_table) #Choose a according to epsilon-greedy method

       for i in range(H) :                   #Repeat (for each step of episode)
           #print("Action:",i)
           next_state, reward =get_env_feedback(state,action)  #Take action a, observe reward and next state
           next_action = choose_action(next_state,q_table) #Choose a' from s' according to epsilon-greedy method
           #total_reward += reward
           #print("next_state: s",next_state+1)

           q_table[action][state] = q_table[action][state] + LEARNING_RATE * ( reward + DISCOUNT_FACTOR * q_table[next_action][next_state] -  q_table[action][state] )
           state = next_state
           action = next_action
           #print (q_table)
       #print("Total Reward:", total_reward)
           
    return q_table


def main():
      K = 9
      H = 9

      print("=====Q-Learning=====")
      q=Q_Learning(K,H)
      print("Q Table")
      #print(q)
      print("                 a1                    a2")    
      for i in range(NUM_OF_STATES) :
            print("s",i+1,"  ",q['a1'][i],"  ",q['a2'][i])

      print('\n')
      print("=====Sarsa=====")
      q=Sarsa(K,H)
      print("Q Table")
      #print(q)
      print("                 a1                    a2")    
      for i in range(NUM_OF_STATES) :
            print("s",i+1,"  ",q['a1'][i],"  ",q['a2'][i])

      K = 27
      H = 27
      print('\n')
      print("=====Q-Learning=====")
      q=Q_Learning(K,H)
      print("Q Table")
      #print(q)
      print("                 a1                    a2")    
      for i in range(NUM_OF_STATES) :
            print("s",i+1,"  ",q['a1'][i],"  ",q['a2'][i])

      print('\n')
      print("=====Sarsa=====")
      q=Sarsa(K,H)
      print("Q Table")
      #print(q)
      print("                 a1                    a2")    
      for i in range(NUM_OF_STATES) :
            print("s",i+1,"  ",q['a1'][i],"  ",q['a2'][i])
            


if __name__ == '__main__':
    main()





