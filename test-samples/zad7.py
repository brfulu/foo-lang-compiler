import io
import string
text = ''
text = input()
result = ''
result = text[0]
i = 0
i = 1
while (i < len(text)):
	if (text[(i - 1)].isalpha() and text[i].isdigit()):
		result = (result + '*')
	if (text[(i - 1)].isdigit() and text[i].isalpha()):
		result = (result + '#')
	result = (result + text[i])
	i += 1
print(result)
