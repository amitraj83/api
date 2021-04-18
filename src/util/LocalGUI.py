import flask
from flask import request, jsonify
import psycopg2
import subprocess
import datetime
import numpy as np
import pandas as pd
import os, random
import os.path
from os import path
from flask import render_template, redirect
from flask import send_file
import shutil


app = flask.Flask(__name__, static_folder='./static')
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def getThreeBlogsLInks():
    dir = os.walk("C:\house-idea\scrapebox64\Addons\ScrapeBox Google Image Grabber")
    dirList = None
    for d in dir:
        dirList = d[1]
        break
    if dirList:
        randomDir = os.path.join("C:\house-idea\scrapebox64\Addons\ScrapeBox Google Image Grabber",
                                 d[1][random.randrange(len(d[1]))])
        randomFile = random.choice(os.listdir(randomDir))
        shutil.move(os.path.join(randomDir, randomFile), os.path.join(os.path.abspath(os.getcwd()), "static",randomFile))
        return render_template('mytemplate.html', imgSrc=randomDir+"-"+randomFile)
    else:
        return "<html><body>No image found. try again</body></html>"
    # image = random.choice(os.listdir(os.path.join(os.path.abspath(os.getcwd()), "static")))


PARENT_DIR = "C:\\house-idea\\code\\api\\src\\util\\"

@app.route('/accept', methods=['GET'])
def accept():
    imgSrc = request.args.get('imgSrc')
    print(os.path.abspath(os.getcwd()))
    src = os.path.join(os.path.abspath(os.getcwd()), "static", imgSrc)
    print(src)
    dest = os.path.join(os.path.abspath(os.getcwd()),  "approved")
    shutil.move(src, dest)
    return redirect('http://localhost:90')

@app.route('/reject', methods=['GET'])
def reject():
    imgSrc = request.args.get('imgSrc')
    os.remove(os.path.join(os.path.abspath(os.getcwd()), "static", imgSrc))
    return redirect('http://localhost:90')



@app.route('/move-to-server', methods=['POST'])
def moveall():
    root = os.path.join(os.path.abspath(os.getcwd()), "approved")
    subprocess.run(["scp", root+"/*.*", "root178.62.52.68:/root"])
    return redirect('http://localhost:90')


app.run(host='0.0.0.0', port=90)