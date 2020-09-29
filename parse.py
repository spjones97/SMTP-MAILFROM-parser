import sys

def errorMessage(error):
	print("ERROR -- " + error)
	return

def isChar(string, index):
	if (string[index].isdigit() or string[index].isalpha()):
		return True
	return False

def isSpecial(string, index):
	if (string[index].isdigit() or string[index].isalpha()):
		return False
	elif (string[index] == '<' or string[index] == '>' or string[index] == '(' or string[index] == ')' or string[index] == '['
		or string[index] == ']' or string[index] == '\\' or string[index] == '.' or string[index] == ',' or string[index] == ';'
		or string[index] == ':' or string[index] == '@' or string[index] == '"' or string[index] == ' ' or string[index] == '\t' or string[index] == '\n'):
		return True
	return False

def nullspace(string, index):
	while index < len(string):
		if (string[index] == '\t' or string[index] == ' '):
			index+=1
		else:
			return index
	return 0

def whitespace(string, index):
	if (string[index] != ' ' and string[index] != '\t'):
		return 0
	return nullspace(string, index + 1)

def element(string, index):
	if (not string[index].isalpha()):
		return 0
	while index < len(string):
		if not isChar(string, index):
			return index
		index += 1
	return 0

def domain(string, index):
	while index < len(string):
		index = element(string, index)
		if (index == 0):
			return 0
		elif (string[index] == '.'):
			index += 1
		elif not isChar(string, index) and string[index] != '>':
			return 0
		else:
			return index
	return 0

def localpart(string, index):
	if string[index] == '@':
		return 0
	while index < len(string):
		if (isSpecial(string, index)):
			return index
		else:
			index += 1
	return 0

def mailbox(string, index):
	index = localpart(string, index)
	if (index == 0):
		errorMessage("mailbox")
		return 0
	if (string[index] != '@'):
		errorMessage("mailbox")
		return 0
	index = domain(string, index + 1)
	if (index == 0):
		errorMessage("mailbox")
		return 0
	return index

def path(string, index):
	if (string[index] != '<'):
		errorMessage("path")
		return 0
	index = mailbox(string, index + 1)
	if (index == 0):
		return 0
	if (string[index] != '>'):
		errorMessage("path")
		return 0
	index = nullspace(string, index + 1)
	if (string[index] != '\n'):
		errorMessage("CLRF")
		return 0
	return index

def mailfrom(string):
	if string[0:4] != "MAIL":
		errorMessage("mail-from-cmd")
		return
	index = whitespace(string, 4)
	if (index == 0):
		errorMessage("mail-from-cmd")
		return
	if string[index:index+5] != "FROM:":
		errorMessage("mail-from-cmd")
		return
	index = nullspace(string, index + 5)
	out = path(string, index)
	if (out == 0):
		return
	else:
		print("Sender ok")
		return

while True:
	input = sys.stdin.readline()
	if input:
		sys.stdout.write(input)
		index = mailfrom(input)
	else:
		sys.exit(0)
