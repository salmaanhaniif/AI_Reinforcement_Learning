import random

class Agent:
    def __init__(self, algorithm="Qlearn", alpha=0.15, gamma=0.95, epsilon=1.0, epsilonMin=0.01, epsilonDecay=0.999):
        # Q-Table
        # State to all actions pair 
        self.policy = {} # Dictionary untuk memudahkan pair jumlah state yang banyak
        self.algorithm = algorithm.lower()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonMin = epsilonMin
        self.epsilonDecay = epsilonDecay
        self.actions = ["turnLeft", "turnRight", "moveForward", "grab", "climb"]

    def getQValue(self, state, action):
        # Tambahkan 0 untuk nilai awal semua action di state
        if state not in self.policy:
            self.policy[state] = {}
            for act in self.actions:
                self.policy[state][act] = 0.0
        # Tambahkan 0 untuk nilai awal action
        if action not in self.policy[state]:
            self.policy[state][action] = 0.0
            
        return self.policy[state][action]

    def chooseAction(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            if state not in self.policy:
                self.policy[state] = {a: 0.0 for a in self.actions}
            
            qValues = self.policy[state]
            maxQ = max(qValues.values())
            bestActions = []
            for action, qVal in qValues.items():
                if qVal == maxQ:
                    bestActions.append(action)
            
            return random.choice(bestActions)

    def learn(self, state, action, reward, nextState, done, nextAction=None):
        if nextState not in self.policy:
            self.policy[nextState] = {a: 0.0 for a in self.actions}
        
        currentQ = self.getQValue(state, action)

        if done:
            # Di final state, hadiah di masa depan adalah 0
            nextQ = 0
        elif self.algorithm == "sarsa":
            nextQ = self.getQValue(nextState, nextAction)
        else: # Q-learning
            nextQ = max(self.policy[nextState].values())
        
        newQ = currentQ + self.alpha * (reward + self.gamma * nextQ - currentQ)
        self.policy[state][action] = newQ

    def updateEpsilon(self):
        if self.epsilon > self.epsilonMin:
            self.epsilon *= self.epsilonDecay

    def displayStateQValue(self, state):
        print("-" * 60)
        print(f"State: {state}")
        
        qValues = self.policy[state]
        maxQ = max(qValues.values())
        
        for action, qVal in qValues.items():
            if qVal == maxQ:
                print(f"    - {action}: {qVal:.2f}  <-- Optimal")
            else:
                print(f"    - {action}: {qVal:.2f}")

    def displayQTable(self):
        print("\n=== FINAL Q-TABLE ===")
        print(f"Ukuran Q-Table: {len(self.policy)} entri")
        
        sortedStates = sorted(self.policy.keys())

        for state in sortedStates:
            self.displayStateQValue(state)
        