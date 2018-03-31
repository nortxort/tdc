""" Web related functions and utilities. version 0.0.9 """
import time
import logging
import requests
import requests_toolbelt
import requests.utils as utils
import requests.structures as structures

__all__ = ['utils', 'requests_toolbelt', 'structures']

# Default user agent for both GET and POST.
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'

log = logging.getLogger(__name__)

__session = requests.session()


def _default_header():
    """
    Default header for both GET and POST.

    :return: The default header dict.
    :rtype: dict
    """
    header = {
        'Accept': '*/*',
        'User-Agent': USER_AGENT,
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    return header


def is_cookie_expired(cookie_name):
    """
    Check if a session cookie is expired.

    :param cookie_name: The cookie name
    :type cookie_name: str
    :return: True if expired, False if not expired,
    or None if the cookie name is not in the session cookies.
    :rtype: bool | None
    """
    expires = int
    timestamp = int(time.time())

    for cookie in __session.cookies:
        if cookie.name == cookie_name:
            expires = cookie.expires
        else:
            return None

    if timestamp > expires:
        log.debug('cookie[\'%s\'] is expired. time stamp: %s, expires: %s' %
                  (cookie_name, timestamp, expires))
        return True

    log.debug('cookie[\'%s\'] is not expired. time stamp: %s, expires: %s' %
              (cookie_name, timestamp, expires))

    return False


def delete_cookie(cookie_name):
    """
    Delete a session cookie by name.

    :param cookie_name: The name of the cookie to delete.
    :type cookie_name: str
    :return: True if the cookie was deleted, else False.
    :rtype: bool
    """
    if cookie_name in __session.cookies:
        log.debug('session cookies before deletion: %s' % __session.cookies)
        del __session.cookies[cookie_name]
        log.debug('session cookies after deletion: %s' % __session.cookies)

        return True

    return False


def has_cookie(cookie_name):
    """
    Check if a cookie is in the session cookies.

    :param cookie_name: The name of the cookie to check.
    :type cookie_name: str
    :return: A request.cookie if the cookie is in session cookies, else False.
    :rtype: bool | requests.cookie
    """
    if cookie_name in __session.cookies:
        log.debug('cookie `%s` found in session.' % __session.cookies[cookie_name])
        return __session.cookies[cookie_name]

    log.debug('no cookie named `%s` found in session.' % cookie_name)
    return False


class Response:
    """ Class representing a response. """
    def __init__(self, content, json, cookies, headers, status_code, error=None):
        """
        Initiate the Response and set its values.
        """
        self.content = content
        self.json = json
        self.cookies = cookies
        self.headers = headers
        self.status_code = status_code
        self.error = error


def get(url, json=False, header=None, referer=None, proxy='', timeout=20, session=True):
    """
    Makes a GET request.

    :param url: The url of the GET request.
    :type url: str
    :param json: Set to True if the expected response contains json data.
    :type json: bool
    :param header: Use a special header for this request.
    :type header: dict | None
    :param referer: Use a special referer for the request.
    :type referer: str | None
    :param proxy: Use a proxy for this request.
    :type proxy: str
    :param timeout: The timeout of the request.
    :type timeout: int
    :param session: Should session data be saved from this request.
    :type session: bool
    :return: A Response object.
    :rtype: Response
    """
    d_header = _default_header()

    if referer is not None:
        d_header['Referer'] = referer

    if isinstance(header, dict):
        d_header.update(header)

    if proxy:
        _proxy = {
            'https': 'http://%s' % proxy,
            'http': 'http://%s' % proxy
        }
        proxy = _proxy

    _e = None
    _gr = None
    _json = None

    log.debug('url: %s' % url)
    try:
        if not session:
            _gr = requests.request(method='GET', url=url, headers=d_header, proxies=proxy, timeout=timeout)
        else:
            _gr = __session.request(method='GET', url=url, headers=d_header, proxies=proxy, timeout=timeout)
        if json:
            _json = _gr.json()
    except ValueError as ve:
        log.error('ValueError while decoding `%s` to json. %s' % (url, ve))
        _e = ve
    except (requests.ConnectionError, requests.RequestException) as re:
        log.error('requests exception: %s' % re)
        _e = re
    finally:
        if _gr is None or _e is not None:
            _response = Response(None, None, None, None, None, error=_e)
        else:
            _response = Response(_gr.text, _json, _gr.cookies, _gr.headers, _gr.status_code)

        return _response


def post(url, post_data, json=False, header=None, referer=None, proxy='', timeout=20, session=True,
         follow_redirect=False, is_stream=False):
    """
    Makes a POST request.

    :param url: The url of the POST request.
    :type url: str
    :param post_data: The data to POST.
    :type post_data:
    :param json: Set to True if the expected POST response contains json data.
    :type json: bool
    :param header: Use a special header for this POST request.
    :type header: dict | None
    :param referer: Use a special referer for this POST request.
    :type referer: str | None
    :param proxy: Use a proxy for this POST request.
    :type proxy: str
    :param timeout: The timeout for the POST request.
    :type timeout: int
    :param session: Should session data be saved from this POST request.
    :type session: bool
    :param follow_redirect: Should the POST request follow redirects.
    :type follow_redirect: bool
    :param is_stream: Is the post data a stream(file).
    :type is_stream: bool
    :return: A Response object.
    :rtype: Response
    """
    d_header = _default_header()

    if referer is not None:
        d_header['Referer'] = referer

    if isinstance(header, dict):
        d_header.update(header)

    if proxy:
        _proxy = {
            'https': 'http://%s' % proxy,
            'http': 'http://%s' % proxy
        }
        proxy = _proxy

    _e = None
    _pr = None
    _json = None

    log.debug('url: %s, post_data: %s' % (url, post_data))
    try:
        if not session:
            _pr = requests.request(method='POST', url=url, data=post_data, headers=d_header,
                                   allow_redirects=follow_redirect, proxies=proxy, timeout=timeout, stream=is_stream)
        else:
            _pr = __session.request(method='POST', url=url, data=post_data, headers=d_header,
                                    allow_redirects=follow_redirect, proxies=proxy, timeout=timeout, stream=is_stream)
        if json:
            _json = _pr.json()
    except ValueError as ve:
        log.error('ValueError while decoding `%s` to json. %s' % (url, ve))
        _e = ve
    except (requests.ConnectionError, requests.RequestException) as re:
        log.error('requests exception: %s' % re)
        _e = re
    finally:
        if _pr is None or _e is not None:
            _response = Response(None, None, None, None, None, error=_e)
        else:
            _response = Response(_pr.text, _json, _pr.cookies, _pr.headers, _pr.status_code)

        return _response
