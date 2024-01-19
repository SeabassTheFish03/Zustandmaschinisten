import sys

def main():
	if sys.argc == 3:
		filename = sys.argv[1]
		openMode = sys.argv[2]
	else:
		print("Usage: py setup.py <filename.json> <openMode>")
		exit()


if __name__ == "__main__":
	main()