# -*- coding: utf-8 -*-

import basic_model

class Images(basic_model.defaultModel):

	def __init__(self, core):
		basic_model.defaultModel.__init__(self, core)
		self.collection = core.conf['gallery']['collection']

	def getImages(self):
		return self.db.get(self.collection, {}, sort={'time': -1})
