import re

with open('webapp/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Tokenize and match brackets accurately
stack = []
i = 0
n = len(code)
line = 1
col = 1
errors = []

in_single = False
in_double = False
template_stack = []
in_block_comment = False
in_line_comment = False

# Helper to check if '/' can be a regex literal start
def can_be_regex_start(prev_token_char):
    return prev_token_char in ('(', '=', ':', ',', '[', '!', '&', '|', '?', ';', '{', '}', '~', '+', '-', '*', '%', '^', '\n', None)

prev_significant_char = None

while i < n:
    ch = code[i]
    if ch == '\n':
        line += 1
        col = 1
        in_line_comment = False
        i += 1
        continue
    
    col += 1
    
    if in_line_comment:
        i += 1
        continue
        
    if in_block_comment:
        if ch == '*' and i + 1 < n and code[i+1] == '/':
            in_block_comment = False
            i += 2
            continue
        i += 1
        continue
        
    if in_single:
        if ch == '\\':
            i += 2
            continue
        if ch == "'":
            in_single = False
            prev_significant_char = "'"
        i += 1
        continue
        
    if in_double:
        if ch == '\\':
            i += 2
            continue
        if ch == '"':
            in_double = False
            prev_significant_char = '"'
        i += 1
        continue

    if len(template_stack) > 0 and template_stack[-1] == 'TEMPLATE_LITERAL':
        if ch == '\\':
            i += 2
            continue
        if ch == '`':
            template_stack.pop()
            prev_significant_char = '`'
            i += 1
            continue
        if ch == '$' and i + 1 < n and code[i+1] == '{':
            template_stack.append('TEMPLATE_EXPR')
            stack.append(('${', line, col))
            i += 2
            prev_significant_char = '{'
            continue
        i += 1
        continue

    # Comments
    if ch == '/' and i + 1 < n and code[i+1] == '/':
        in_line_comment = True
        i += 2
        continue
    if ch == '/' and i + 1 < n and code[i+1] == '*':
        in_block_comment = True
        i += 2
        continue

    # Regex literal
    if ch == '/' and can_be_regex_start(prev_significant_char):
        # Scan until end of regex
        i += 1
        while i < n:
            if code[i] == '\\':
                i += 2
                continue
            if code[i] == '/':
                # Regex flags
                i += 1
                while i < n and code[i].isalpha():
                    i += 1
                prev_significant_char = 'regex'
                break
            if code[i] == '\n':
                break
            i += 1
        continue

    if ch == "'":
        in_single = True
        i += 1
        continue
    if ch == '"':
        in_double = True
        i += 1
        continue
    if ch == '`':
        template_stack.append('TEMPLATE_LITERAL')
        i += 1
        continue

    if not ch.isspace():
        prev_significant_char = ch

    if ch in '({[':
        stack.append((ch, line, col))
    elif ch in ')}]':
        if not stack:
            errors.append(f"Extra closing {ch} at line {line}:{col}")
        else:
            top, tl, tc = stack.pop()
            if top == '${' and ch == '}':
                if template_stack and template_stack[-1] == 'TEMPLATE_EXPR':
                    template_stack.pop()
            elif (ch == ')' and top != '(') or (ch == '}' and top != '{') or (ch == ']' and top != '['):
                errors.append(f"Mismatched {top} from line {tl}:{tc} closed by {ch} at line {line}:{col}")
    i += 1

if stack:
    for s, l, c in stack:
        errors.append(f"Unclosed {s} opened at line {l}:{c}")

print(f"Total errors found: {len(errors)}")
for err in errors[:10]:
    print(err)
