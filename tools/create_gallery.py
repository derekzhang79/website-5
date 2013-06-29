#!/usr/bin/python
# -*- coding: utf-8 -*-

import __init__
import settings

import ImageOps
import Image
import os
from time import time

class galleryBuilder():

	THUMB_DIR = False
	THUMB64_DIR = False
	ORIGINAL_DIR = False
	NEW_ORIGINAL_DIR = False

	def __init__(self, settings):
		self.conf = settings.conf
		self.db = settings.db
		self.collection = self.conf['gallery']['collection']

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

	def resizeImages(self, filenames, existing_images = set()):

		result = []
		total = len(filenames)

		count = 1
		for filename in filenames:
			message = str(count) + '/' + str(total)
			if not filename.rsplit('/', 1)[1] in existing_images:
				fileinfo = self.resizeImage(filename)
				result.append(fileinfo)

			else:
				message += ' skipped'

			print message
			count += 1

		return result

	def getFilesList(self):
		filenames = self.getFiles(self.ORIGINAL_DIR)
		total = len(filenames)
		print 'Found ' + str(total)+ ' files...'

		return filenames

	def getFormattedList(self, filenames):
		images = set()
		for filename in filenames:
			images.add(filename.rsplit('/', 1)[1])

		return images

	def addToDatabase(self, records):
		for record in records:
			record = {
				'original': record['original'],
				'new_original': record['new_original'],
				'thumbnail': record['thumbnail'],
				'time': time()
			}
			self.db.insert(self.collection, record)

	def createGallery(self):
		print '> START IMAGE RESIZING...'
		print 'Open ' + self.ORIGINAL_DIR + ' directory'

		if not self.db:
			print '> No Database'
			return False

		filenames = self.getFilesList()

		existing_images = set()
		if not self.conf['gallery']['force']:
			self.db.createCollection(self.collection)
			_buff = self.db.get(self.collection, {})

			for item in _buff:
				existing_images.add(item['original'])
		else:
			self.db.cleanUp(self.collection)

		print 'Processing...'

		result = self.resizeImages(filenames, existing_images)
		self.addToDatabase(result)

		images_to_delete = existing_images - self.getFormattedList(filenames)

		for image_name in images_to_delete:
			self.db.remove(self.collection, {'original': image_name})

		print 'Done!...'

if __name__ == '__main__':

	core = settings.core(clear_run=True)
	gn = galleryBuilder(core)
	gn.createGallery()

