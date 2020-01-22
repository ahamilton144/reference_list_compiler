import numpy as np
import pandas as pd
import bibtexparser

# name of bib file (without extension)
bib_file = 'references_from_mendeley'
# read bib file from Mendeley, renamed refs.bib
with open(bib_file + '.bib', 'r') as bibtex_file:
  bib_dict = bibtexparser.load(bibtex_file).entries_dict

n_bib = len(bib_dict)
keys_bib = list(bib_dict.keys())

# Parse lists for author, tags, title
def get_attribute(key_bib, key_attribute, parse='na'):
  attribute = bib_dict[key_bib][key_attribute].split(parse)
  return (attribute)

for i,key_bib in enumerate(keys_bib):
  bib_dict[key_bib]['author_parsed'] = get_attribute(key_bib, 'author', ' and ')
  bib_dict[key_bib]['tags_parsed'] = get_attribute(key_bib, 'mendeley-tags', ',')
  bib_dict[key_bib]['title'] = get_attribute(key_bib, 'title', '{')[1]
  bib_dict[key_bib]['title'] = get_attribute(key_bib, 'title', '}')[0]

# Get all tags and list of keys in each tag
tags_dict = {}
no_tags = []
for i,key_bib in enumerate(keys_bib):
  try:
    tag_list = bib_dict[key_bib]['tags_parsed']
    for tag in tag_list:
      if tag in tags_dict:
        tags_dict[tag].append(key_bib)
      else:
        tags_dict[tag] = [key_bib]
  except:
    no_tags.append(key_bib)
keys_tag = list(tags_dict.keys())

### write latex file
with open('reference_list.tex', 'w') as write_file:
  write_file.write("\\title{Reference notes \& tags} \n\\author{Andrew L. Hamilton \\\\\nUniversity of North Carolina at Chapel Hill \\\\\nDepartment of Environmental Sciences and Engineering} \n\\date{\\today} \n")
  write_file.write("\\documentclass[11pt]{article} \n\\usepackage[margin=1in]{geometry} \n\\usepackage{natbib} \n\\bibliographystyle{apa}  \n\n")
  write_file.write("\\begin{document} \n\\maketitle \n\n")

  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("%%%%%%%%%% Full reference list with notes and tags %%%%%%%%%%\n")
  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("\\section{References \& notes} \n")
  for i,key_bib in enumerate(keys_bib):
    write_file.write("\\noindent\\citep{" + bib_dict[key_bib]['ID'] + "} \n\\begin{itemize} \n")
    write_file.write("\\item{Reference ID:  " + bib_dict[key_bib]['ID'] + "} \n\n")
    write_file.write("\\item{Authors:  " + bib_dict[key_bib]['author'] + "} \n\n")
    write_file.write("\\item{Title:  " + bib_dict[key_bib]['title'] + "} \n\n")
    write_file.write("\\item{Journal:  " + bib_dict[key_bib]['journal'] + "} \n\n")
    write_file.write("\\item{Year:  " + bib_dict[key_bib]['year'] + "} \n\n")
    write_file.write("\\item{Tags:  " + bib_dict[key_bib]['mendeley-tags'] + "} \n\n")
    write_file.write("\\item{Notes:  " + bib_dict[key_bib]['annote'] + "} \n\n")
    write_file.write("\\end{itemize}\medskip\n\n\n\n")

  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("%%%%%%%%%% Sublists for each tag %%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("\\section{Tags} \n")
  for i,key_tag in enumerate(keys_tag):
    write_file.write("\\subsection{" + key_tag + "} \n")
    for j,key_bib in enumerate(tags_dict[key_tag]):
      write_file.write("\\noindent\\citep{" + bib_dict[key_bib]['ID'] + "}:   "  + bib_dict[key_bib]['title'] + "\n\\medskip\n\n")
    write_file.write("\n\n")
  write_file.write("\n\\bibliography{" + bib_file + "} \n\\end{document}")



