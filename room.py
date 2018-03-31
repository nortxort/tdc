
class Image:
    """
    Class representing an image.
    """
    def __init__(self, image_url):
        """
        Initialize the Image class.

        :param image_url: An image url.
        :type image_url: str
        """
        self._image_url = image_url
        self._img_parts = self._image_url.split('/')

    @property
    def url(self):
        """
        Returns the url of a image.

        :return: An image url.
        :rtype: str
        """
        return self._image_url

    @property
    def uid(self):
        """
        Returns the user ID (handle?) of a image.

        :return: The user ID of a image.
        :rtype: int
        """
        return self._img_parts[3]

    @property
    def name(self):
        """
        Returns the file name of a image.

        :return: The image file name.
        :rtype: str
        """
        return self._img_parts[4]


class Room:
    """
    Class representing a room on the directory.
    """
    def __init__(self, **room_data):
        """
        Initialize the Room class.

        :param room_data: A dictionary containing room data.
        :type room_data: dict
        """
        self._status = room_data.get('status', [])
        self._name = room_data.get('name', '')
        self._broadcasters_images = room_data.get('broadcasters_images', [])
        self._users = room_data.get('users')
        self._images = room_data.get('images', [])
        self._status_icon = room_data.get('status_icon', '')
        self._broadcasters_image_common = room_data.get('broadcasters_image_common', '')
        self._general_icon = room_data.get('general_icon', '')
        self._description = room_data.get('description', '')

    @property
    def status(self):
        """
        Returns a list of statuses a room has been a signed. e.g `promoted`, `pro` etc.

        NOTE: This might not apply to all rooms.

        :return: A list of statuses.
        :rtype: list
        """
        return self._status

    @property
    def name(self):
        """
        Returns the room name.

        :return: The name of the room.
        :rtype: str
        """
        return self._name

    @property
    def broadcasters_images(self):
        """
        Not sure what this is.

        :return:
        :rtype: list
        """
        return self._broadcasters_images

    @property
    def images(self):
        """
        Returns a list of Image instances.

        :return: A list of Image instances.
        :rtype: list
        """
        images = []
        for img in self._images:
            image = Image(img)
            images.append(image)
        return images

    @property
    def status_icon(self):
        """
        Returns a status icon image url.

        :return: A image url.
        :rtype: str
        """
        return self._status_icon

    @property
    def broadcasters_image_common(self):
        """
        Returns a image url constructed from broadcasting users.

        :return: A image url.
        :rtype: str
        """
        return self._broadcasters_image_common

    @property
    def general_icon(self):
        """
        Returns a rooms avatar image url.

        :return: A room avatar image url.
        :rtype: str
        """
        return self._general_icon

    @property
    def description(self):
        """
        Returns the room description.

        :return: The room description.
        :rtype: str
        """
        return self._description

    @property
    def watching_count(self):
        """
        Returns the number of users in the room *not* broadcasting.

        :return: The number of users not broadcasting.
        :rtype: int
        """
        return self._users['watching_count']

    @property
    def broadcasting_count(self):
        """
        Returns the number of users broadcasting.

        :return: The number of users broadcasting.
        :rtype: int
        """
        return self._users['broadcasting_count']

    @property
    def total_users(self):
        """
        Returns the total number of users in a room.

        :return: The total user count.
        :rtype: int
        """
        return self.watching_count + self.broadcasting_count

    def add_images(self, images):
        """
        Add one or more images to a rooms images.

        :param images: A list containing image url's.
        :type images: list
        """
        if len(images) == 1:
            self._images.append(images[0])
        elif len(images) > 1:
            self._images.extend(images)
