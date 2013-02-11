# -*- coding: utf-8 -*-

import basic
import site_builder

class miscController(basic.defaultController):

	@basic.printpage
	def printPage(self, page, params):

		self.sbuilder = site_builder.builder()

		return {
			'index':            self.printIndex,
		    '':                 self.printIndex,
		    'tweeria':          self.printProject,
		    'kgs':              self.printProject,
		    'megatyumen':       self.printProject,
		    'works':            self.printProject,
		}

	@basic.methods
	def methods(self, params = {}):
		return {

		}

	# --------------------------------------------------------------------------------------------------
	# Print pages

	def printIndex(self, fields, param):
		fields = {}
		return basic.defaultController._printTemplate(self, 'index', fields)

	def printProject(self, fields, param):

		project = {'code': fields['__page__']}

		if project['code'] == 'tweeria':
			project.update({
				'name': 'Tweeria',
			    'link': 'http://tweeria.com'
			})

		elif project['code'] == 'kgs':
			project.update({
				'name': 'Document Management System for Government',
			})

		elif project['code'] == 'megatyumen':
			project.update({
				'name': 'City Portal',
				'link': 'http://megatyumen.ru'
			})

		elif project['code'] == 'works':
			project.update({
				'name': 'Random works'
			})

		fields.update({'project': project})

		return basic.defaultController._printTemplate(self, 'project', fields)


data = {
	'class': miscController,
    'type': ['index', 'default'],
	'urls': ['', 'index', 'tweeria', 'kgs', 'megatyumen', 'works']
}
