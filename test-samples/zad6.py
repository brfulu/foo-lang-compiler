import io
import math
import string
result = []
x = 0
x = int(input())
while (x >= 0):
	temp = 0
	temp = int(math.sqrt(x))
	if ((temp * temp) == x):
		result.append(x)
	x = int(input())
output = ''
i = 0
i = 0
while (i < len(result)):
	output = (output + (str(result[i]) + ', '))
	i += 1
print('Perfect squares:', output)
