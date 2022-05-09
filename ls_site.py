import os
rootPath = "./site"

class lsSite():
	def __init__(self, path):
		if path[-1] == '/':
			path = path[:-1]
		self.path = path
		self.len = len(path)

	def listdir_recursive(self, path, depth):
		if(path[-1] != "/"):
			path += "/"
		fpw = open(path + "index.html", "wb")
		fpw.write("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><head><title>index</title></head><body><ul>".encode("utf-8"))
		if(path != rootPath and path != rootPath + "/"):
			fpw.write("\n<p style=\"margin: 25px;\"><li><a href=\"../\" style=\"font-size:25px\">dir: ../</a></li></p>".encode("utf-8"))
		for item in os.listdir(path):
			if(item == "404.html" \
				or item == "index.html" \
				or item == "favicon.ico"):
				continue
			itemPath = os.path.join(path, item)
			if(os.path.isdir(itemPath)):
				self.listdir_recursive(itemPath, depth + 1)
				Str = "\n<p style=\"margin: 25px;\"><li><a href=\""
				if(depth == 0):
					Str += "./"
				else:
					for i in range(depth):
						Str += "../"
				fpw.write((Str + itemPath[7:] + "/index.html\" style=\"font-size:25px\">dir: " + itemPath[7:] + "/</a></li></p>").encode("utf-8"))
			else:
				Str = "\n<p style=\"margin: 25px;\"><li><a href=\""
				if(depth == 0):
					Str += "./"
				else:
					for i in range(depth):
						Str += "../"
				fpw.write((Str + itemPath[7:] + "\" style=\"font-size:25px\">" + itemPath[7:] + "</a></li></p>" ).encode("utf-8"))
		fpw.write("\n</ul></body></html>".encode("utf-8"))
		fpw.close()
	def run(self):
		self.listdir_recursive(self.path, 0)

ls = lsSite(rootPath)
ls.run()