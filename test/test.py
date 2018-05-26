import requests

in_file = open("test.jpg", "rb") # opening for [r]eading as [b]inary
bytes_stream = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
in_file.close()

files = {'file': open('test.jpg','rb')}
values = {'DB': 'photcat', 'OUT': 'jpg', 'SHORT': 'short'}

r=requests.post("http://localhost:5000/",
                files=files,
                data=values)

print(r.headers)
print(r.content)
