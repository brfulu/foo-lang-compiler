import io
import string
text = ''
text = input()
result = ''
i = 0
i = 0
while i < len(text) - 1:
	result = result + text[i]
	if text[i].isalpha() and text[i + 1].isdigit():
		result = result + '#'
	if text[i].isdigit() and text[i + 1].isalpha():
		result = result + '*'
	i += 1
print(result)
