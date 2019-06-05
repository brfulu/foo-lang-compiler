import io
import math
result = []
x = 0
x = int(input())
while x >= 0:
	temp = 0
	temp = math.sqrt(x)
	if temp * temp == x:
		result.append(x)
	x = int(input())
print('Perfect squares')
i = 0
i = 0
while i < len(result):
	print(result[i])
	i += 1
