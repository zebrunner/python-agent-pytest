class ZafiraError(Exception):
    """ Common exception for Zafira App """


class ConfigError(ZafiraError):
    """ Raises if environ var is missing """


class APIError(ZafiraError):
    """ An exception for Zafira client API calls issues """
