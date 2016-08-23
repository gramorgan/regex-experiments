class DFA:
	def __init__(self, d, q0, A):
		self.d = d
		self.A = A
		self.q0 = q0

	def accept(self, input):
		q = self.q0
		for c in input:
			ind = ord(c) - 97
			q = self.d[q][ind]

		return q in self.A


class NFA:
	def __init__(self, d, q0, A):
		self.d = d
		self.A = A
		self.q0 = q0

	def accept(self, input):
		q = self._follow_lambda([self.q0])
		for c in input:
			if not q:
				return False
			q_new = []
			ind = ord(c) - 96
			for state in q:
				q_new = q_new + self.d[state][ind]
			q = self._follow_lambda(q_new)

		return bool([x for x in q if x in self.A])

	def _follow_lambda(self, q):
		loop_again = True
		new_states = q
		while loop_again:
			tmp = []
			for state in new_states:
				tmp = tmp + self.d[state][0]
			if not tmp:
				loop_again = False
			else:
				q = q + tmp
				new_states = tmp
		return q


class Regex:
	def __init__(self, regex):
		tree = build_symbol_tree(regex)
		tree.print_tree()
		self.M = tree_to_NFA(tree)

	def test(self, input):
		return self.M.accept(input)



class Node:
	def __init__(self, symbol):
		self.symbol = symbol
		self.children = []

	def print_tree(self):
		self._print_tree(0)

	def _print_tree(self, depth):
		print " " * depth + self.symbol
		for node in self.children:
			node._print_tree(depth + 1)


def tree_to_NFA(input):
	if input.symbol == '+':
		to_return = tree_to_NFA(input.children[0])
		for i in range(1, len(input.children)):
			to_return = concat_NFA(to_return, tree_to_NFA(input.children[i]))
		return to_return
	elif input.symbol == '|':
		to_return = tree_to_NFA(input.children[0])
		for i in range(1, len(input.children)):
			to_return = union_NFA(to_return, tree_to_NFA(input.children[i]))
		return to_return
	elif input.symbol == '*':
		return kleene_NFA(tree_to_NFA(input.children[0]))
	else:
		return create_string_NFA(input.symbol)


def build_symbol_tree(input):
	node, ind = _build_symbol_tree(input)
	return node

def _build_symbol_tree(input):
	current_node = None
	i = 0
	while i < len(input):
		if input[i] == '(':
			new_node, ind = _build_symbol_tree(input[(i + 1):])
			i = ind
			if current_node != None:
				current_node.children.append(new_node)
			else:
				current_node = new_node
		elif input[i] == ')':
			return current_node, i + 1
		elif input[i] == '|':
			if current_node != None:
				new_node = Node('|')
				new_node.children = [current_node]
				current_node = new_node
			else:
				current_node = Node('|')
		elif input[i] == '*':
			if current_node != None:
				new_node = Node('*')
				if input[i - 1] == ')':
					new_node.children = [current_node]
					current_node = new_node
				else:
					new_node.children = [current_node.children[len(current_node.children) - 1]]
					current_node.children[len(current_node.children) - 1] = new_node
		else:
			if current_node == None:
				current_node = Node(input[i])
			elif current_node.symbol == '+':
				current_node.children.append(Node(input[i]))
			elif current_node.symbol == '|':
				if input[i - 1] == '|':
					new_node = Node('+')
					new_node.children.append(Node(input[i]))
					current_node.children.append(new_node)
				else:
					current_node.children[len(current_node.children) - 1].children.append(Node(input[i]))
			else:
				new_node = Node('+')
				new_node.children.append(current_node)
				new_node.children.append(Node(input[i]))
				current_node = new_node
		i += 1
	return current_node, len(input)


def create_string_NFA(input):
	d = [
		[[] for x in range(27)]
	]
	last_state = 0
	for c in input:
		ind = ord(c) - 96
		d[last_state][ind].append(last_state + 1)
		d.append([[] for x in range(27)])
		last_state += 1

	return NFA(d, 0, [last_state])


def union_NFA(M1, M2):
	inc_d2 = [[[z + len(M1.d) for z in y] for y in x] for x in M2.d]
	d = M1.d + inc_d2
	d.append([[] for x in range(27)])
	d[len(d) - 1][0] = [M1.q0, M2.q0 + len(M1.d)]
	return NFA(d, len(d) - 1, M1.A + [x + len(M1.d) for x in M2.A])


def kleene_NFA(M):
	d = M.d
	d.append([[] for x in range(27)])
	d[len(d) - 1][0] = [M.q0]
	for state in M.A:
		d[state][0].append(len(d) - 1)
	return NFA(d, len(d) - 1, [len(d) - 1])


def concat_NFA(M1, M2):
	inc_d2 = [[[z + len(M1.d) for z in y] for y in x] for x in M2.d]
	d = M1.d + inc_d2
	for state in M1.A:
		d[state][0].append(M2.q0 + len(M1.d))
	return NFA(d, M1.q0, [x + len(M1.d) for x in M2.A])


def main():
	input_regex = raw_input("Enter a regex: ")
	R = Regex(input_regex)

	while True:
		to_test = raw_input("Enter a string to test: ")
		if to_test == "X":
			break
		print R.test(to_test)


if __name__ == '__main__':
	main()
