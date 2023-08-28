from customer_tools_afternoon import Customer
import numpy as np
import pandas as pd


class Supermarket:

    def __init__(self):
        self.customer_id = 0
        self.customer_list = []
        self.data = pd.DataFrame(columns=['minute', 'customer_id', 'location'])

    def opening_hours(self, time):
        for t in range(time):
            self.time = t
            self.add(np.random.randint(10))
            self.move_all()
            customer_dict = {
                'minute': [self.time for _ in self.customer_list],
                'customer_id': [customer.customer_id for customer in self.customer_list],
                'location' : [customer.history[-1] for customer in self.customer_list]
                }
            self.data = pd.concat([self.data, pd.DataFrame(customer_dict)], ignore_index = True)

        for customer in self.customer_list:
            if customer.history[-1] != 'checkout':
                customer.history.append('checkout')

    def add(self, number):
            
        for i in range(number):
            customer = Customer(self.customer_id)
            self.customer_list.append(customer)
            self.customer_id += 1

    def move_all(self):

        for customer in self.customer_list:
            customer.markov()


if __name__ == '__main__':
    supermarket = Supermarket()
    supermarket.opening_hours(20)
    print(supermarket.data)
    supermarket.data.to_csv('customer_moves_data_afternoon.csv')
