# reference_list_compiler
Simple tool for compiling all references from a .bib file into a .tex file, which can be used to create a .pdf file. Pdf will list a section for each "tag", with all references using that tag.Then will list all references that have no tags. Currently set up for Mendeley, but I assume it would be straightforward to extend to other reference management software.

## Steps
- Download .bib file to working directory (In Mendeley, highlight all references you want to include, then click File -> Export)
- In `reference_list_compiler.py`, change the name of `bib_file` and `latex_file` to match the names of your .bib file you just downloaded and the .tex file you want to create, respectively. Do not include extensions in this string.
- Run `reference_list_compiler.py` in Python (I use 3.6, have not checked for backwards compatibility)
- This will create a .tex file. Compile this using your favorite Tex software (I use TeXworks, and you should also be able to use Overleaf)
- This will create a .pdf file. 
- That's it!
