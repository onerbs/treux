def peek(text: str, length: int) -> str:
	if len(text) < length:
		return text
	words = text.split(' ')
	result = words.pop(0)
	if len(result) > length:
		result = result[:length]
	while len(result) < length:
		result += f' {words.pop(0)}'
	return result + '...'
