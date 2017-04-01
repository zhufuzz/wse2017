import os, sys

class Example(object):
	@classmethod
	def main(cls, argv):
		baseDir = os.path.dirname(os.path.abspath(argv[0]))
		#first = os.path.dirname(os.path.abspath(argv[1]))
		print baseDir
		#print os.path.abspath(argv[1])


	#main = classmethod(main)

if __name__ == '__main__':
	Example.main(sys.argv)