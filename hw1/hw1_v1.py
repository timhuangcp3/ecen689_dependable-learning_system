import math
import os
states = [0, 1, 2]
actions = {'a1', 'a2'}
transitions = {'a1': [[0.1, 0.5, 0.4], [0.3, 0.3, 0.4], [0.7, 0.1, 0.2]],
               'a2': [[0.4, 0.1, 0.5], [0.6, 0.3, 0.1], [0.2, 0.5, 0.3]]}
reward = {'a1': [[0.7, 0.2, 0.1], [0.5, 0.6, -0.1], [0.2, 0.8, 0.0]],
          'a2': [[0.1, 0.8, 0.1], [-0.2, 0.5, 0.7], [0.9, -0.4, 0.5]]}
discount_factor = 0.5
convergence_criterion = 0.02

class MDP():
  def __init__(self, transitions, reward, discount_factor):
      self.transitions = {}
      self.reward = {}
      self.discount_factor = float(discount_factor)

mdp = MDP(transitions, reward, discount_factor)

def value_iteration():
      #Initialize V arbitrarily
      V1 = {s: 0 for s  in states}
      iter=0
      while True:
          V = V1.copy()
          delta = 0
          iter += 1
          for s in states:
              V1[s] = max([ sum([ transitions[a][s][s1]*(reward[a][s][s1] + discount_factor*V[s1]) for s1 in states]) for a in actions])
              delta = max(delta, abs(V1[s]-V[s]))
          print(V1)
          if delta < convergence_criterion * (1-discount_factor) / discount_factor:
              print ("the number of iterations :", iter)
              return V1

def deterministic_policy_1(V):
      pi = {}
      max_sum=0
      
      for s in states:
        for a in actions:
          if max_sum < sum([ transitions[a][s][s1]*(reward[a][s][s1] + discount_factor*V[s1]) for s1 in states]) :
             max_sum = sum([ transitions[a][s][s1]*(reward[a][s][s1] + discount_factor*V[s1]) for s1 in states]);
             max_a = a
        pi[s] = max_a     
      return pi

def value_iteration_gs():
      #Initialize value function as V0
      V1={s: 0 for s in states}
      Vd={s: 0 for s in states}
      iter=0
      while True:
        V = V1.copy()
        iter+=1
        for i in range(0, len(states)):
             V1[i]= max([   sum([ transitions[a][i][s1]*(reward[a][i][s1]) for s1 in states]) + discount_factor*sum([ transitions[a][i][j]*V1[j] for j in range(0,i)])
                      + discount_factor*sum([ transitions[a][i][j]*V[j] for j in range(i,len(states)) ])   for a in actions])
             Vd[i]=abs(V1[i]-V[i])
        print(V1)
        #print("vd")
        #print(Vd)
        d=0
        for j in range(0, len(states)):
          #print(Vd[j]*Vd[j])
          d+=Vd[j]*Vd[j]
        #print(d)
        if math.sqrt(d) < convergence_criterion :
           print ("the number of iterations :", iter)
           return V1

def deterministic_policy_2(V):
      pi = {}
      max_sum=0
      
      for s in states:
        for a in actions:
          if max_sum < sum([ transitions[a][s][s1]*(reward[a][s][s1]) for s1 in states])+ discount_factor*sum([ transitions[a][s][s1]*V[s1] for s1 in states]) :
             max_sum = sum([ transitions[a][s][s1]*(reward[a][s][s1]) for s1 in states])+ discount_factor*sum([ transitions[a][s][s1]*V[s1] for s1 in states]);
             max_a = a
        pi[s] = max_a  
      return pi

def finite_horizon():
    V1={s: 0 for s in states}
    H = 4
    for i in range(0, H):
        V = V1.copy()
        for s in states:
            V1[s] = max([ sum([ transitions[a][s][s1]*(reward[a][s][s1]+discount_factor*V[s1] ) for s1 in states])  for a in actions])
        print(V1)
    return V1

def deterministic_policy_3(V):
      pi = {}
      max_sum=0
      
      for s in states:
        for a in actions:
          if max_sum < sum([ transitions[a][s][s1]*(reward[a][s][s1]+ discount_factor*V[s1] ) for s1 in states]) :
             max_sum = sum([ transitions[a][s][s1]*(reward[a][s][s1]+ discount_factor*V[s1] ) for s1 in states]);
             max_a = a
        pi[s] = max_a  
      return pi


print("====================Value Iteration====================")
V = value_iteration()
print("")
print("state value function")
print("state - value")
for s in V:
    print("s",s+1, '-', V[s])

pi = deterministic_policy_1(V)
print("")
print("deteministic policy")
print("state - action")
for s in pi:
    print ("s",s+1, '-', pi[s])

print("=======================================================")
print("")
print("=============Value Iteration by Gauss-Seidel===========")
V= value_iteration_gs()
print("")
print("state value function")
print("state - value")
for s in V:
    print("s",s+1, '-', V[s])

pi = deterministic_policy_2(V)
print("")
print("deteministic policy")
print("state - action")
for s in pi:
    print ("s",s+1, '-', pi[s])

print("=======================================================")
print("")
print("===========Finite Horizon Dynamic Programming==========")
V= finite_horizon()
print("")
print("state value function")
print("state - value")
for s in V:
    print("s",s+1, '-', V[s])

pi = deterministic_policy_3(V)
print("")
print("deteministic policy")
print("state - action")
for s in pi:
    print ("s",s+1, '-', pi[s])


os.system("pause")



