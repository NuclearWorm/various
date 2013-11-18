#!/usr/bin/env python

"""This demonstrates a minimal http upload cgi.
This allows a user to upload up to three files at once.
It is trivial to change the number of files uploaded.

This script has security risks. A user could attempt to fill
a disk partition with endless uploads. 
If you have a system open to the public you would obviously want
to limit the size and number of files written to the disk.
"""
import cgi
import cgitb; cgitb.enable()
import os, sys
from comparevideo import CompareVideo

UPLOAD_DIR = "/tmp"

HTML_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><title>File Upload</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head><body><h1>File Upload</h1>
<form action="%(SCRIPT_NAME)s" method="POST" enctype="multipart/form-data">
File name: <input name="file_1" type="file"><br>
File name: <input name="file_2" type="file"><br>
<input name="submit" type="submit">
</form>
"""

def print_html_form (addition):
    """This prints out the html form. Note that the action is set to
      the name of the script which makes this is a self-posting form.
      In other words, this cgi both displays a form and processes it.
    """
    print "content-type: text/html\n"
    print HTML_TEMPLATE % {'SCRIPT_NAME':os.environ['SCRIPT_NAME']}
    print '<br><h3>Result:</h3><p>' + addition
    print """</body>
    </html>"""

files_c = []
form = cgi.FieldStorage()
def save_uploaded_file (form_field, upload_dir):
    """This saves a file uploaded by an HTML form.
       The form_field is the name of the file input field from the form.
       For example, the following form_field would be "file_1":
           <input name="file_1" type="file">
       The upload_dir is the directory where the file will be written.
       If no file was uploaded or if the field does not exist then
       this does nothing.
    """
    
    if not form.has_key(form_field): return
    fileitem = form[form_field]
    if not fileitem.file: return
    path = os.path.join(upload_dir, fileitem.filename) 
    files_c.append(path)
    fout = file (path, 'wb')
    while 1:
        chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()

save_uploaded_file ("file_1", UPLOAD_DIR)
save_uploaded_file ("file_2", UPLOAD_DIR)


compare = CompareVideo(files_c[0], files_c[1])
add = compare.compare()
compare.clean()
print_html_form (add)
