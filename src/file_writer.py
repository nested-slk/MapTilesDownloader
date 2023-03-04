import sqlite3
import os
import multiprocessing
import io
import json
import shutil

class FileWriter:

	slicer = None
	dataFile = ""
	def ensureDirectory(lock, directory):

		lock.acquire()
		try:

			if not os.path.exists('temp'):
				os.makedirs('temp')

			if not os.path.exists('output'):
				os.makedirs('output')

			os.makedirs(directory, exist_ok=True)

		finally:
			lock.release()

		return directory

	def createLogFile(lock, path, fileName):
		global logFilePath

		logFilePath = path + "\\tiles_list.txt"
		FileWriter.ensureDirectory(lock, path)

		logData = "\n"
		with open(logFilePath, 'w+') as logFile:
			logFile.write(logData)

		return

	def closeLogFile(lock):
		global logFilePath

		logData = "\n"
		with open(logFilePath, 'a') as logFile:
			logFile.write(logData)

		return

	@staticmethod
	def addMetadata(lock, path, file, name, description, format, bounds, center, minZoom, maxZoom, profile="mercator", tileSize=256):
		# global dataFile
		# dataFile = path
		FileWriter.ensureDirectory(lock, path)

		data = [
			("name", name),
			("description", description),
			("format", format), 
			("bounds", ','.join(map(str, bounds))), 
			("center", ','.join(map(str, center))), 
			("minzoom", minZoom), 
			("maxzoom", maxZoom), 
			("profile", profile), 
			("tilesize", str(tileSize)), 
			("scheme", "xyz"), 
			("generator", "EliteMapper by Visor Dynamics"),
			("type", "overlay"),
			("attribution", "EliteMapper by Visor Dynamics"),
		]
		with open(path + "/metadata.json", 'w+') as jsonFile:
			json.dump(dict(data), jsonFile)

		FileWriter.createLogFile(lock, path, file)
		
		return
	
	@staticmethod
	def addInfoToLogFile(lock, x, y, z):
		global logFilePath

		with open(logFilePath, 'a') as logFile:
			logFile.write("\n <file>")
			logFile.write("osm_100-l-3-{z}-{x}-{y}.png".format( x=x, y=y, z=z))
			logFile.write("</file>")

		return

	@staticmethod
	def addTile(lock, filePath, sourcePath, x, y, z, outputScale):
		fileDirectory = os.path.dirname(filePath)
		FileWriter.ensureDirectory(lock, fileDirectory)
		shutil.copyfile(sourcePath, filePath)
		FileWriter.addInfoToLogFile(lock, x, y, z)
		return

	@staticmethod
	def exists(filePath, x, y, z):
		if os.path.isfile(filePath):
			FileWriter.addInfoToLogFile(lock, x, y, z)
			return True

		return False


	@staticmethod
	def close(lock, path, file, minZoom, maxZoom):
		FileWriter.closeLogFile(lock)
		#TODO recalculate bounds and center
		return