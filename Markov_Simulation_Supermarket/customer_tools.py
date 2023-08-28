import numpy as np
import pandas as pd

#Transition probabilities matrix
df_Q = pd.read_csv('/home/evangelo/evangelo-leo-0/evangelos-leo/Markov-chain-simulation-master/transition-propability-matrix.csv', index_col=0)

class Customer:
    '''
    Customer class that simulates a Markov chain for one customer based
    on Markov states defined above and a transition probability matrix
    '''
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.state = 'entrance'
        self.nb_state = 1
        self.history = ['entrance']

    def __repr__(self):
        return f"The customer number {self.customer_id} is at {self.state}"

    def markov(self):
        
        if self.state != 'checkout':
            

            self.state = np.random.choice(df_Q.columns, p=df_Q.loc[self.state])
            self.history.append(self.state)

            # if next_state == 'checkout':
            #    self.state = 'checkout'
            #    self.history.append(self.state)
            #    self.nb_state += 1
            #    yield self.state

            # else:
            #    self.state = next_state
            #    self.history.append(self.state)
            #    self.nb_state += 1
            #    yield self.state
