
from main import parse
from pathlib import Path
import os
import subprocess


def test_parse():
    data = parse(Path('tests/input/main.lua'), Path('tests/input/'))

    assert len(data) == 31

def test_bundle():
    p = Path('tests/bundle.lua')
    if p.exists():
        os.remove(p)
    subprocess.run('./lua_bundler')
    
