# Rule Engine with AST

## Overview

This project is a simple Rule Engine built using Flask that allows users to create, combine, and evaluate rules using an Abstract Syntax Tree (AST). The rules can be constructed using logical operators (`AND`, `OR`) and can evaluate conditions based on a provided context.

## Features

- **Create Rules**: Users can input rules using logical conditions (e.g., `age > 25`).
- **Combine Rules**: Users can combine multiple rules using `AND` or `OR` operators.
- **Evaluate Rules**: The engine evaluates the created or combined rules against a given context in JSON format.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Regular Expressions

## Project Structure

```
/rule_engine
│
├── app.py                    # Main application file
├── templates
│   └── index.html            # HTML file for the user interface
├── static
│   └── style.css             # CSS file for styling
└── requirements.txt          # List of dependencies
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SandeepaTN/Rule-Engine-with-AST.git
   cd Rule-Engine-with-AST
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000`.


## Usage

### Creating a Rule

1. Enter a rule in the provided textarea (e.g., `age > 25`).
2. Click on **Create Rule**. The created rule will be displayed below.

### Combining Rules

1. Enter multiple rules in the textarea, separating each rule with a new line.
   ```
   age > 25
   salary < 50000
   ```
2. Select a combination preference (AND/OR).
3. Click on **Combine Rules**. The combined rule will be displayed below.

### Evaluating a Rule

1. Enter the context in JSON format in the provided textarea. Example:
   ```json
   {
       "age": 30,
       "salary": 40000
   }
   ```
2. Click on **Evaluate Rule**. The result of the evaluation will be displayed.

## Code Explanation

### Node Class

The `Node` class represents a node in the Abstract Syntax Tree. Each node can either be an operator or an operand.

### Tokenization and Parsing

- **Tokenize**: The `tokenize` function breaks down a rule string into tokens using regular expressions.
- **Parse Expression**: The `parse_expression` function constructs the AST from the tokenized input.

### Rule Creation and Combination

- **create_rule**: Takes a rule string and returns the corresponding AST.
- **combine_rules**: Combines multiple ASTs based on the selected logical preference (AND/OR).

### Evaluation

The `evaluate_rule` function traverses the AST and evaluates the conditions based on the provided context.
