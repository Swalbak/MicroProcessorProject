import pickle

with open('./user_names.pickle', 'rb') as f:
	us = pickle.load(f)

print(us)
print(us)
