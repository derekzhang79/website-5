# -*- coding: utf-8 -*-

import ImageOps
import Image
import os

class galleryBuilder():

	THUMB_DIR = False
	THUMB64_DIR = False
	ORIGINAL_DIR = False
	NEW_ORIGINAL_DIR = False

	def __init__(self, settings):
		self.core = settings

		self.THUMB_DIR = settings.APP_DIR + settings.conf['gallery']['thumbnails_dir']
		self.THUMB64_DIR = settings.APP_DIR + settings.conf['gallery']['thumbnails64_dir']
		self.ORIGINAL_DIR = settings.APP_DIR + settings.conf['gallery']['original_dir']
		self.NEW_ORIGINAL_DIR = settings.APP_DIR + settings.conf['gallery']['new_original_dir']

	def resizeImage(self, file_path, th_width = 200, th_height = 200, or_width = 800, or_height = 600):
		image = Image.open(file_path)

		# Crop and make thumbnails
		thumb = ImageOps.fit(image, (th_width, th_height), Image.ANTIALIAS)
		thumb64 = ImageOps.fit(image, (64, 64), Image.ANTIALIAS)

		# Resize original
		image.thumbnail((or_width, or_height), Image.ANTIALIAS)

		old_filename = file_path.rsplit('/', 1)[1]
		thumb_filename = old_filename.rsplit('.', 1)[0] + "_thumb.png"
		new_filename = old_filename.rsplit('.', 1)[0] + "_new.png"

		thumb_filename = thumb_filename.replace(" ", "_")
		new_filename = thumb_filename.replace(" ", "_")

		thumb.save(self.THUMB_DIR + thumb_filename, "PNG")
		thumb64.save(self.THUMB64_DIR + thumb_filename, "PNG")

		image.save(self.NEW_ORIGINAL_DIR + new_filename, "PNG")

		return {
			'original': old_filename,
		    'new_original': new_filename,
		    'thumbnail': thumb_filename
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

	def resizeAllImages(self, existing_images = set()):
		print '> START IMAGE RESIZING...'
		print 'Open ' + self.ORIGINAL_DIR + ' directory'

		files = self.getFiles(self.ORIGINAL_DIR)
		result = []

		total = len(files)
		print 'Found ' + str(total)+ ' files... Processing...'

		count = 1
		for filename in files:
			message = str(count) + '/' + str(total)
			if not filename.rsplit('/', 1)[1] in existing_images:
				fileinfo = self.resizeImage(filename)
				result.append(fileinfo)

			else:
				message += ' skipped'

			print message
			count += 1

		print 'Done!...'

		return result

