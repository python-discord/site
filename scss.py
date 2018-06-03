"""
Single-file libsass wrapper that can compile SASS/SCSS files into CSS.

Usage: `python scss.py input.scss:output.css input2.scss:output2.css`
"""

import sys

import sass

if len(sys.argv) <= 1:
    print("Usage: python scss.py input.scss:output.css input2.sass:output2.sass")

for arg in sys.argv[1:]:
    input_file, output_file = arg.split(":")
    source_map_file = f"{output_file}.map"

    try:
        compiled, source_map = sass.compile(
            filename=input_file,
            output_style="compressed",
            output_filename_hint=output_file,
            source_map_filename=source_map_file
        )
    except sass.CompileError as e:
        print(f"Failed to compile {input_file}\n\n{e}")
        exit(1)
    else:
        with open(output_file, "w") as out_fh:
            out_fh.write(compiled)

        with open(source_map_file, "w") as map_fh:
            map_fh.write(source_map)

        print(f"Compiled: {input_file} -> {output_file}")
