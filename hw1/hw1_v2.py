import math
import os
states1 = [0, 1, 2]
actions1 = {'a1', 'a2'}
transitions1 = {'a1': [[0.1, 0.5, 0.4], [0.3, 0.3, 0.4], [0.7, 0.1, 0.2]],
               'a2': [[0.4, 0.1, 0.5], [0.6, 0.3, 0.1], [0.2, 0.5, 0.3]]}
reward1 = {'a1': [[0.7, 0.2, 0.1], [0.5, 0.6, -0.1], [0.2, 0.8, 0.0]],
          'a2': [[0.1, 0.8, 0.1], [-0.2, 0.5, 0.7], [0.9, -0.4, 0.5]]}
discount_factor1 = 0.5
convergence_criterion1 = 0.02

class MDP():
  def __init__(self, states, actions, transitions, reward, discount_factor, convergence_criterion):
      self.states = states
      self.actions = actions
      self.transitions = transitions
      self.reward = reward
      self.discount_factor = float(discount_factor)
      self.convergence_criterion = convergence_criterion


  def value_iteration(self):
      #Initialize V arbitrarily
      V1 = {s: 0 for s  in self.states}
      iter=0
      while True:
          V = V1.copy()
          delta = 0
          iter += 1
          for s in self.states:
              V1[s] = max([ sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1] + self.discount_factor*V[s1]) for s1 in self.states]) for a in self.actions])
              delta = max(delta, abs(V1[s]-V[s]))
          print(V1)
          if delta < self.convergence_criterion * (1-self.discount_factor) / self.discount_factor:
              print ("the number of iterations :", iter)
              return V1

  def deterministic_policy_1(self, V):
      pi = {}
      max_sum=0
      
      for s in self.states:
        for a in self.actions:
          if max_sum < sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1] + self.discount_factor*V[s1]) for s1 in self.states]) :
             max_sum = sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1] + self.discount_factor*V[s1]) for s1 in self.states]);
             max_a = a
        pi[s] = max_a     
      return pi

  def value_iteration_gs(self):
      #Initialize value function as V0
      V1={s: 0 for s in self.states}
      Vd={s: 0 for s in self.states}
      iter=0
      while True:
        V = V1.copy()
        iter+=1
        for i in range(0, len(self.states)):
             V1[i]= max([   sum([ self.transitions[a][i][s1]*(self.reward[a][i][s1]) for s1 in self.states]) + self.discount_factor*sum([ self.transitions[a][i][j]*V1[j] for j in range(0,i)])
                      + self.discount_factor*sum([ self.transitions[a][i][j]*V[j] for j in range(i,len(self.states)) ])   for a in self.actions])
             Vd[i]=abs(V1[i]-V[i])
        print(V1)
        #print("vd")
        #print(Vd)
        d=0
        for j in range(0, len(self.states)):
          #print(Vd[j]*Vd[j])
          d+=Vd[j]*Vd[j]
        #print(d)
        if math.sqrt(d) < self.convergence_criterion :
           print ("the number of iterations :", iter)
           return V1

  def deterministic_policy_2(self, V):
      pi = {}
      max_sum=0
      
      for s in self.states:
        for a in self.actions:
          if max_sum < sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1]) for s1 in self.states])+ self.discount_factor*sum([ self.transitions[a][s][s1]*V[s1] for s1 in self.states]) :
             max_sum = sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1]) for s1 in self.states])+ self.discount_factor*sum([ self.transitions[a][s][s1]*V[s1] for s1 in self.states]);
             max_a = a
        pi[s] = max_a  
      return pi

  def finite_horizon(self):
    V1={s: 0 for s in self.states}
    H = 4
    for i in range(0, H):
        V = V1.copy()
        for s in self.states:
            V1[s] = max([ sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1]+V[s1] ) for s1 in self.states])  for a in self.actions])
        print(V1)
    return V1

  def deterministic_policy_3(self, V):
      pi = {}
      max_sum=0
      
      for s in self.states:
        for a in self.actions:
          if max_sum < sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1]+ V[s1] ) for s1 in self.states]) :
             max_sum = sum([ self.transitions[a][s][s1]*(self.reward[a][s][s1]+ V[s1] ) for s1 in self.states]);
             max_a = a
        pi[s] = max_a  
      return pi



mdp = MDP(states1, actions1, transitions1, reward1, discount_factor1, convergence_criterion1)


print("====================Value Iteration====================")
V = mdp.value_iteration()
print("")
print("state value function")
print("state - value")
for s in V:
    print("s",s+1, '-', V[s])

pi = mdp.deterministic_policy_1(V)
print("")
print("deteministic policy")
print("state - action")
for s in pi:
    print ("s",s+1, '-', pi[s])

print("=======================================================")
print("")
print("=============Value Iteration by Gauss-Seidel===========")
V= mdp.value_iteration_gs()
print("")
print("state value function")
print("state - value")
for s in V:
    print("s",s+1, '-', V[s])

pi = mdp.deterministic_policy_2(V)
print("")
print("deteministic policy")
print("state - action")
for s in pi:
    print ("s",s+1, '-', pi[s])

print("=======================================================")
print("")
print("===========Finite Horizon Dynamic Programming==========")
V= mdp.finite_horizon()
print("")
print("state value function")
print("state - value")
for s in V:
    print("s",s+1, '-', V[s])

pi = mdp.deterministic_policy_3(V)
print("")
print("deteministic policy")
print("state - action")
for s in pi:
    print ("s",s+1, '-', pi[s])


os.system("pause")



