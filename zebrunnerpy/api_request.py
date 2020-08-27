import logging

import requests


class APIRequest:

    LOGGER = logging.getLogger('zebrunner')

    def __init__(self, base_url):
        self.base_url = base_url

    # HTTP methods
    def send_post(self, endpoint, body=None, headers=None, default_err_msg=None):
        url = self.base_url + endpoint
        self.LOGGER.debug('POST {} \n Headers:{} \n Payload: {}'.format(url, headers, body))
        try:
            resp = requests.post(url, json=body, headers=headers)
        except Exception as e:
            self.LOGGER.error(default_err_msg, e)
        return self.__verify_response(resp)

    def send_post_screenshot(self, endpoint, body=None, headers=None, default_err_msg=None):
        url = self.base_url + endpoint
        self.LOGGER.debug('POST {} \n Headers:{} \n Payload: {}'.format(url, headers, body))
        try:
            resp = requests.post(url, body, headers=headers)
        except Exception as e:
            self.LOGGER.error(default_err_msg, e)
        return self.__verify_response(resp)

    def send_post_without_authorization(self, endpoint, body=None, default_err_msg=None):
        url = self.base_url + endpoint
        self.LOGGER.debug('POST {} \n Payload: {}'.format(url, body))
        try:
            resp = requests.post(url, json=body)
        except Exception as e:
            self.LOGGER.error(default_err_msg, e)
        return self.__verify_response(resp)

    def send_get(self, endpoint, headers=None, default_err_msg=None):
        url = self.base_url + endpoint
        self.LOGGER.debug('POST {} \n Headers:{} \n Payload: {}'.format(url, headers, body))
        try:
            resp = requests.get(url=url, headers=headers)
        except Exception as e:
            self.LOGGER.error(default_err_msg, e)
        return self.__verify_response(resp)

    def send_delete(self, endpoint=None, body=None, headers=None, default_err_msg=None):
        url = self.base_url + endpoint
        self.LOGGER.debug('POST {} \n Headers:{} \n Payload: {}'.format(url, headers, body))
        try:
            resp = requests.delete(url, json=body, headers=headers)
        except Exception as e:
            self.LOGGER.error(default_err_msg, e)
        return self.__verify_response(resp)

    def send_put(self, endpoint=None, body=None, headers=None, default_err_msg=None):
        url = self.base_url + endpoint
        self.LOGGER.debug('POST {} \n Headers:{} \n Payload: {}'.format(url, headers, body))
        try:
            resp = requests.put(url, json=body, headers=headers)
        except Exception as e:
            self.LOGGER.error(default_err_msg, e)
        return self.__verify_response(resp)

    @staticmethod
    def __verify_response(resp):
        """Log and check API call. In case status code of response is not 200, will raise an HTTPException """
        if not str(resp.status_code).startswith('2'):
            raise Exception("HTTP call fails. Response status code {status_code}".format(status_code=resp.status_code))
        return resp
