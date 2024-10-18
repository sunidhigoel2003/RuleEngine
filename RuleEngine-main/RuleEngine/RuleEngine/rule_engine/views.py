from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import create_rule, combine_rules, evaluate_rule
from .models import Node

@csrf_exempt  # Disable CSRF validation for simplicity; consider security implications for production
def create_rule_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rule_string = data.get('rule')  # Ensure this matches the key in your JSON
            
            if not rule_string:
                return JsonResponse({'error': 'Rule string is required'}, status=400)
            
            # Process the rule_string here (e.g., save to the database)
            
            return JsonResponse({'message': 'Rule created successfully'}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def combine_rules_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rules = data.get('rules')  # Expecting a list of rules
            
            if not rules or not isinstance(rules, list):
                return JsonResponse({'error': 'A list of rules is required'}, status=400)

            # Combine the rules logic here
            combined_rule = " AND ".join(rules)  # Example combining logic
            
            return JsonResponse({'combined_rule': combined_rule}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Convert the AST dictionary to Node objects
def dict_to_node(ast_dict):
    if ast_dict is None:
        return None

    # Create a Node instance from the dictionary
    node = Node(ast_dict['type'], 
                left=dict_to_node(ast_dict.get('left')), 
                right=dict_to_node(ast_dict.get('right')), 
                value=ast_dict.get('value'))  # Use 'value' if applicable

    return node

@csrf_exempt
def evaluate_rule_view(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            ast_dict = body.get('ast')  # This should be a dictionary representation of the AST
            data = body.get('data')  # Attributes dictionary
            if ast_dict is None or data is None:
                return JsonResponse({'error': 'AST and data are required'}, status=400)

            # Convert the AST dictionary to Node objects
            ast = dict_to_node(ast_dict)

            result = evaluate_rule(ast, data)  # Now passing Node object
            return JsonResponse({'result': result}, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format', 'details': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
