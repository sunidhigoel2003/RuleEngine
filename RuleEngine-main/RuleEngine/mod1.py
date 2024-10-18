import re

# Define the Node structure (same as before)
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

# Test case
rule1 = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
ast = create_rule(rule1)
print_ast(ast)
