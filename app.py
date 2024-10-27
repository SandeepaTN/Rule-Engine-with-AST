from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)


class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        if self.type == "operator":
            return f"({str(self.left)} {self.value} {str(self.right)})"
        else:
            return str(self.value)


def tokenize(rule):
    token_pattern = r"(\s+|AND|OR|!=|==|<=|>=|>|<|[()])|(\w+)|(\d+|'[^']*')"
    tokens = [match[0] or match[1] or match[2]
              for match in re.findall(token_pattern, rule)]
    return [token for token in tokens if token.strip()]


def parse_expression(tokens):
    if not tokens:
        return None
    token = tokens.pop(0)
    if token == '(':
        left = parse_expression(tokens)
        operator = tokens.pop(0)
        right = parse_expression(tokens)
        tokens.pop(0)  # Remove closing parenthesis
        return Node("operator", left=left, right=right, value=operator)
    elif re.match(r'^\w+$', token):  # Match variable names
        operator = tokens.pop(0)  # This should be a comparison operator
        right = tokens.pop(0)  # This should be the value being compared
        return Node("operand", value=f"{token} {operator} {right}")
    else:
        raise ValueError(f"Unexpected token: {token}")


def create_rule(rule_str):
    tokens = tokenize(rule_str)
    if not tokens:
        raise ValueError("No tokens found in the rule string.")
    return parse_expression(tokens)


def combine_rules(rules, preference='AND'):
    if not rules:
        return None
    combined = rules[0]
    for rule in rules[1:]:
        combined = Node('operator', left=combined,
                        right=rule, value=preference)
    return combined


def evaluate_rule(node, data):
    if node is None:
        return False
    if node.type == "operand":
        left_operand, operator, right_operand = node.value.split()
        left_value = data.get(left_operand.strip("'"), None)

        if left_value is None:
            return False

        right_value = int(right_operand) if right_operand.isdigit(
        ) else right_operand.strip("'")

        if operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '==':
            return left_value == right_value
        elif operator == '!=':
            return left_value != right_value
        elif operator == '>=':
            return left_value >= right_value
        elif operator == '<=':
            return left_value <= right_value

    left_result = evaluate_rule(node.left, data)
    right_result = evaluate_rule(node.right, data)
    return left_result and right_result if node.value == 'AND' else left_result or right_result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_rule', methods=['POST'])
def create():
    data = request.get_json()
    rule_str = data.get('rule')
    try:
        rule = create_rule(rule_str)
        return jsonify({"success": True, "rule": str(rule)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/combine_rules', methods=['POST'])
def combine():
    data = request.get_json()
    rules = data.get('rules', [])
    preference = data.get('preference', 'AND')
    try:
        asts = [create_rule(rule) for rule in rules]
        combined_rule = combine_rules(asts, preference)
        return jsonify({"success": True, "combined_rule": str(combined_rule)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    rule_str = data.get('rule')
    context = data.get('context')

    try:
        if not rule_str:
            return jsonify({"success": False, "error": "Rule string is empty"}), 400

        # Check if context is valid
        if not isinstance(context, dict):
            return jsonify({"success": False, "error": "Invalid context format. Must be a JSON object."}), 400

        # Create the rule from the rule string
        rule = create_rule(rule_str)

        # Log the created rule for debugging
        print(f"Created Rule AST: {rule}")

        # Evaluate the rule against the context
        result = evaluate_rule(rule, context)
        return jsonify({"success": True, "result": result}), 200

    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"}), 400


if __name__ == '__main__':
    app.run(debug=True)
