import re
from pathlib import Path


def parse(source, workdir):

    required_files = {}

    def parse_require_statement(line):
        '''
            local *** = require("sdxvsvd")
            local *** = require "sdxvsvd"    
        '''
        cols = line.split('require')
        assert len(cols) <= 2
        
        rhs = cols[-1]
        
        file = rhs.strip("('')"" \n")
        if '.lua' not in file: 
            file = file + '.lua'
            
        fname = file[:-4]
        
        if file not in required_files:
            required_files[fname] = parse_file(workdir / file)
        

    def parse_file(file):
        with open(file, 'r') as f:
            source_lines = f.readlines()
            
        require_ids = [i for i, l in enumerate(source_lines) if re.search(r"\b" + re.escape('require') + r"\b", l)]

        for rlid in require_ids:
            parse_require_statement(source_lines[rlid])
        
        return source_lines

    with open('bundle_base.lua', 'r') as f:
        output = f.readlines()
        
    original_lines = parse_file(source)

    for fname, flines in required_files.items():
        output.append('')
        output.append(f"files['{fname}'] = function(...)\n")
        output = output + [f'    {l}' for l in flines]
        output[-1] = output[-1] + '\n'
        output.append('end\n')

    return output + original_lines


def bundle(source, target, workdir):
    with open(target, 'w') as f:
        f.writelines(parse(source, workdir))
    