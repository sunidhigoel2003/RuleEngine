import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }
    
def create_rule(rule_string):
    tokens = re.findall(r'\(|\)|AND|OR|[a-zA-Z_]+|[><=]|[0-9]+', rule_string)
    return build_ast(tokens).to_dict()

def build_ast(tokens):
    operators = []
    operands = []
    
    def process_operator():
        right = operands.pop()
        left = operands.pop()
        operator = operators.pop()
        operands.append(Node(node_type="operator", left=left, right=right, value=operator))
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                process_operator()
            operators.pop()  # Remove "("
        elif token in ["AND", "OR"]:
            while (operators and operators[-1] in ["AND", "OR"]):
                process_operator()
            operators.append(token)
        elif token in [">", "<", "="]:
            left_operand = operands.pop()
            right_operand = tokens[i + 1]
            i += 1
            condition = f"{left_operand.value} {token} {right_operand}"
            operands.append(Node(node_type="operand", value=condition))
        else:
            operands.append(Node(node_type="operand", value=token))
        i += 1

    while operators:
        process_operator()

    return operands[0]  # Root of the AST

def combine_rules(rules):
    # This is a placeholder for the actual AST logic
    root_node = None

    # Example rule parsing (this is just a placeholder, implement your parsing logic)
    for rule in rules:
        if root_node is None:
            # Create the root node for the first rule
            root_node = Node("operator")  # You may want to determine if it's AND/OR here
        # Parse and create nodes for each rule as needed
        # For demonstration, let's just create a simple left node
        left_node = Node("operand", value=rule)  # Replace this with your actual logic to create nodes
        if root_node.left is None:
            root_node.left = left_node
        else:
            # Handle combining further rules if needed (this is just an example)
            current = root_node
            while current.right is not None:
                current = current.right
            current.right = left_node  # Assuming you want to chain them as right children

    return root_node  # Ensure this is a Node instance


def evaluate_rule(ast_root, data):
    if ast_root.type == "operand":
        return evaluate_condition(ast_root.value, data)

    elif ast_root.type == "operator":
        left_result = evaluate_rule(ast_root.left, data)
        right_result = evaluate_rule(ast_root.right, data)
        if ast_root.value == "AND":
            return left_result and right_result
        elif ast_root.value == "OR":
            return left_result or right_result
    return False

def evaluate_condition(condition, data):
    # Condition example: "age > 30"
    field, operator, value = re.split(r'\s+', condition)
    value = int(value)  # Assuming numerical comparisons

    if field not in data:
        return False  # Invalid field in the condition
    
    # Compare data[field] with the condition
    if operator == '>':
        return data[field] > value
    elif operator == '<':
        return data[field] < value
    elif operator == '=':
        return data[field] == value
    return False
