**Markov Simulation**

In this project, the goal was a program that simulates customer behaviour in a supermarket. To achieve that, I explored the data, I calculated a probability transition matrix (PTM), I implemented a customer class, I run a Monte-Carlo-Markov-Chain (MCMC) simulation for a single customer and extended the simulation for multiple customers. The provided dataset is an observation of how the clients move in a supermarket consisted of only 4 sections (spicies, fruits, dairy and drinks) and the checkout in weekdays of a signle week. Additionally to the general PTM I found it also interesting in calcuating a PTM of the clients' movement for each time range of the day (morning, afternoon and evening) and see how a random client would behave according to these probabilities

*Technologies* : Python, Pandas, NumPy, Matplotlib, Seaborn

[EDA: Exploratory Data Analysis](https://github.com/vaggos3625/Portfolio/blob/main/Markov_Simulation_Supermarket/Class_Notes.ipynb)


[Customer Class](https://github.com/vaggos3625/Portfolio/blob/main/Markov_Simulation_Supermarket/customer_tools.py)


[Supermarket Class](https://github.com/vaggos3625/Portfolio/blob/main/Markov_Simulation_Supermarket/random_walk.py)
