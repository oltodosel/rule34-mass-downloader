import urllib.request, os
from bs4 import BeautifulSoup

# To download images or not, if not, then it just saves urls into ./urls
# It's quite faster to download separately if the batch is too big.
# `cat urls | parallel -k -P5 --progress wget`
to_download = False

query = input("What am i searching for? ")
query = query.replace(" ", "+")

pid = 0
while 1:
	url = "https://rule34.xxx/index.php?page=dapi&s=post&q=index"
	limit = "&limit=1000"
	tags = "&tags=" + query
	url = url + limit + tags + '&pid=' + str(pid)
	download = int(0)

	if not os.path.exists(query):
		os.makedirs(query)

	html = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")
	url = str(soup.getText)
	url = str(url)
	url = url.split('file_url="')
	num = int(0)
	for item in url:
		test = str(item)
		if test.startswith("//img"):
			num += 1
	print((str(num) + ' results for "' + query + '"'))

	if num == 0:
		print("no results")
		exit()
	ac2 = int(1)

	print("\n\n\nBegining download")
	for item in url:
		test = str(item)
		url = test
		if test.startswith("//img"):
			url = url.replace('="', "")
			url = url.split(" ")
			url = url[0]
			url = url.replace('"', "")
			url = url.replace("//", "http://")
			name = url.replace("/", "-")
			name = name.replace("http:--img.rule34.xxx-images-", (query + "/"))

			if not os.path.isfile(name):
				if to_download:
					print("Downloading: " + url)
					urllib.request.urlretrieve(url, name)
					download += 1
					print("Downloaded " + str(download))
				else:
					print(url, file=open('urls', 'a'))
			else:
				print("Already downloaded " + url)

	if download == 1:
		endcharacter = ""
	else:
		endcharacter = "s"

	if download == 0:
		print("\n\n\nDownloaded nothing")
	else:
		print("\n\n\nDownloaded " + str(download) +" image" + endcharacter)

	pid += 1
