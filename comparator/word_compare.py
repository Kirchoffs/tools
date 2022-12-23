import re

def process(file, spec):
    res = []
    
    with open(file) as f:
        content = f.readlines()
        line_number = 1
        for line in content:
            while len(line) > 0:
                old_len = len(line)
                for re_str, type in spec:
                    re_match = re.search(re_str, line)
                    if re_match != None:
                        if type == 'word' or type == 'symbol':
                            res.append((line[re_match.start():re_match.end()], line_number))
                        line = line[re_match.end():]
                        break
            
                if old_len == len(line):
                    print("Error")
                    exit()
            line_number += 1
            
    return res

alpha_file, beta_file = input("Input the name of two files needed to compare word by word: ").split()

re_strs = [
    ("^[{}\[\]\"\':,]", "delimiter"), 
    ("^\s+", "space"), 
    ("^\w+", "word"), 
    ("^[+-=]", "symbol"),
]

alpha_content = process(alpha_file, re_strs)
beta_content = process(beta_file, re_strs)

idx = 0
while idx < len(alpha_content) and idx < len(beta_content):
    if alpha_content[idx][0] != beta_content[idx][0]:
        print("Line number: ", alpha_content[idx][1])
        print("Compare: ", alpha_content[idx][0], beta_content[idx][0])
        break
    idx += 1