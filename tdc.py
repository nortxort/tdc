""" Tinychat directory crawler by Nortxort (https://github.com/nortxort)"""
import web
import room


class Directory:
    """
    Class to get rooms from tinychat's directory.
    """
    base_url = 'https://tinychat.com'
    post_url = 'https://tinychat.com/home/data'

    def __init__(self, crawl=False, category='all'):
        """
        Initialize the Directory class.

        :param crawl: if True, get rooms at class initializing.
        :type crawl: bool
        :param category: The room category. `all`, `most-gifted` or `near-you`.
        :type category: str
        """
        self.category = category
        self._html_source = ''
        self._rooms = {}
        self._page = 0
        self._csrf_token = ''

        if crawl:
            self.crawl()

    @property
    def rooms_dict(self):
        """
        Returns a dictionary where the key is
        the room name and the value is a Room instances.

        :return: A dictionary of rooms.
        :rtype: dict
        """
        return self._rooms

    @property
    def rooms(self):
        """
        Returns a list of Room instances.

        :return: A list of Room instances.
        :rtype: list
        """
        rooms = []
        for k in self._rooms:
            rooms.append(self._rooms[k])
        return rooms

    @property
    def pages_crawled(self):
        """
        Returns the number of `pages` crawled.

        :return: The number of pages crawled.
        :rtype: int
        """
        return self._page

    @property
    def room_count(self):
        """
        Returns the number of unique rooms found.

        :return: The number of rooms found.
        :rtype: int
        """
        return len(self._rooms) - 1

    def _set_csrf_token(self):
        """
        Set the csrf token required for the POST.
        """
        pattern = 'id="csrf-token" content="'
        if pattern in self._html_source:
            self._csrf_token = self._html_source.split(pattern)[1].split('" />')[0]
        else:
            print ('[ERROR] setting the csrf token failed.')

    def _poster(self, category='', page=0):
        """
        Makes POST to tinychat's server and gets json data as response.

        :param category: The room category. e.g `all`, `most-gifted` or `near-you`.
        :type category: str
        :param page: The page number.
        :type page: int
        :return: json data or None.
        :rtype: dict | None
        """
        if self._csrf_token != '':
            header = {'X-Requested-With': 'XMLHttpRequest'}

            post_data = {
                '_token': self._csrf_token,
                'category': category,
                'page': str(page)
            }

            response = web.post(url=self.post_url, post_data=post_data, header=header, json=True)
            if response.error is None:
                return response.json
        return None

    def _crawler(self):
        """
        The initial crawler.
        """
        first_run = self._poster()

        for room_data in first_run['rooms'][self.category]:
            room_name = room_data['name']
            if room_name not in self._rooms:
                self._rooms[room_name] = room.Room(**room_data)
            else:
                self._rooms[room_name].add_images(room_data['images'])

        # start the page crawler.
        self._page_crawler()

    def _page_crawler(self):
        """
        Crawls tinychat directory pages.
        """
        page = 1
        while True:
            page_crawler = self._poster(category=self.category, page=page)
            if page_crawler is None:
                print ('[ERROR] json response: %s' % page_crawler)
                break
            elif len(page_crawler['rooms']) == 0:
                break
            else:
                for k in page_crawler['rooms']:
                    room_name = page_crawler['rooms'][k]['name']
                    if room_name not in self._rooms:
                        self._rooms[room_name] = room.Room(**page_crawler['rooms'][k])
                    else:
                        room_images = page_crawler['rooms'][k]['images']
                        self._rooms[room_name].add_images(room_images)

                page += 1
                self._page = page

    def crawl(self):
        """
        Prepares and starts the crawler.
        """
        response = web.get(self.base_url)
        if response.error is None:
            self._html_source = response.content
            self._set_csrf_token()
            self._crawler()
        else:
            print ('[ERROR] crawl error: %s' % response.error)
