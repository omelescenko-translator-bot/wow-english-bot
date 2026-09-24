# -*- coding: utf-8 -*-
import re

with open(r'C:\PROJECTS\English_Learning_Bot\webapp\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Strip multiline comments
clean = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
# Strip singleline comments
clean = re.sub(r'//.*', '', clean)

# Strip strings
clean = re.sub(r'"(\\.|[^"\\])*"', '""', clean)
clean = re.sub(r"'(\\.|[^'\\])*'", "''", clean)
clean = re.sub(r'`(\\.|[^`\\])*`', '``', clean, flags=re.DOTALL)

# Strip regexes
clean = re.sub(r'/[^/\n]+/g', '', clean)

print('Clean parens:', clean.count('('), 'vs', clean.count(')'))
print('Clean curlies:', clean.count('{'), 'vs', clean.count('}'))
print('Clean brackets:', clean.count('['), 'vs', clean.count(']'))
