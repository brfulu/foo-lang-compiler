def is_sorted(arr = []):
	result = []
	result = True
	i = 0
	i = 1
	while (i < len(arr)):
		if (arr[i] < arr[(i - 1)]):
			result = False
		i += 1
	return result
n = 0
n = int(input())
x = []
i = 0
i = 0
while (i < n):
	num = 0
	num = int(input())
	x.append(num)
	i += 1
result = []
result = is_sorted(x)
print(result)
