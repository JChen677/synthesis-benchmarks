import csv
import getopt
import glob
import numpy as np
import os
import shutil
import subprocess
import sys

jsynBench = ["box", "diagonal", "evasion", "follow", "limitedbox", "solitarybox", "square", "cinderella"]
dtBench = ["boxGame", "diagonalGame", "evasion_Paper", "follow_Paper", "limited_diagonal", "solitaryBoxGame", "square"]

def parseJSynRet(jsyn):
	timeStart = jsyn.find("Time = ")
	if (timeStart < 0): #Error: No time value found
		return -1
	timeEnd = jsyn.find("s", timeStart)
	timeVal = jsyn[timeStart + 7:timeEnd]
	return float(timeVal)

def parseDTRet(dt):
	timeStart = dt.find("Total computation time")
	if (timeStart < 0): #Error: No time value found
		return -1
	timeEnd = dt.find("milliseconds", timeStart)
	timeVal = dt[timeStart + 24:timeEnd - 1]
	return float(timeVal) / 1000 #Convert to seconds

def main():
	#Run Jsyn benchmarks
	os.chdir("../jsyn")
	debug = open("debug.txt", "w")
	jsynTimes = []
	for i in range(0, len(jsynBench)):
		args = ["jrealizability", "-timeout", "10000", "-fixpoint", "-synthesis", "-nondet", jsynBench[i] + ".lus"]
		debug.write("Run jkind with args {}\n".format(args))
		jsyn = subprocess.check_output(args)
		time = parseJSynRet(jsyn)
		jsynTimes.append(time)
	debug.close()

	#Run DT-Synth benchmarks
	os.chdir("../dtsynth")
	debug = open("debug.txt", "w")
	dtTimes = []
	for i in range(0, len(dtBench)):
		args = ["./main", dtBench[i] + ".json"]
		debug.write("Run DTSynth with args {}\n".format(args))
		dt = subprocess.check_output(args)
		time = parseDTRet(dt)
		dtTimes.append(time)

	#DTSynth has no cinderella file
	dtBench.append("cinderella")
	dtTimes.append("n/a")

	#Write results to data.csv
	os.chdir("../scripts")
	data = open("data.csv", "w")
	data.write("JSynth Benchmark\tTime(s)\t\tDTSynth Benchmark\tTime(s)\n")
	for i in range(0, len(jsynBench)):
		data.write("{jsBench}\t{jsTime}\t\t{dtBench}\t{dtTime}\n".format(jsBench = jsynBench[i], jsTime = jsynTimes[i], dtBench = dtBench[i], dtTime = dtTimes[i]))

if (__name__ == "__main__"):
	main()
