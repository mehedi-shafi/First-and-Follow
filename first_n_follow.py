#imports
import json

#dictionaries
rules = {}
first = {}
follow = {}


def get_rules_line(operator, line):
	if '|' in line:
		for part in line.split('|'):
			get_rules_line(operator, part)
	else:
		rules[operator].append(line)


def get_first(operator, rule):
	if rule[0].islower() or rule[0] == '0':
		first[operator].append(rule[0])
	else:
		if len(first[str(rule[0])]) == 0:
			init_first(rule[0])
			init_first(operator)
		else:
			for first_term in first[rule[0]]:
				if first_term == '0':
					if len(rule[1:]) >= 1:
						get_first(operator, rule[1:])
					else:
						first[operator].append('0')
				else:
					first[operator].append(first_term)

def get_follow(operator):
	for key in rules.keys():
		for rule in rules[key]:
			if operator in rule:
				#if the searching operator is the last index or the next character is empty string and last index
				#i.e S->ABC0 if searching for C considering 0 as the empty string it is the last index.
				if rule.find(operator) == len(rule)-1 or (rule[rule.find(operator)+1] == '0' and rule.find(operator)+1 == len(rule)-1):
					if len(follow[key]) == 0:
						get_follow(key)
					else:
						follow[operator].extend(follow[key])
				else:
					index = rule.find(operator) + 1
					run = True
					while index < len(rule) and run:
						run = False
						temp = rule[index]
						if temp.islower():
							follow[operator].append(temp)
							break
						else:
							for fll in first[temp]:
								if fll == '0':
									run = True
								else:
									follow[operator].append(fll)
						index += 1
									

def init_first(char):
	for rule in rules[char]:
		get_first(char, rule)

def make_unique_list(list_val):
	return list(set(list_val))

# reading the rules from file

number_of_rules = 0
with open('input_rules.txt', "r") as f:
	for line in f:
		rules[line[0]] = []
		first[line[0]] = []
		follow[line[0]] = []
		if number_of_rules == 0:
			follow[line[0]].append('$')
		number_of_rules += 1
		get_rules_line(line[0], line[3:].replace("\n", ""))

for left in rules.keys():
	init_first(left)
for left in rules.keys():
	get_follow(left)

print()
print("Rules.")
print("----------------------------------------------")

for left in rules.keys():
	print(left + ": " + str(make_unique_list(rules[left])))

print()
print("First.")
print("----------------------------------------------")

for left in first.keys():
	print(left + ": " + str(make_unique_list(first[left])))

print()
print("Follow.")
print("----------------------------------------------")

for left in follow.keys():
	print(left + ": " + str(make_unique_list(follow[left])))