import web
import os
import pyjxslt
import lxml.etree as ET #XSL transform
from bs4 import BeautifulSoup #pretty print RDF output
render = web.template.render('templates/')

urls = (
	'/', 'home', 
	'/viewer', 'viewer' 
) 
	
#home
class home(object):
	def GET(self):
		return render.home()

	#POST method for input file uploading (check that document is xml to do)
	#fai in modo che input file si chiami sempre input.xml
	def POST(self):
		x = web.input(myfile={})
		filedir = 'static/temp' # change this to the directory you want to store the file in.
		if 'myfile' in x: # to check if the file-object is created
			filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.

			#transform file and write output to output.xml (change to result.rdf)
			

			xml_filename = filedir +'/'+ filename
			xsl_filename = 'static/script/transform/transform_people.xsl'


			gw = pyjxslt.Gateway(25333)
			# Add an xslt transformation.  
			#       First parameter is the name of the transformation
			# 	    Second parameter is either XSLT text or the name of a file that contains XSLT text
			gw.add_transform('k1', xsl_filename)
			# Do a transformation
			#       First parameter is the name of the xslt transformation (cached on server)
			#       Second parameter is either XML text or the name of a file that contains XML text
			#       Third parameter is dictionary of parameters to pass to XSLT Transformer [parms_dict]
			result = gw.transform('k1', xml_filename)
			# Remove the transformation when you are done with it or need to replace it with a new one
			gw.remove_transform('k1')

			f = open('static/temp/output.xml', 'w')
			f.write(ET.tostring(result, pretty_print=True))
			f.close()


			# dom = ET.parse(xml_filename)
			# xslt = ET.parse(xsl_filename)
			# transform = ET.XSLT(xslt)
			# newdom = transform(dom)
			# f = open('static/temp/output.xml', 'w')
			# f.write(ET.tostring(newdom, pretty_print=True))
			# f.close()

		



		raise web.seeother('/viewer')#make redirection to visualization?

#viewer
class viewer(object):
	def GET(self):
		output_path = 'static/temp/output.xml'

		if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
			bs = BeautifulSoup(open(output_path), 'xml')
			output = bs.prettify()

			return render.viewer(output)
		else: 
			raise web.seeother('/#transform') # redirects user to upload form if there is no output file in temp folder 

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()