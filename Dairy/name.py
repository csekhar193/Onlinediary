import urllib2
print("Please enter the name of the person\n")
name = raw_input()
url = 'https://gender-api.com/get?key=uBmwJfvnZkytwoUAwb&name='+name
response = urllib2.urlopen(url).read()
print(response)