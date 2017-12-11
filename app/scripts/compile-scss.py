"""
Compiles SCSS into CSS for inclusion in the web app.
"""
from scss import Compiler
#from scss import Scss

input_paths = [
    "../static/site.scss"
]
output_path = "../static/site.css"

for sheet in input_paths:
    compiler = Compiler()

    # load file
    with open(sheet) as input_file:
        contents = input_file.read()
        output = compiler.compile_string(contents)
        #print(output)
        # save output
        with open(output_path, mode='w') as out_file:
            out_file.write(output)

print("Done")
