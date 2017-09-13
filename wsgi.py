#!/usr/bin/env python3

from infibot import app
from bot import util

if __name__ == "__main__":
    util.set_webhook()

    app.run()
