import io
num = 0
num = int(input())
sum = 0
sum = 0
while num > 0:
	digit = 0
	digit = num % 10
	sum = sum + digit
	num = num // 10
result = ''
result = ''
if sum < 10:
	result = 'Suma cifara je manja od 10'
else:
	if sum == 10:
		result = 'Suma cifara je 10'
	else:
		result = 'Suma cifara je veca od 10'
print(result)
