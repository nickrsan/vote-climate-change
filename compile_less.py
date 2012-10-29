import os, subprocess, re
from vote_climate.settings import LESSC

def compile_less(dirs = None, node = "node", lessc = LESSC):
	for l_dir in dirs:
		if os.path.exists(l_dir):
			if (lessc is None) or (not os.path.exists(lessc)):
				lessc = os.path.join(l_dir,"..","..","utils","less","bin","lessc") # set the default less location to a subfolder of the directory here
				if not os.path.exists(lessc):
					raise BaseException("No lessc at %s" % lessc) # this won't handle if lessc is in the path
			for root, dirs, files in os.walk(l_dir): # for every file in every subdirectory of this folder
				for l_file in files:
					if re.search("\.less$", l_file): # if it ends with .less 
						full_file_path = os.path.join(root,l_file)
						css_file_path = full_file_path[:-4] + "css" # create a full path for this with the name css
						print "compiling %s -> %s" % (full_file_path,css_file_path)
						check = subprocess.call([node,lessc,full_file_path,">",css_file_path],shell=True) # run it on the shell
						
						if check == 0: # if it all went well
							f = open(css_file_path,'r')
							l_css = f.read()
							f.close()
							f = open(css_file_path,'w')
							f.writelines(("/*************** THIS IS AN AUTOMATICALLY COMPILED CSS FILE ***************/\n/*****/\n/*************** DO NOT MAKE CHANGES HERE ***************/\n/*****/\n/*****/\n/*****/\n/*****/\n\n\n\n\n\n\n",l_css))
							f.close()

