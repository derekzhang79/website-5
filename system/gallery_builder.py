# -*- coding: utf-8 -*-

import ImageOps
import Image
import os

class galleryBuilder():

	THUMB_DIR = False
	ORIGINAL_DIR = False

	def __init__(self, settings):
		self.core = settings

		self.THUMB_DIR = settings.APP_DIR + settings.conf['gallery']['thumbnails_dir']
		self.ORIGINAL_DIR = settings.APP_DIR + settings.conf['gallery']['original_dir']

	def resizeImage(self, file_path, th_width = 200, th_height = 200):
		image = Image.open(file_path)
		thumb = ImageOps.fit(image, (th_width, th_height), Image.ANTIALIAS)

		filename = file_path.rsplit('/', 1)[1]
		new_filename = filename.rsplit('.', 1)[0] + "_thumb.png"

		thumb.save(self.THUMB_DIR + new_filename, "PNG")

		return {
			'original': filename,
		    'thumbnail': new_filename
		}

	def getFiles(self, directory):

		alist_filter = ['jpg','bmp','png','gif']
		path = os.path.join(directory)

		files = []

		for r,d,f in os.walk(path):
			for file in f:
				if file[-3:].lower() in alist_filter:
					files.append(os.path.join(directory, file))

		return files

	def resizeAllImages(self):
		print '> START IMAGE RESIZING...'
		print 'Open ' + self.ORIGINAL_DIR + ' directory'

		files = self.getFiles(self.ORIGINAL_DIR)
		result = []

		total = len(files)
		print 'Found ' + str(total)+ ' files... Processing...'

		count = 1
		for filename in files:
			fileinfo = self.resizeImage(filename)
			result.append(fileinfo)

			print str(count) + '/' + str(total)
			count += 1

		print 'Done!...'

		return result

