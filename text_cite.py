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
    cite_dict[cite_key] = {'title':title, 'year':cite_key[-4:],'director':director}


with fileinput.FileInput('presidents-men.tex', inplace=True, backup='.bak') as file:
    for line in file:
        temp_line = line
        for cite_key in cite_dict.keys():
            if f"\\citetitle{{{cite_key}}}" in line:
                temp_line = temp_line.replace(f"\\citetitle{{{cite_key}}}", f"{cite_dict[cite_key]['title']} ({cite_dict[cite_key]['director']}, {cite_dict[cite_key]['year']})")

        print(temp_line, end='')

pprint(cite_dict)
