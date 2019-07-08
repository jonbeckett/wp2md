# wp2md

## Wordpress XML Export to Markdown Text File Converter for Python 3.x

This python 3.x script will convert a Wordpress export file into a collection of markdown formatted text files.

Usage:

`python wp2md.py <export file> <output folder>`

e.g.

`python wp2md.py c:\temp\blog_export.xml c:\temp\output`


### Pre-Requisites

The script makes use of both the markdownify, and unidecode modules, which should be installed with PIP as per the commands below:

`pip install markdownify`
`pip install unidecode`


### Output

The script creates a folder structure within the output folder of years, and months (in yyyy-mm format). Each markdown file within those folders will be named by it's original post date (in yyyy-mm-dd format) along the post title - e.g. `2019-07-08 Hello World.md`.

Within each markdown file, the original post title is on the first line, the date in long format (e.g. Monday 8th July 2019) is on the third line, and content begins on the 5th line.

Most common extended characters are replaced at run-time to their ascii equivalents - so curly quotes, long dashes, etc are replaced with standard ascii equivalents.


### Notes

I have not experimented with images and media within the blog export, and I have not played with removing all the Wordpress block comments - mostly because I did not need to for my own blog. If this is an issue for you, you might want to extend the code further and/or re-write the way the script deals with that content.