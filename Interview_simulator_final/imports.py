import streamlit as st
from streamlit_option_menu import option_menu #navbar
import pymysql as pm #database
import subprocess #page linking
import sys #page linking

#resume
import base64
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
#resume

#emotion
import cv2
import numpy as np
from keras.models import load_model
import time
#emotion

#save state
import json
#save state

#tech_int
import pandas as pd
import spacy
import random
#tech_int

def dbconn():
    return pm.connect(host='localhost',user='root',password='',db='final_vis')