# -*- coding: utf-8 -*-

import basic_controller

class galleryController(basic_controller.defaultController):

	DIR = './gallery/'

	pages = {
	'type': ['photos'],
		'urls': {
			'big': 'printFotorama'
		}
	}

	def printDefault(self, data):
		images = self.core.model['gallery']['Images'].getImages()
		data['fields'].update({'images': images})

		return self.printTemplate('gallery', data)

	def printFotorama(self, data):
		images = self.core.model['gallery']['Images'].getImages()
		data['fields'].update({'images': images})

		return self.printTemplate('gallery_fotorama', data)