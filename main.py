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

#print("Just forcing diff with this line")
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
	if config_find=="": config_find = "\"\"\""
	if config_replacement=="": config_replacement = "\"\""
	if config_encoding=="": config_encoding = "utf-8"
	debug_mode = 1
else:
	with open("/data/config.json","r") as fid:
		config = json.load(fid)
	interactive_mode = False
	config_find = config["parameters"]["find"]
	config_replacement = config["parameters"]["replacement"]
	config_encoding = config["parameters"]["encoding"]
	debug_mode = int(config["parameters"]["debug"])

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
		for inline in infile:
			outfile.write(inline.replace(config_find,config_replacement))
			lineno+=1
		if debug_mode: print("Processed %d lines"%lineno)
		