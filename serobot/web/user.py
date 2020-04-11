
from dataclasses import dataclass
from typing import List
from configparser import ConfigParser


@dataclass
class User:
    username: str
    password: str
    permissions: List[str]

    @classmethod
    def read_user_map(cls, auth_path):
        """
        Parameters
        ----------
        auth_path : Path
            Path to the authorization configuration file.

        Returns
        -------
        user_map : Dict[str, User]
            User map to be used with DictionaryAuthorizationPolicy.
        """
        config = ConfigParser()
        config.read(auth_path)

        user_map = dict()
        try:
            for username in config.sections():
                values = config[username]
                password = values['password']
                user_map[username] = cls(username, password, ['public', 'protected'])
        except Exception:
            raise RuntimeError(f'Error reading authorization configuration from {auth_path}.')

        return user_map
