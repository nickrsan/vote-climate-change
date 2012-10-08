from django.template.defaultfilters import removetags
from django.core import exceptions

import voteclimate.models

all_tags = ["!doctype", "a","abbr","acronym","address","applet","area","b","base","basefont","bdo","big","blockquote","body","br","button","caption",
"center","cite","code","col","colgroup","dd","del","dfn","dir","div","dl","dt","em","fieldset","font","form","frameset","h1","h2","h3",
"h4","h5","h6","head","hr","html","i","iframe","img","input","ins","isindex","kbd","label","legend","li","link","map","menu","meta","noframes",
"noscript","object","ol","optgroup","option","p","param","pre","q","s","samp","script","select","small","span","strike","strong","style",
"sub","sup","table","tbody","td","textarea","tfoot","th","thead","title","tr","tt","u","ul","var",]

def strip_tags(process_string,unsafe_tags = None,safe_tags = None):
	'''django's removetags only accepts space separated lists of tags (rawr), so we're taking our list and composing that string, while accepting some safe tags to keep
	copied from EC code'''
	
	if (not unsafe_tags and not safe_tags): # if we don't have any args passed or they are invalid
		#print "neither"
		unsafe_tags = all_tags
	elif safe_tags:
		#print "safe"
		unsafe_tags = list(set(all_tags) - set(safe_tags)) # if we provided safe tags, subtract them from the set of all_tags

		if unsafe_tags: # we don't need anything else done, but if both args are provided, we should print a warning noting that only the safe is being used since it's more restrictive
			pass # TODO: PRINT WARNING
	elif unsafe_tags is not None and type(unsafe_tags) != list: # this should check for functionality and not type, but for now this is fine
		#print "wrong - %s" % type(unsafe_tags)
		unsafe_tags = all_tags # start with all tags as the base to strip
	elif unsafe_tags:
		#print "unsafe"
		pass # it's already defined, but we don't want it caught in the else
	else:
		#print "other"
		unsafe_tags = all_tags
	
	remove_str = ""
	for item in unsafe_tags:
		remove_str += "%s " % item
	
	return removetags(process_string,remove_str)
