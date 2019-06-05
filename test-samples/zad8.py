import io
text = ''
text = input()
result = ''
a = ''
a = 'asdsadsa'
if len(text) % 2 == 1:
	mid = 0
	mid = len(text) // 2
	result = result + text[mid]
	print(result)
	i = 0
	i = 0
	while i < mid:
		i += 1
		result = text[mid - i] + result
		result = result + text[mid + i]
		print(result)
else:
	rmid = 0
	rmid = len(text) // 2
	lmid = 0
	lmid = rmid - 1
	result = text[lmid] + text[rmid]
	print(result)
	i = 0
	i = 0
	while i < len(text) // 2 - 1:
		i += 1
		result = text[lmid - i] + result
		result = result + text[rmid + i]
		print(result)
