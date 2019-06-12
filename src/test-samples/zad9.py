

n = 0
n = int(input())
text = ''
text = input()
token = ''
result = ''
text = (text + ' ')
i = 0
i = 0
while (i < len(text)):
	if text[i].isalpha():
		token = (token + text[i])
	else:
		if (len(token) > n):
			token = token.upper()
		result = (result + token)
		result = (result + text[i])
		token = ''
	i += 1
print(result)
