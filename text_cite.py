from pprint import pprint
import re
import fileinput

with open("Zotero PhD Biblio.bib") as file:
    is_video_entry = False
    video_entry_line_length = 5
    line_read_count = 0
    entry = ""

    entries = []
    for line in file:
        if is_video_entry and line_read_count < video_entry_line_length:
            line_read_count += 1
            entry += line
        elif line_read_count >= video_entry_line_length:
            entries.append(entry)
            is_video_entry = False
            line_read_count = 0
            entry = ""
        elif line.startswith("@video"):
            is_video_entry = True
            entry += line


raw_key,raw_title = entries[0].split(',')[0:2]

cite_dict = {}

for entry in entries:
    raw_key, raw_title = entry.split(',')[0:2]
    cite_key = raw_key[7:]
    title = raw_title[raw_title.find('{')+1:-1]
    director = entry[entry.find('author'):]
    director = director[director.find('{') + 1:director.find('}')]
    director = " ".join(director.split(',')[::-1]).strip()
    author = entry[entry.find('author'):]
    author = author[author.find('{') + 1:author.find('}')]
    publisher = entry[entry.find('publisher'):]
    publisher = publisher[publisher.find('{') + 1:publisher.find('}')]
    cite_dict[cite_key] = {'title':title,
                           'year':cite_key[-4:],
                           'director':director,
                           'publisher':publisher,
                           'first_cite': True,
                           'author':author,
                           'cite_key':cite_key}

with fileinput.FileInput('presidents-men.tex', inplace=True, backup='.bak') as file:
    for line in file:
        temp_line = line
        for cite_key in cite_dict.keys():
            if f"\\citetitle{{{cite_key}}}" in line:
                if cite_dict[cite_key]['first_cite']:
                    temp_line = temp_line.replace(f"\\citetitle{{{cite_key}}}",
                                                  f"\\textit{{{cite_dict[cite_key]['title']}}} ({cite_dict[cite_key]['director']}, {cite_dict[cite_key]['year']})")
                    cite_dict[cite_key]['first_cite'] = False
                else:
                    temp_line = temp_line.replace(f"\\citetitle{{{cite_key}}}",
                                                  f"\\textit{{{cite_dict[cite_key]['title']}}}")

        print(temp_line, end='')

filmography = [cite_dict[cite_key] for cite_key in cite_dict.keys() if not cite_dict[cite_key]['first_cite']]
filmography = sorted(filmography, key=lambda d: d['title'])
filmography = sorted(filmography, key=lambda d: d['author'])

with open("presidents-men.tex", "a") as tex_file:
    tex_file.write("\n\section{Filmography}\n\n")

    previous_director = ""
    for film in filmography:
        link = r"\bibitem[\citeproctext]{" + film['cite_key'] + "}\n"
        director = film['director']
        if director == previous_director:
            director = "---------"
        filmography_line = link + f"{director} \\textit{{{film['title']}}} ({film['year']}), {film['publisher']}.\n\n"
        previous_director = film['director']
        tex_file.write(filmography_line)

