import io
import string
file = ''
file = input()
text = ''
text = open(file, 'r').read()
n = 0
n = int(input())
total = 0
k = 0
k = 0
while (k < n):
	k += 1
	key = ''
	key = input()
	token = ''
	counter = 0
	counter = 0
	i = 0
	i = 0
	while (i < len(text)):
		if text[i].isalpha():
			token = (token + text[i])
		else:
			if (token == key):
				counter += 1
			token = ''
		i += 1
	total = (total + counter)
	print(key, counter)
print('Total: ', total)
