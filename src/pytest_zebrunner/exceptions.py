class ZebrunnerError(Exception):
    """ Common exception for Zafira App """


class ConfigError(ZebrunnerError):
    """ Raises if environ var is missing """


class APIError(ZebrunnerError):
    """ An exception for Zafira client API calls issues """
