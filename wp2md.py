# Script         : Wordpress to Markdown
# Author         : Jonathan Beckett (jonbeckett@outlook.com)
# Compatibility  : Python 3.x
# Pre-Requisites : Markdownify and Unidecode
#
# To install the pre-requisites, run the following commands from the command prompt:
# > pip install markdownify
# > pip install unidecode

import sys
import os
import time
import datetime
import re
from xml.dom import minidom
from markdownify import markdownify as md
from unidecode import unidecode

# if the tool is run with no arguments, display a title
if (len(sys.argv)==1):
	print("\nwp2md.py - Wordpress Export to Markdown Conversion Tool, by Jonathan Beckett\n")

# check we have parameters - inform the user if not
if len(sys.argv)<3:
	print("Tool expects two arguments.")
	print("Format : python wp2md.py <source_file> <output_path>")
	print("e.g. python wp2md.py c:\\temp\\blog.xml c:\\temp\\output")
	sys.exit(0)
	
# get the parameters from the command line
source_file = sys.argv[1]
output_path = sys.argv[2]


if not os.path.isfile(source_file):
	print("The input file (" + source_file +") does not exist")
	sys.exit(0)
	
if not os.path.isdir(output_path):
	print("The output directory (" + output_path +") does not exist")
	sys.exit(0)


# utility function to strip invalid characters from filenames (needed because we use post titles in filenames)
def get_valid_filename(fn):
	fn = str(fn).strip()
	return re.sub(r'(?u)[^-\w\ ]', '', fn)

# read the XML file
xml_doc = minidom.parse(source_file)

# get the blog posts from the XML
blog_posts = xml_doc.getElementsByTagName("item")

# loop through the blog posts in the XML
for blog_post in blog_posts:

	# get the post type
	post_type = blog_post.getElementsByTagName("wp:post_type")[0].firstChild.nodeValue

	# do not handle attachments
	if (post_type != "attachment"):

		# retrieve the title from the post
		if (blog_post.getElementsByTagName("title")[0].firstChild):
			post_title = blog_post.getElementsByTagName("title")[0].firstChild.nodeValue
		else:
			post_title = "Untitled"
		
		post_date = blog_post.getElementsByTagName("wp:post_date")[0].firstChild.nodeValue
		
		# retrieve the content from the post
		if (blog_post.getElementsByTagName("content:encoded")[0].firstChild):
			post_content = blog_post.getElementsByTagName("content:encoded")[0].firstChild.nodeValue
		else:
			post_content = ""
			
		# replace extended characters, tags, etc
		post_content = post_content.replace("<!-- wp:paragraph -->","")
		post_content = post_content.replace("<!-- /wp:paragraph -->","")
		post_content = post_content.replace( u'\U0001f499', '')
		post_content = post_content.replace( u'\U0001f49a', '')
		post_content = post_content.replace( u'\U0001f49b', '')
		post_content = post_content.replace( u'\U0001f49c', '')
		post_content = post_content.replace( u'\U0001f633', '')
		post_content = post_content.replace( u'\u2018', u'\'')
		post_content = post_content.replace( u'\u2019', u'\'')
		post_content = post_content.replace( u'\u201c', u'\"')
		post_content = post_content.replace( u'\u201d', u'\"')
		post_content = post_content.replace( u'\u2013', '-')
		post_content = post_content.replace( u'\u2026', '...')
		post_content = post_content.replace( u'\u2033', '\'')
		post_content = post_content.replace( u'\u2032', '\'')
		post_content = post_content.replace( u'\xd7', 'x')
		post_content = post_content.replace( u'\xc2', ' ')
		
		post_content = unidecode(post_content)
		
		# if there are paragraph tags in the content, convert it to markdown
		# else leave it alone		
		if ("<p" in post_content):
			post_markdown = md(post_content)
		else:
			post_markdown = post_content
		
		# Sometimes markdownify leaves spaces at the start of lines - remove them
		post_markdown = ''.join(line.lstrip(' \t') for line in post_markdown.splitlines(True))
		
		# construct a post date in year-month-day format (use wp:post_date to retrieve the data)
		post_year = post_date[0:4]
		post_month = post_date[5:7]
		post_day = post_date[8:10]
		post_day_digit = post_day[-1:]
		post_date = datetime.datetime.strptime(post_year + "-" + post_month + "-" + post_day, '%Y-%m-%d')
		
		# work out the suffix for the date
		post_day_suffixes = {"1":"st" , "2":"nd" , "3":"rd"}
		post_day_suffix = post_day_suffixes.get(post_day_digit,"th")
		
		# make a nicely formatted date (e.g. Monday 8th July 2019)
		post_date_formatted = post_date.strftime("%A ") + post_day.lstrip("0") + post_day_suffix + post_date.strftime(" %B %Y")
		
		# create a filename for the post
		post_filename = post_year + "-" + post_month + "-" + post_day + " " + post_title
		
		# create a year folder
		post_parent_path = os.path.join(output_path,post_year)
		if not os.path.exists(post_parent_path):
			os.makedirs(post_parent_path)
			print("Creating Parent Path for " + post_year)
		
		# create a month folder within the year folder
		post_child_path = os.path.join(output_path,post_year,post_year + "-" + post_month)
		if not os.path.exists(post_child_path):
			os.makedirs(post_child_path)
			print("Creating Child Path for " + post_year + "-" + post_month)
		
		# construct a valid filename
		output_filename = os.path.join(post_child_path,get_valid_filename(post_filename) + ".md")
		
		# write the markdown into a file
		post_file = open(output_filename, "w")
		post_file.write("# " + post_title + "\n\n")
		post_file.write("## " + post_date_formatted + "\n\n")
		post_file.write(post_markdown)
		post_file.close()
		
		# output the filename (to show progress)
		print(output_filename)
