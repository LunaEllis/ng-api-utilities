# importing Python packages
from datetime import datetime, timedelta
import requests, json
# imports custom exceptions from exceptions.py
from exceptions import *


# Base class to handle logs and caches
class BaseLog:
    # Init method
    # Saves the specified file path
    # Keeps a time stamp of when the log class was created, to log when the program launches
    # Var stores the item separator
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.time_created = datetime.timestamp(datetime.now())
        self.separator = "-//-"
        self.new_line = "\n"

    # Read File method
    # Returns the entire file as a string
    def read_file(self):
        with open(self.file_path, "r+") as f:
            x = f.read()
            f.close()
        return x

    # Write File method
    # Appends the passed string to the end of the file, followed by a new line char
    def write_file(self, text: str):
        with open(self.file_path, "a+") as f:
            f.write(text + self.new_line)
            f.close()

    # Clear method
    # Clears the file
    def clear_file(self):
        with open(self.file_path, "w") as f:
            f.close()


# Log class (inherits from BaseLog)
# Class to handle writing to a log
class Log(BaseLog):
    # Init method
    # Calls the BaseLog init, passing a file path of 'log.txt'
    # Logs when the program was initiated
    def __init__(self):
        super().__init__('log.txt')
        self.log_message("Program initiated", self.time_created)

    # Log Message method
    # Writes the passed / current timestamp, and the passed message, into the log file
    def log_message(self, msg: str, t=None):
        if not t: t = datetime.timestamp(datetime.now())

        text = f"{t} {self.separator} {msg}"
        self.write_file(text)

    # Log Command method
    # Logs the command used, as well as the time it was used (as a timestamp)
    # Also logs the user who executed the command, if passed through
    def log_command(self, cmd: str, user=None, t=None):
        if not t: t = datetime.time((datetime.now()))

        text = f"{t} {self.separator} "
        if not user:
            text += f"{cmd}"
        else:
            text += f"{user} executed {cmd}"

        self.write_file(text)


# Cache class (inherits from BaseLog)
# Class to handle caching api data
class Cache(BaseLog):
    # Init method
    # Calls the BaseLog init, passing a file path of 'cache.txt'
    # Defines the grace period in minutes for cached data (defaults to 10)
    # Defines the max length of the cache (defaults to 30)
    def __init__(self, grace=15, cache_length=50):
        super().__init__('cache.txt')
        self.grace = timedelta(minutes=grace)
        self.cache_length = cache_length

    # Get Timestamp function
    # Returns a timestamp from the passed datetime string
    def get_timestamp(self, string: str):
        return datetime.fromtimestamp(float(string))

    # Get Json function
    # Returns a dict of the passed json string
    def get_json(self, string: str):
        return json.loads(string)

    # Load Json function
    # Returns a json string of the passed dict
    def load_json(self, dct):
        """
        Returns dictionary object as a string of json
        :param dct: dict
        :return: json
        """
        return json.dumps(dct)


    # Scan Cache method
    # Performs a basic check to see if the passed string is stored
    # in the file, and if so calls the Check Cache method.
    # If both checks are passed, returns True. Else returns False
    def scan_cache(self, string, name=False):
        l = self.read_file().split(self.new_line)

        # Iterates through each entry in the cache, checking if 'string' is contained in the entry
        # If string is found, calls check_cache, passing 'string', the entry 'string' was found in, and 'name'.
        for item in l:
            if str(string) in item:
                a = self.check_cache(string, item, name)
                if a: return a

        return None

    # Check Cache method
    # Checks if the item passed through was saved to the cache within the grace period
    # Also checks if item and string match
    # Returns True on match, else returns False
    def check_cache(self, string: str, item: str, name: bool):
        l = item.split(f" {self.separator} ")
        t1 = self.get_timestamp(l[0])
        t2 = datetime.now()

        if t2 - t1 >= self.grace: return False

        if name and (self.load_json(l[1])['name'].lower() == string.lower()):
            return self.load_json(l[1])
        if not name: return self.load_json(l[1])

        return False

    # Clean Cache method
    # Clears any obsolete data from the cache
    def clean_cache(self):
        # Loads the cache as a list of each item
        # Var stores the current time as a datetime obj
        l = self.read_file().split(self.new_line)
        tn = datetime.now()

        # Guard clause, clears the file and returns if list 'l' is empty
        if len(l) < 1: return self.clear_file()

        # Var stores the timestamp of the cache's last entry
        tx = l[-1].split(self.separator)[0]

        # Checks if the timestamp tx is older than the grace period
        if tn - self.get_timestamp(tx) >= self.grace:
            return self.clear_file()

        # Removes each obsolete item from the list of cache entries
        for item in l:
            if tn - self.get_timestamp(item[0]) >= self.grace:
                l.pop(l.index(item))

        # Writes every remaining item back into the cache
        self.clear_file()
        for item in l:
            self.write_cache(item.split(f" {self.separator} ")[1])

    # Write Cache method
    # Writes passed item into cache
    # Returns 1 if successful
    def write_cache(self, item):
        # Turns cache into list of entries
        # If len of list is full, removes the first (oldest) entry
        l = self.read_file().split(self.new_line)
        if len(l) >= self.cache_length:
            l = l[1:]

        # Writes the current time (as a timestamp), followed by the passed item, into the cache
        t = datetime.timestamp(datetime.now())
        string = f"{t} {self.separator} {str(item)}"

        self.write_file(string)
        return 1

