import re

bundle_base = [
    'local loaded_files = {}\n',
    'local files = {}\n',
    'local require = function(name)\n',
    '    if loaded_files[name] == nil then\n',
    '        loaded_files[name] = files[name]()\n',
    '    end\n',
    '    return loaded_files[name]\n',
    'end\n',
]

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

    output = bundle_base
        
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
        f.writelines(parse(
            source, 
            source.parent if not workdir else workdir
        ))

if __name__=="__main__":
    import argparse
    from pathlib import Path
    from lua_bundler import bundle

    parser = argparse.ArgumentParser(
        prog = 'LUABundle',
        description='Bundle LUA Scripts for ArduPilot'
    )

    parser.add_argument('source', type=Path, help='Entry point LUA file')
    parser.add_argument('target', type=Path, help='Target LUA file to write bundle to')
    parser.add_argument('-w', '--workdir', required=False, type=Path, help='folder for lua files, defaults to parent folder of entry point')

    args = parser.parse_args()
    print(args)
    if not args.source or not args.target:
        parser.print_help()
        exit()

    bundle(args.source, args.target, args.workdir)