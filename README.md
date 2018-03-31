<<<<<<< HEAD
## Tdc

Directory crawler.

### Requirements

* [requests](https://github.com/requests/requests)
* [requests_toolbelt](https://github.com/requests/toolbelt) *


`pip install requests requests_toolbelt`

\* *Only required because of it's import in web.py. Not relevant to the code.*

## Usage
A basic example:

	import tdc
	
	directory = tdc.Directory(crawl=True)
	
	# show the results
	for room in directory.rooms:
		print('%s, Users: %s, Broadcasters: %s, Watching: %s' % 
			(room.name, room.total_users, room.broadcasting_count, room.watching_count))
	

## Author

* [nortxort](https://github.com/nortxort)

## License

The MIT License (MIT)

Copyright (c) 2018 nortxort

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice
shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
=======
# tdc
Directory crawler
>>>>>>> d79db7cc06052d7a9e3fa2567d7cf0772a17b54a
