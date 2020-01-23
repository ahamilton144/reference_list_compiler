import bibtexparser

# name of bib file (without extension)
bib_file = 'references_from_mendeley_example'
#name of latex file to write (without extension)
latex_file = 'reference_list_example'

# read bib file from Mendeley
with open(bib_file + '.bib', 'r', encoding='utf8') as bibtex_file:
  bib_dict = bibtexparser.load(bibtex_file).entries_dict

n_bib = len(bib_dict)
keys_bib = sorted(list(bib_dict.keys()), key=lambda v: v.upper())

# Parse lists for author, tags, title
def get_attribute(key_bib, key_attribute, parse='na'):
  attribute = bib_dict[key_bib][key_attribute].split(parse)
  return (attribute)

for i,key_bib in enumerate(keys_bib):
  if 'author' in bib_dict[key_bib]:
    bib_dict[key_bib]['author_parsed'] = get_attribute(key_bib, 'author', ' and ')
  if 'mendeley-tags' in bib_dict[key_bib]:
    bib_dict[key_bib]['tags_parsed'] = get_attribute(key_bib, 'mendeley-tags', ',')
  try:
    bib_dict[key_bib]['title'] = get_attribute(key_bib, 'title', '{')[1]
    bib_dict[key_bib]['title'] = get_attribute(key_bib, 'title', '}')[0]
  except:
    bib_dict[key_bib]['title'] = get_attribute(key_bib, 'title', '{')[0]


# Get all tags and list of keys in each tag
tags_dict = {}
no_tags = []
yes_tags = []
for i,key_bib in enumerate(keys_bib):
  try:
    tag_list = bib_dict[key_bib]['tags_parsed']
    yes_tags.append(key_bib)
    for tag in tag_list:
      if tag in tags_dict:
        tags_dict[tag].append(key_bib)
      else:
        tags_dict[tag] = [key_bib]
  except:
    no_tags.append(key_bib)
keys_tag = sorted(list(tags_dict.keys()), key=lambda v: v.upper())


### function for writing ref info to file
def write_ref(write_file, bib_dict, key_bib):
  write_file.write("\\noindent\\citep{" + bib_dict[key_bib]['ID'] + "} \n\\begin{itemize} \n")
  write_file.write("\\item{\\textit{Reference ID}:  " + bib_dict[key_bib]['ID'] + "} \n\n")
  if 'author' in bib_dict[key_bib]:
    write_file.write("\\item{\\textit{Author}:  " + bib_dict[key_bib]['author'].replace(' and ', ' $\\backslash$$\\backslash$ ') + "} \n\n")
  if 'title' in bib_dict[key_bib]:
    write_file.write("\\item{\\textit{Title}:  " + bib_dict[key_bib]['title'] + "} \n\n")
  if 'journal' in bib_dict[key_bib]:
    write_file.write("\\item{\\textit{Journal}:  " + bib_dict[key_bib]['journal'] + "} \n\n")
  if 'year' in bib_dict[key_bib]:
    write_file.write("\\item{\\textit{Year}:  " + bib_dict[key_bib]['year'] + "} \n\n")
  if 'mendeley-tags' in bib_dict[key_bib]:
    write_file.write("\\item{\\textit{Tags}:  " + bib_dict[key_bib]['mendeley-tags'].replace(',', ' $\\backslash$$\\backslash$ ') + "} \n\n")
  if 'annote' in bib_dict[key_bib]:
    write_file.write("\\item{\\textit{Notes}:  " + bib_dict[key_bib]['annote'] + "} \n\n")
  write_file.write("\\end{itemize}\medskip\n\n\n\n")


### write latex file
with open(latex_file + '.tex', 'w', encoding='utf8') as write_file:
  write_file.write("\\title{Reference notes \& tags} \n\\author{Andrew L. Hamilton \\\\\nUniversity of North Carolina at Chapel Hill \\\\\nDepartment of Environmental Sciences and Engineering} \n\\date{\\today} \n")
  write_file.write("\\documentclass[11pt]{article} \n\\usepackage[margin=1in]{geometry} \n\\usepackage{natbib} \n\\bibliographystyle{apa}  \n\n")
  write_file.write("\\begin{document} \n\\maketitle \n\n")
  write_file.write("\\noindent Compiled from " + bib_file.replace('_','\_') + ".bib \n\n")

  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("%%%%%%%%%% Sublists for each tag %%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("\\section{Tags} \n")
  for key_tag in keys_tag:
    write_file.write("\\noindent " + key_tag + "\\\\\n")
  write_file.write("\medskip\n\n\n\n")
  for i,key_tag in enumerate(keys_tag):
    write_file.write("\\subsection{Tag: " + key_tag + "} \n")
    for j,key_bib in enumerate(tags_dict[key_tag]):
      write_ref(write_file, bib_dict, key_bib)

  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("%%%%%%%%%% Tagless refs ########################## %%%%%%%%%%\n")
  write_file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
  write_file.write("\\section{Tagless} \n")
  for key_bib in no_tags:
    write_ref(write_file, bib_dict, key_bib)

  write_file.write("\n\\bibliography{" + bib_file + "} \n\\end{document}")




