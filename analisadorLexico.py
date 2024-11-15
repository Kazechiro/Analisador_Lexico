import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Define the token specifications
token_specification = [
    ('KEYWORD', r'\b(?:if|else|while|for|return|import|from|as|def|class|try|except|finally|with|lambda|yield|assert|break|continue|del|global|nonlocal|pass|raise|True|False|None|and|or|not|is|in|print)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('NUMBER', r'\b\d+(\.\d*)?\b'),
    ('STRING', r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
    ('DELIMITER', r'[\(\)\[\]\{\}\,\:\;\.\@\...]'),
    ('OPERATOR', r'[@+\-*/%&|^~<>!=]=?|//|<<|>>|\*\*|:='),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
    ('MISMATCH', r'.'),  # Catch-all for invalid characters
]

# Compile the regex patterns
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
get_token = re.compile(token_regex).match

def lex(code):
    """Lexical analyzer function"""
    line_num = 1
    line_start = 0
    tokens = []
    mo = get_token(code)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group(kind)
        column = mo.start() - line_start
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'MISMATCH':
            tokens.append(('ERROR', f"Caractere inválido '{value}'", line_num, column))
        elif kind != 'WHITESPACE':
            tokens.append((kind, value, line_num, column))
        mo = get_token(code, mo.end())
    return tokens

# Create the GUI application
def analyze_code():
    """Analyze the code entered in the text area."""
    code = code_input.get("1.0", tk.END).strip()
    if not code:
        messagebox.showwarning("Aviso", "Por favor, insira algum código para análise.")
        return

    tokens = lex(code)
    token_count = len(tokens)
    token_types = {}

    # Process token results
    for kind, _, _, _ in tokens:
        token_types[kind] = token_types.get(kind, 0) + 1

    # Display the results in the output area
    output_area.delete("1.0", tk.END)
    output_area.insert(tk.END, f"Total de tokens: {token_count}\n\n")
    output_area.insert(tk.END, "Tipos de Tokens:\n")
    for kind, count in token_types.items():
        output_area.insert(tk.END, f"{kind}: {count}\n")

    # Display each token in detail
    output_area.insert(tk.END, "\nTokens detalhados:\n")
    for kind, value, line, column in tokens:
        output_area.insert(tk.END, f"{kind} ({value}) - Linha {line}, Coluna {column}\n")

# GUI setup
root = tk.Tk()
root.title("Analisador Léxico")

# Input section
input_label = ttk.Label(root, text="Digite o código:")
input_label.pack(pady=5)

code_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15)
code_input.pack(padx=10, pady=5)

# Analyze button
analyze_button = ttk.Button(root, text="Analisar Código", command=analyze_code)
analyze_button.pack(pady=5)

# Output section
output_label = ttk.Label(root, text="Resultado:")
output_label.pack(pady=5)

output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, state=tk.NORMAL)
output_area.pack(padx=10, pady=5)

# Run the application
root.mainloop()
