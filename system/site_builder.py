# -*- coding: utf-8 -*-

import __init__
import datetime
import cherrypy
import __main__

from jinja2 import Environment, ModuleLoader, Template, FunctionLoader, FileSystemLoader, ChoiceLoader

class builder():

	cur_time = datetime.datetime.now()

	loads = 0

	COMPILED = __main__.core.APP_DIR+'templates/compiled/templates.py'

	env = Environment(
		auto_reload=True,
		loader=FileSystemLoader(__main__.core.APP_DIR+'templates/')
	)

	def __init__(self, core = None):

		if not core:
			core = __main__.core

		self.core_settings = core
		self.base_fields = self.core_settings.base_fields

	def throwWebError(self, error_code = 404, params = {}):

		error = 'Unknown error'
		if error_code == 404:
			error = 'Page Not Found'

		fields = {'error': error, 'code':error_code }

		return self.loadTemplate('error.jinja2', fields)

	def redirect(self, url, text = "Redirecting ... "):
		fields = {'redirect_url':url,'redirect_text':text}
		return self.loadTemplate('redirect.jinja2',fields)

	def httpRedirect(self, url):
		raise cherrypy.HTTPRedirect(url)

	def prettifyTmpPath(self, tmp_path):
		return tmp_path.replace('./','')

	def loadTemplate(self, filename = '', fields = {}, incoming_text = False, useJ = False):

		if not 'current_page' in fields:
			fields.update({
				'current_page': filename,
				'version': self.core_settings.__version__,
				'address': cherrypy.request.path_info[1:],
				'build': self.core_settings.__build__,
				'conf_name': self.core_settings.loaded_data['conf_name']
			})

		if not 'login' in fields:
			fields.update({'login':False})

		fields.update(self.base_fields)

		template = self.env.get_template(filename)
		fields.update({"fields": fields})
		text = template.render(fields)

		return text

if __name__ == '__main__':
	builder = builder()