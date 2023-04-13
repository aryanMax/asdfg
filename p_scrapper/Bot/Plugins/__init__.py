from Bot import bot, loop
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram.errors import FloodWait
from ..Helpers.Coomer_Scrapper import fetch_coomer_pages
from ..Helpers.Kemono_Scrapper import fetch_kemono_pages
from ..config import botStartTime
from concurrent.futures import ThreadPoolExecutor
import psutil
import shutil
import asyncio
import re
import requests
import os
from time import time
executor = ThreadPoolExecutor(10)