#_____________________________________________________________________________________________________________________


# Conection Class (inherits from Cache)
# Establishes a connection to NG's API, and manages calls to said API
# Purpose: Readability + Versatility
class Connection(Cache):
    # Init method
    # Sets api_key as an attribute, and tests the connection to the servers
    # If test fails, rasies an exception
    def __init__(self, auth_key=get_auth_key(), cache=True, grace=15):
        self.api_key = "http://apiv2.nethergames.org"
        self.auth_key = self.auth_key()
        self.test_connection()

        self.cache = cache
        if cache:
            super().__init__(grace)

    # Get Auth Key method
    # Returns API auth key from text file.
    # -- GUIDE to setup API auth key in GitHub Repository --
    def get_auth_key(self):
        with open("auth_key.txt", "r+") as f:
            key = f.readline().strip()
            f.close()
        return key

    # Base Call method
    # Performs a request using the passed query
    # Checks if response is valid, if not raises connection error
    def base_call(self, query: str, json=True):
        if self.auth_key:
            # if valid auth key is detected, a call is made using that auth key
            response = requests.get(self.api_key + query, headers={'Authorization': f'TOK:{self.auth_key}'})
        else:
            response = requests.get(self.api_key + query)

        if str(response.status_code).startswith("2"):
            if not json: return response
            return response.json()
        else:
            raise ConnectionError(response.status_code, query_type=query)

    # Cache Call method
    # Makes a base call using the passed query, and caches the data
    def cache_call(self, query: str, json=True):
        return self.cache_data(self.base_call(query, json))

    # Test Connection method
    # Uses the server stats api command to test the connection to NG's servers
    # If successful, returns the response as a python dict
    # Else returns False
    def test_connection(self):
        query = "/v1/servers"

        return self.base_call(query)

    # Cache Data method
    # if self.cache is set to true, attempts to write the passed data into the cache and returns data
    # else, returns False
    def cache_data(self, data: dict):
        if not self.cache: return False
        if self.scan_cache(data) or not data: return False

        self.write_cache(data)
        return data

    # Stats method
    # Requests the specified ign's stats
    # Returns them as a python dict
    def stats(self, ign: str):
        r = self.scan_cache(ign, name=True)
        if r: return r

        query = f"/v1/players/{ign}"

        return self.cache_call(query)

    # Guild method
    # Requests the specified guild's stats
    # Returns them as a python dict
    def guild(self, guild: str):
        query = f"/v1/guilds/{guild}"

        return self.cache_call(query)

    # Leaderboard method
    # Requests the specified leaderboard
    # Returns it as a python dict
    def leaderboard(self, board, column=None, scope=None, limit=100):
        query = f"/v1/leaderboads?type={board}"

        if board == 'game':
            query += f"&{column}" # column is only used when type is 'game'
        if board == 'factions':
            query += f"&{scope}" # scope is only used when type is 'factions'

        return self.cache_call(query)

    # Server Announcements method
    # Requests the announcements of specified form, to the specified limit (defaults to last 100)
    # Returns response as a python dict
    def server_announcments(self, form: str, limit=100):
        if form == 'discord':
            query = f"/v1/announcments/discord?limit={limit}"
        else:
            query = f"/v1/announcments?type={form}&limit={limit}"

        return self.cache_call(query)

    # Player Avatar method
    # Requests the specified player's avatar
    # Returns response as 64x64 image/png
    def player_avatar(self, ign: str):
        query = f"/v1/players/{ign}/avatar"

        r =  self.base_call(query, json=False)

        with open("sample_image.png", "wb") as file:
            file.write(r.content)
            file.close()

        return r


#__________
if __name__ == '__main__':
    con = Connection()
    print(con.test_connection())
