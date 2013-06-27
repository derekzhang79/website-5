# -*- coding: utf-8 -*-

import basic_controller

class mainController(basic_controller.defaultController):

	DIR = './'

	pages = {
		'type': ['index', 'default'],
		'urls': {
			'index':            'printDefault',
			'':                 'printDefault',
			'tweeria':          'printProject',
			'kgs':              'printProject',
			'megatyumen':       'printProject',
			'works':            'printProject'
		}
	}

	def printDefault(self, data):
		return self.printTemplate('index', data)

	def printProject(self, data):

		project = {'code': data['fields']['__page__']}

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

		data['fields'].update({'project': project})

		return self.printTemplate('project', data)
