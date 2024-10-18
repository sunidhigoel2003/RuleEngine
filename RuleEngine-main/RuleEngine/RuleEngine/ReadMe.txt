How to test the Functions?

Step 1: Open the terminal and run the project using the command: python manage.py runserver

Step 2.0: Open the POSTMAN Software

Step 2.1.0: Testing the create_rule function 

Step 2.1.1: Select POST Request and paste this link:  http://127.0.0.1:8000/rules/create_rule/

Step 2.1.2: Input for postman raw: 

{
    "rule": "Example rule string"
}


Step 2.2.0: Testing the combine_rules function 

Step 2.2.1: Select POST Request and paste this link:  http://127.0.0.1:8000/rules/combine_rules/

Step 2.2.2: Input for postman raw: 

{
    "rules": [
        "Rule 1",
        "Rule 2",
        "Rule 3"
    ]
}


Step 2.3.0: Testing the evaluate_rule function 

Step 2.3.1: Select POST Request and paste this link:  http://127.0.0.1:8000/rules/evaluate_rule/

Step 2.3.2: Input in postman raw: 

{
    "ast": {
        "type": "operator",
        "left": {
            "type": "operand",
            "value": "age > 30"  // This needs to be parsed correctly in the evaluate_rule
        },
        "right": {
            "type": "operand",
            "value": "department = 'Sales'"
        },
        "value": "AND"  // Specify the operator if necessary
    },
    "data": {
        "age": 35,
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
}
