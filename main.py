import os

import user
import options
import sync

api = user.authenticate()

location = os.path.expanduser(options.location())

sync.sync(api, location)
