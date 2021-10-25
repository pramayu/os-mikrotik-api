import random
import math

def random_digits():
	digits = [i for i in range(0,9)]
	random_str = ""
	for i in range(6):
		index = math.floor(random.random() * 10)
		random_str += str(digits[index])

	return random_str