This package bundles lua scripts into a single file using the require statement. It is intended to make writing scripts for Ardupilot more modular.

It is inspired by this Stack Overflow answer: https://stackoverflow.com/a/58776273


usage: 

`lua_bundler source.lua target.lua`

where: 
- source.lua is the entrypoint of the script
- target.lua is the place to save the bundled scripts
-optional -w or --workdir is the top level folder containing all the modules, if not provided then parent folder of source.lua is used.


To import a file:

`local result = require('file_to_import')`


The modules are basically functions which are called when they are first imported and stored in a struct. The result is a pointer to the location of the output of the function. I don't know if this is the way the require statement in LUA is meant to work, but it allows you to tidy up big scripts nicely into multiple smaller files.