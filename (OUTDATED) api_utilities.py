## This code is outdated, it was built to work with the previous API version.

from datetime import datetime, timedelta
import requests, json


# Base class to handle logs and caches
class BaseLog:
    # Init method
    # Saves the specified file path
    # Keeps a time stamp of when the log class was created, to log when the program launches
    # Var stores the item separator
    def __init__(self, file_path):
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
    def write_file(self, text):
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
    def log_message(self, msg, t=None):
        if not t: t = datetime.timestamp(datetime.now())

        text = f"{t} {self.separator} {msg}"
        self.write_file(text)

    # Log Command method
    # Logs the command used, as well as the time it was used (as a timestamp)
    # Also logs the user who executed the command, if passed through
    def log_command(self, cmd, user=None, t=None):
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
    def __init__(self, grace=10, cache_length=30):
        super().__init__('cache.txt')
        self.grace = timedelta(minutes=grace)
        self.cache_length = cache_length

    # Get Timestamp function
    # Returns a timestamp from the passed string
    def get_timestamp(self, string):
        return datetime.fromtimestamp(float(string))

    # Get Json function
    # Returns a dict of the passed json string
    def get_json(self, string):
        return json.loads(string)

    # Load Json function
    # Returns a json string of the passed dict
    def load_json(self, dct):
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
    def check_cache(self, string, item, name):
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
        tx = l[-1].split({f" self.separator "})[0]

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

# Connection Class (inherits from Cache)
# Establishes a connection to NG's servers, and handles api calls
# Purpose: makes everything a lot easier to read later on
class Connection(Cache):
    # Init method
    # Sets api_key as an attribute, and tests the connection to the servers
    # If test fails, raises an exception
    # NTS: change "Exception" to "ConnectionError" later on
    def __init__(self, cache=True, grace=10):
        self.api_key = "http://apiv2.nethergames.org"
        if not self.test_connection:
            print("Error Connecting to NetherGames Servers")
            raise Exception

        self.cache = cache
        if cache:
            super().__init__(grace)

    # Test Connection method
    # Uses the server stats api command to test the connection to NG's servers
    # If successful, returns the response as a python dict
    # Else returns False
    def test_connection(self):
        query = "/servers/stats?total=true"
        response = requests.get(self.api_key + query)

        if str(response.status_code).startswith("2"):
            return response.json()
        else:
            return False

    # Cache Data method
    # If self.cache is set to True, writes the passed data into the cache
    # Else, returns False
    def cache_data(self, data):
        if not self.cache: return False
        if self.scan_cache(data): return False

        self.write_cache(data)

    # Stats method
    # Requests the specified ign's stats
    # Returns them as a python dict
    def stats(self, ign):
        r = self.scan_cache(ign, name=True)
        if r: return r

        query = f"/players/{ign}/stats"

        response = requests.get(self.api_key + query).json()
        self.cache_data(response)
        return response

    # Guild method
    # Requests the specified guild's stats
    # Returns them as a python dict
    def guild(self, guild):
        query = f"/guilds/{guild}/stats"

        response = requests.get(self.api_key + query).json()
        return response

    # Leaderboard method
    # Requests the specified leaderboard
    # Returns it as a python dict
    def leaderboard(self, board, game=None, column=None, scope=None, limit=100):
        query = "/leaderboard?"
        query += f"type={board}&"
        if game: query += f"game={game}&"
        if column: query += f"column={column}&"
        if scope: query += f"scope={scope}&"
        query += f"limit={limit}"

        response = requests.get(self.api_key + query).json()
        return response

    # Server Announcements method
    # Requests the announcements of specified form, to the specified limit (defaults to last 100)
    # Returns response as a python dict
    def server_announcments(self, form, limit=100):
        query = f"/announcements?type={form}&limit={limit}"

        response = requests.get(self.api_key + query).json()
        return response

    # Discord Announcements Method
    # Requests the discord announcements to the specified limit (defaults to last 100)
    # Returns response as a python dict
    # NOTE: Currently Disabled
    # def discord_announcements(self, limit=100):
    #     query = f"announcements/discord?limit={limit}"
    #
    #     response = requests.get(self.api_key + query).json()
    #     return response

#_______________________________________________________________________________________________________

if __name__ == '__main__':
    con = Connection()
    print(con.test_connection())
