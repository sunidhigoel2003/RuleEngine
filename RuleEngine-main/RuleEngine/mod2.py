import re

# Define the Node structure
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type  # 'operator' or 'operand'
        self.value = value  # 'AND', 'OR' for operators, condition string for operands
        self.left = left  # Left child node
        self.right = right  # Right child node

# Tokenize the rule string using regex
def tokenize(rule_string):
    # Tokenizing parentheses, operators, and conditions
    tokens = re.findall(r"\(|\)|AND|OR|[a-zA-Z_]+ ?(?:>|<|=|<=|>=|!=) ?'?[a-zA-Z0-9_.]+'?", rule_string)
    return tokens

# Parse tokens into an AST using a recursive approach
def parse_expression(tokens):
    if not tokens:
        return None

    # Stack for operators and operands
    operand_stack = []
    operator_stack = []

    def apply_operator():
        # Pop the operator and two operands and create a new Node
        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()
        operand_stack.append(Node(type="operator", value=operator, left=left, right=right))

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "(":
            # Handle nested expressions by recursively calling parse_expression
            sub_expr, sub_len = parse_expression(tokens[i + 1:])
            operand_stack.append(sub_expr)
            i += sub_len + 1  # Skip the sub-expression length plus the closing parenthesis
        elif token == ")":
            # Stop parsing when encountering a closing parenthesis
            break
        elif token in ("AND", "OR"):
            # Handle operator precedence
            while operator_stack and operator_stack[-1] in ("AND", "OR"):
                apply_operator()
            operator_stack.append(token)
        else:
            # This is a condition/operand
            operand_stack.append(Node(type="operand", value=token))

        i += 1

    # Apply remaining operators in the stack
    while operator_stack:
        apply_operator()

    return operand_stack[0], i  # Return the root of the AST and the index processed

# Main function to convert a rule string into an AST
def create_rule(rule_string):
    tokens = tokenize(rule_string)
    ast, _ = parse_expression(tokens)
    return ast

# Helper function to print the AST
def print_ast(node, level=0):
    if node is not None:
        print('  ' * level + f"Node(type={node.type}, value={node.value})")
        if node.left:
            print_ast(node.left, level + 1)
        if node.right:
            print_ast(node.right, level + 1)

# Helper function to check if two subtrees are identical (used for merging)
def are_identical(node1, node2):
    if not node1 and not node2:
        return True
    if not node1 or not node2:
        return False
    return (node1.type == node2.type and
            node1.value == node2.value and
            are_identical(node1.left, node2.left) and
            are_identical(node1.right, node2.right))

# Helper function to merge two nodes intelligently
def merge_nodes(node1, node2):
    # If nodes are identical, return one of them
    if are_identical(node1, node2):
        return node1

    # If both nodes are operators of the same type, merge their children
    if node1.type == "operator" and node2.type == "operator":
        # If both are AND, merge their children
        if node1.value == node2.value:
            left = merge_nodes(node1.left, node2.left)
            right = merge_nodes(node1.right, node2.right)
            return Node(type="operator", value=node1.value, left=left, right=right)

        # If one is AND and the other is OR, we can combine them
        if node1.value == "AND" and node2.value == "OR":
            return Node(type="operator", value="OR", left=node1, right=node2)
        elif node1.value == "OR" and node2.value == "AND":
            return Node(type="operator", value="OR", left=node2, right=node1)

    # If both are operators but different, wrap them in an OR
    return Node(type="operator", value="OR", left=node1, right=node2)

# Function to combine multiple rules into one AST efficiently
def combine_rules(rule_asts):
    if len(rule_asts) == 1:
        return rule_asts[0]  # Only one rule, no need to combine

    combined_ast = rule_asts[0]

    for rule_ast in rule_asts[1:]:
        combined_ast = merge_nodes(combined_ast, rule_ast)  # Combine each rule AST using the merge function

    return combined_ast

# Example usage with two rules (converted to ASTs)
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
rule2 = "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)"

# Create ASTs for the individual rules
ast1 = create_rule(rule1)
ast2 = create_rule(rule2)

# Print AST for each rule
print("AST for Rule 1:")
print_ast(ast1)
print("\nAST for Rule 2:")
print_ast(ast2)

# Combine the rules
combined_ast = combine_rules([ast1, ast2])

# Print the combined AST
print("\nCombined AST:")
print_ast(combined_ast)
