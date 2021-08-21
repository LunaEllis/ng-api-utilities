# NG - API Utilities
A Python module to make communicating with the NetherGames REST API easier and more streamlined.

NOTE: I highly recommend reading through the documentation for the NG REST API, which can be read at [this link](
https://support.nethergames.org/en-au/article/rest-api-documentation-1wf73dq/),
      just so you understand what each api request is doing.
      Additionally, please read the [Integration Setup Guide](https://github.com/LunaEllis/ng-api-utilities/blob/main/Integration%20Setup%20Guide.md) if you're developing a larger project and unsure of what an integration is.

# IN THIS MODULE:
- Class Connection

- Class BaseLog
- Class Log
- Class Cache

- Method get_auth_key

_Editor's Note: All classes will contain the attributes and methods of inherited classes, but they won't be written down here._


# Class Connection:
// inherits from class Cache

- Establishes a connection to the NG servers.
- Takes parameters:
  - cache { = True }
    - If True, opens the cache file and reads/writes player data from the cache.
  - grace { = 15 }
    - Defines the length of time (in minutes) that cache entires will be considered 'useable'.
    - After the grace period, entries in the cache will be considered 'obsolete', and won't be useable.

- Attributes:
  - api_key
    - Stores the value 'http://apiv2.nethergames.org', which is the url header that every api call requires.
  - cache
    - Sets whether the cache is to be used or not.
  - grace
    - Defines the grace perioed for cached entries
    - Only used if cache is set to True.

- Methods:
  - base_call
    - Paramaters: _query_, _json_: True
    - Method makes the GET request using the passed query, and returns the response (as json, if bool _json_ is set to false
  - cache_call
    - Paramaters: _query_, _json_: True
    - Method passes paramaters to base_call, then writes the response to the cache and returns it
  - test_connection
    - Paramaters: _None_
    - Sends a server stats request to NG. If successful, returns a dict of the response.
  - cache_data
    - Paramaters: _data_
    - Writes _data_ to the cache, if self.cache is set to True
  - stats
    - Paramaters: _ign_
    - Gets the stats for the specified ign.
      - If ign has a useable entry in the cache, the entry is used, and no call is made to NG's servers.
        - This helps to reduce the chances of hitting the rate limit.
      - Otherwise, the stats are pulled from the server, passed into cache_data, and then returned.
  - guild
    - Paramaters: _guild_
    - Gets the guild stats for the specified guild.
  - leaderboard
    - Paramaters: _board_, _game_: None, _column_: None, _scope_: None, _limit_: 100
    - Makes a leaderboard request using the inputted data.
    - Read [this article](https://support.nethergames.org/en-au/article/rest-api-documentation-1wf73dq/#3-get-v1leaderboard) for more detail on how this works.
  - server_announcements
    - Paramaters: _form_, _limit_: 100
    - Pulls the server/discord announcements of the specified form, to the specified limit.
  - player_avatar
    - Paramaters: _ign_
    - Gets the avatar for the specified ign.
    - _Response is in the 64x64 image/png format_


# Class BaseLog

- Base class, handles creating log / cache file, reading to file, writing to file, and emptying file
- Takes parametaers:
  - file_path
    - Passes in the path of the desired file.

- Attributes:
  - time_created
    - Stores a time stamp of the time the init function was called.
      - This is meant for logs, to track once the program has been fully initialised.
  - seperator
    - Stores the separator used inside of logs / caches.
      - This can be changed, but it is recommended to make it a mix of characters that you wouldn't find else where, so as to not cause errors when reading from the cache.
  - new_line
    - Stores the new line character
      - This is so that, if the module is used on a different os, it can be easily changed.

- Methods:
  - read_file
    - Parameters: _None_
    - Returns the entire file (at file path) as a single string.
  - write_file
    - Parameters: _text_
    - Appends the passed text to the end of the file (at file path), followed by the new line character.
  - clear_file
    - Parameters: _None_
    - Overwrites the current file (at file path) with a new, empty file.


# Class Log
// inherits from BaseLog

- Class, handles writing to a log file.
- Takes parameters:
  - None

- Attributes:
  - None

- Methods:
  - log_message
    - Parameters: _msg_, _t_: None
    - Writes the timestamp _t_ into the log file, followed by the passed _msg_
      - If _t_ is None, _t_ is overwritten with a timestamp of the current time.
  - log_command
    - Parameters: _cmd_, _user_: None, _t_: None
    - Writes the timestamp _t_ into the log file.
    - This is followed by the passed _cmd_, as well as the passed _user_ who executed it.
      - If _user_ is None, just the passed _cmd_ is logged.


# Class Cache
// inherits from BaseLog

- Class, handles reading and writing to a cache.
- Takes paramaters:
  - grace { = 10 }
    - Defines the length of time (in minutes) that entries in the cache will be considered 'useable'.
  - cache_length { = 30 }
    - Defines the max number of entries the cache will save.

- Attributes:
  - None

- Methods:
  - get_timestamp
    - Parameters: _string_
    - Returns _string_ as a timestamp.
      - Note: _string_ must be in the form of a valid timestamp, but data type can vary.
  - get_json
    - Parameters: _string_
    - Returns _string_ as a Python dictionary.
      - Note: _string_ must be valid json.
  - load_json
    - Parameters: _dct_
    - Returns _dct_ as a string of valid json.
      - Note: _dct_ must be a Python dictionary.
  - scan_cache
    - Parameters: _string_, _name_: False
    - Performs a limited check to see if _string_ exists within the cache at all, by iterating through each entry in the cache.
      - If it finds _string_ in an entry, it performs a full check on that entry.
      - If _string_ isn't found anywhere in the cache, the method returns None.
  - check_cache
    - Parameters: _string_, _iten_, _name_
    - Performs a thorough check to see if _item_ is a 'useable' entry, and to see if _string_ and _item_ belong to the same ign.
      - If check is passed, the stats within _item_ are returned as a Python dict.
      - Otherwise, the method returns False.
  - clean_cache
    - Parameters: _None_
    - Removes any obsolete entries from the cache.
  - write_cache
    - Parameters: _item_
    - Writes the current timestamp, and the passed _item_, into the cache.
