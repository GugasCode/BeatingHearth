import sys
import argparse
import numpy as np
import pulses as pul
import filters as flt
import utils.waves as wave
import utils.files as files
import utils.charts as chart
from classifiers import Bayes, KNN
from random import randint

def main():
    parser = argparse.ArgumentParser(description='Beating Heart Project')
    #parser.add_argument(dest='filenames', metavar='filename',nargs='*')
    #both input and output args optional, use cwd if not supplied or -i
    parser.add_argument('-i',dest='input')
    parser.add_argument('-o',dest='output')
    parser.add_argument('-v',dest='visual')
    parser.add_argument('-c',dest='charts')
    parser.add_argument('-t',dest='params')
    #files like .wav or .csv or .xls
    parser.add_argument('-p',dest='phase')

    args = parser.parse_args()

def convertToSCV(inputFolder, outputFolder):
    """
        Standard function to convert wave files in folders
        to their respective csv files
    """
    src = files.listDir(inputFolder)
    for f in src:
        waves = wave.loadWave(inputFolder+f)
        frames = wave.getSamples(waves)
        files.write(outputFolder + f[:-4] + ".csv", frames)

def stdMovArg(data):
    """
        A good standard to run the moving average filter passes
    """
    data = flt.movingAverage(data, 4)
    data = flt.movingAverage(data, 8)
    data = flt.movingAverage(data, 6)
    data = flt.movingAverage(np.fliplr(data), 4)
    data = flt.movingAverage(data, 8)
    data = flt.movingAverage(data, 6)
    return np.fliplr(data)

def stdClean(data):
    """
       Standard run using the clean function for each sound file
    """
    frames = flt.clean(data)
    frames = stdMovArg(frames)
    frames = flt.halfRate(frames)
    return flt.norm(frames)

def stdRun(path, graph=True):
    frames = files.reader(path)
    # if graph:
    #     chart.drawGraphJob(frames)
    frames = stdClean(frames)
    if graph:
        chart.drawGraphJob(frames)
    return pul.findBeats(frames, 4, 6)

def insertName(path, name, mode='w'):
    f = open(path, mode)
    f.write(name + ',')
    f.close()

def saveFile(path):
    """
        Saves the results in a specific file format.
        For latter comparison
    """
    output = "data.xls"
    f = files.listDir(path)
    for i in f:
        print(i)
        result = stdRun(path + i)
        insertName(output, i, mode='a')
        final = result[0]*2
        files.writeCSV(output, final, mode='a')

def classify(path, clas):
    """
        Makes a tuple with the file name, its frames and its classification
    """
    f = files.listDir(path)
    res = []
    for i in f:
        frames = files.reader(path + "/" + i)
        res.append((i,frames,clas))
    return res

def stdClassify(path, folders):
    """
        Makes a list of tuples with all files classified for use in training and test
    """
    l = []
    for p in folders:
        l.extend(classify(path+p, p))
    return l

def makeSets(data, perc=80):
    """
        Makes a test and training set from a list of all files,
        the devision is given by the perc(entage) attribute that specifies
        how much of the total will be used for the training set.
        The selection itself is made at random.
    """
    size = int(len(data) * (perc/100))
    test = []
    while len(data) > size:
        rand = randint(0,len(data)-1)
        test.append(data.pop(rand))
    return (test, data)

def stdRunClassify(path):
    """
        Standard run for classify pre given files based on their respective
        folders.
        Returns a tuple with the test and data sets.
    """
    folders = files.getDir(path)
    data = stdClassify(path, folders)
    return makeSets(data)

def stdShannonRun(path, graph=True):
    frames = files.reader(path)
    # if graph:
    #     chart.drawGraphJob(frames)
    frames = flt.halfRate(frames)
    frames = flt.norm(frames)
    frames = stdMovArg(frames)
    frames = flt.shannon(frames)
    # frames = flt.shannon(frames)
    frames = flt.avgShannon(frames, 40, 20)
    if graph:
        chart.drawGraphJob(frames)
    return pul.findBeats(frames, 4, 6)
    # return frames

if __name__ == '__main__':
    path = sys.argv[1]
    # pulse = stdShannonRun(path)
    # pulse = stdRun(path, graph=True)
    # print(pulse[0])
    # point = pul.getT11(pulse[0], flt.distinguish(pulseStd))
    # print("T11 = " + str(point))
    # point = pul.getT12(pulse[0], flt.distinguish(pulseStd))
    # print("T12 = " + str(point))
    folders = files.getDir(path)
    cl = stdClassify(path, folders)
    test, train = makeSets(data, perc=80)
