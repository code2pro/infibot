#!/usr/bin/env python3

from vslbot import app
from bot import util

util.set_webhook()

if __name__ == "__main__":
    app.run()
