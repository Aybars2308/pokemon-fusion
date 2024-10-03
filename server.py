from flask import Flask, send_file, request
import random
from PIL import Image
import os

app = Flask(__name__)