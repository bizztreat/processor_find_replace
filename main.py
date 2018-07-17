#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import os
import csv
import json

def find_csv_files(basedir):
	filelist = []
	for dirpath, dirnames, files in os.walk(basedir):
		for f in files:
			if f.lower().endswith(".csv"):
				filelist.append(os.path.join(dirpath,f))
	return filelist

def find_nth_column_position(line,delim=",\"",n=7):
	current = 0
	global_position = 0
	while True:
		pos = line.find(delim)
		line = line[pos+len(delim):]
		global_position+=pos+len(delim)
		current+=1
		if current==n-1:
			return global_position
		else:
			continue
		

#if (not os.path.exists("/data/out/tables")): os.makedirs("/data/out/tables")
#if (not os.path.exists("in/tables")): os.makedirs("in/tables")

print("Starting processor Find & Replace")


if not os.path.exists("/data/config.json"):
	#Interactive mode
	interactive_mode = True
	print("/data/config.json not found, running in interactive debug mode")
	config_find = input("Find string [\"\"\"]: ")
	config_replacement = input("Replace with [\"\"]: ")
	config_encoding = input("Input tables encoding [utf-8]: ")
	config_tail_only = input("Replace last column only? [1]: ")
	config_no_columns = input("No. of columns [7]: ")
	if config_find=="": config_find = "\"\"\""
	if config_replacement=="": config_replacement = "\"\""
	if config_encoding=="": config_encoding = "utf-8"
	if config_tail_only=="": config_tail_only = True
	else: config_tail_only = bool(int(config_tail_only))
	if config_no_columns=="": config_no_columns = 7
	else: config_no_columns = int(config_no_columns)
	debug_mode = 1
else:
	with open("/data/config.json","r") as fid:
		config = json.load(fid)
	interactive_mode = False
	config_find = config["parameters"]["find"]
	config_replacement = config["parameters"]["replacement"]
	config_encoding = config["parameters"]["encoding"]
	debug_mode = int(config["parameters"]["debug"])
	config_tail_only = bool(int(config["parameters"]["tail_only"]))
	config_no_columns = int(config["parameters"]["column_count"])

if debug_mode:
	print("Will process following tables:")
	csv_filelist = find_csv_files("/data/in/tables")
	print("\n".join(csv_filelist))
	
for table_path in csv_filelist:
	table_name = os.path.split(table_path)[-1]
	output_path = os.path.join("/data/out/tables",table_name)
	if debug_mode: print("Processing file %s..."%table_path)
	with open(table_path,"rt",encoding=config_encoding) as infile, open(output_path,"wt",encoding=config_encoding) as outfile:
		lineno = 0
		replaced_total = 0
		for inline in infile:
			if (config_tail_only):
				p = find_nth_column_position(inline)
				line_base = inline[:p-1] #till last column
				line_tail = inline[p:-1]
				if line_tail.endswith("\","): line_tail = line_tail[:-2]
				else: line_tail = line_tail[:-1]
				replaced_total+=line_tail.count(config_find)
				line_tail = line_tail.replace(config_find,config_replacement)
				replaced_line = line_base + "\"" + line_tail + "\"\n"
			else:
				replaced_total = inline.count(config_find)
				replaced_line = inline.replace(config_find,config_replacement)
			outfile.write(replaced_line)
			lineno+=1
		if debug_mode: print("Processed %d lines, replaced %d occurrences"%(lineno,replaced_total))
		