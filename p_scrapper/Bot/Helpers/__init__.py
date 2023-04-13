from bs4 import BeautifulSoup
import requests
from Bot import bot, loop
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.errors import FloodWait
from concurrent.futures import ThreadPoolExecutor
import re
executor = ThreadPoolExecutor(10)
