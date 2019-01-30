import web
import os
#import pyjxslt
#import lxml.etree as ET #XSL transform
from bs4 import BeautifulSoup #pretty print RDF output
render = web.template.render('templates/')

urls = (
	'/', 'home', 
	'/viewer', 'viewer',
	'/download' , 'download' 
) 
	
#home
class home(object):
	def GET(self):
		return render.home()


	# POST method for extraction option and input file uploading
	def POST(self):
		# uploaded file
		inpf = web.input(myfile={})
		filedir = 'static/temp' # change this to the directory you want to store the file in
		if 'myfile' in inpf: # to check if the file-object is created
			
		 	filepath=inpf.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
		 	filename=filepath.split('/')[-1] # splits the filepath and chooses the last part (the filename with extension)
		
		 	fout = open(filedir +'/input.xml','w') # creates the file where the uploaded file should be stored
		 	fout.write(inpf.myfile.file.read()) # writes the uploaded file to the newly created file named input.xml
		 	fout.close() # closes the file, upload complete.

		# extraction option
		btn = web.input()
		opt = "%s" % (btn.transform)
		if opt == "1-people":
			execfile('static/script/transform/1-People.py')
			execfile('static/script/transform/toRDFa.py')
			raise web.seeother('/viewer')
		elif opt == "2-people_ev":
			execfile('static/script/transform/2-People_Events.py')
			execfile('static/script/transform/toRDFa.py')
			raise web.seeother('/viewer')
		elif opt == "3-people_rel":
			execfile('static/script/transform/3-People_Relations.py')
			execfile('static/script/transform/toRDFa.py')
			raise web.seeother('/viewer')
		elif opt == "4-places":
			execfile('static/script/transform/4-Places.py')
			execfile('static/script/transform/toRDFa.py')
			raise web.seeother('/viewer')
		elif opt == "5-all":
			execfile('static/script/transform/5-All.py')
			execfile('static/script/transform/toRDFa.py')
			raise web.seeother('/viewer')
		else:
			raise web.seeother('/#transform')
		
# viewer
class viewer(object):
	def GET(self):
		output_path = 'static/temp/viz.html'

		if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
			#bs = BeautifulSoup(open(output_path), 'html')
			#output = bs.prettify()

			output = open(output_path, 'r').read()
			return render.viewer(output)
		else: 
			raise web.seeother('/#transform') # redirects user to upload form if there is no output file in temp folder 


class download(object):
	def GET(self):
		download_path = 'static/temp/output.rdf'
		if os.path.exists(download_path) and os.path.getsize(download_path) > 0:
			bs = BeautifulSoup(open(download_path), 'xml')
			output = bs.prettify()
			return open(output, 'rb'),read()
		else: 
			raise web.seeother('/#transform') # redirects user to upload form if there is no output file in temp folder 


if __name__ == "__main__":
	app = web.application(urls, globals())
	app.internalerror = web.debugerror
	app.run()