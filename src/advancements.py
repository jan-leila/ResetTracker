from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import json
import os

from tracking import Advancement

class Advancements(FileSystemEventHandler):
	def __init__(self, callback):
		self.callback = callback

		self.file_watchdog = None

	def read_file(self, path):
		try:
			with open(path) as f:
				json_data = json.load(f)
		except:
			return
		advancements = Advancement.parse_advancements(json_data)
		self.callback(advancements)

	def on_modified(self, event):
		if event.is_directory:
			return
		self.read_file(event.src_path)

	def injest(self, path):
		files = os.listdir(path)
		self.read_file(os.path.join(path, files[0]))

	def set_path(self, path):
		self.file_watchdog = Observer()
		self.file_watchdog.schedule(self, path, recursive=False)
		self.file_watchdog.start()

	def stop(self):
		if not self.file_watchdog == None:
			self.file_watchdog.stop()
			self.file_watchdog.join()
