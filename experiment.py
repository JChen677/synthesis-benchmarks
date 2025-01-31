#originally authored by Huajun Guo (many thanks!), edited by Andreas Katis

import os, subprocess, sys, glob, shutil, csv, getopt
import numpy as np
import matplotlib.pyplot as plt
#
# Configuration
#
compaction = False
jkind_jar = None
smtlib2c_jar = None

EXPERIMENTS_DIR = 'verification'
PUSH_PATH = 'kind'
ANOTHER_PUSH_PATH = 'fixpoint'
YAPP = 'fixpointwithcompaction'
IMPLEMENT_DIR = 'verification/kind'
ANOTHER_IMPLEMENT_DIR = 'verification/fixpoint'
YAID = 'verification/fixpointwithcompaction'

SECOND_EXPERIMENTS_DIR = 'smaccm'
SECOND_IMPLEMENT_DIR = 'smaccm/kind'
SECOND_ANOTHER_IMPLEMENT_DIR = 'smaccm/fixpoint'
YASID = 'smaccm/fixpointwithcompaction'

THIRD_EXPERIMENTS_DIR = 'other'
THIRD_IMPLEMENT_DIR = 'other/kind'
THIRD_ANOTHER_IMPLEMENT_DIR = 'other/fixpoint'
YATID = 'other/fixpointwithcompaction'

FOURTH_EXPERIMENTS_DIR = 'fixpoint_only'
FOURTH_IMPLEMENT_DIR = 'fixpoint_only/kind'
FOURTH_ANOTHER_IMPLEMENT_DIR = 'fixpoint_only/fixpoint'
YAFID = 'fixpoint_only/fixpointwithcompaction'

NestList_overhead = []
NestList_size = []
NestList_size_compaction = []
NestList_size_name = []
NestList_size_name_verification = []
NestList_size_name_smaccm = []
NestList_size_name_other = []
NestList_size_name_fixpoint_only = []
NestList_performance = []

#delete all previous files except lus files in subfolder
def deleteFile_in_subfolder(folder, lus_files):
    os.chdir(folder)

    cfileList = glob.glob("*.c")
    hfileList = glob.glob("*.h")
    ofileList = glob.glob("*.o")
    sfileList = glob.glob("*.smt2")
    txtfileList = glob.glob("*.txt")

    if (len(cfileList)!=0):
        for f in cfileList:
            os.remove(f)

    if (len(hfileList)!=0):
        for h in hfileList:
            os.remove(h)

    if (len(ofileList)!=0):
        for o in ofileList:
            os.remove(o)

    if (len(sfileList)!=0):
        for s in sfileList:
            os.remove(s)

    if (len(txtfileList)!=0):
        for txt in txtfileList:
            os.remove(txt)

    if (len(lus_files)!=0):
        for lus in lus_files:
            if (os.path.isfile(os.path.splitext(lus)[0])):
                os.remove(os.path.splitext(lus)[0])

    os.chdir("..")

#delete files in each folder except lus
def deleteFile_in_folder():
    lus_files = glob.glob("*.lus")
    deleteFile_in_subfolder("fixpointwithcompaction", lus_files)
    deleteFile_in_subfolder("kind", lus_files)
    deleteFile_in_subfolder("fixpoint", lus_files)

#delete files in synthesis-benchmark folder except lus
def deleteAll():
    txtfileList = glob.glob("*.txt")
    # pdffileList = glob.glob("*.pdf")
    csvfileList = glob.glob("*.csv")

    if (len(txtfileList)!=0):
        for txt in txtfileList:
            os.remove(txt)

    # if (len(pdffileList)!=0):
    #     for pdf in pdffileList:
    #         os.remove(pdf)

    if (len(csvfileList)!=0):
        for csv in csvfileList:
            os.remove(csv)

    os.chdir("verification")
    deleteFile_in_folder()
    os.chdir("..")

    os.chdir("smaccm")
    deleteFile_in_folder()
    os.chdir("..")

    os.chdir("other")
    deleteFile_in_folder()
    os.chdir("..")

    os.chdir("fixpoint_only")
    deleteFile_in_folder()
    os.chdir("..")


def run_realizability(file_path):
    args = ['java', '-jar', jkind_jar, '-jrealizability','-timeout', '10000', '-n', '1000000', file_path]
    with open("debug_jkind.txt", "a") as debug:
        debug.write("Running jkind with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")

def run_synthesis(file_path):
    args = ['java', '-jar', jkind_jar, '-jrealizability','-scratch', '-synthesis', '-timeout', '10000', '-n', '1000000', file_path]
#            '-scratch', '-fixpoint_T', '-timeout', '1000', '-n', '1000000', file_path]
    with open("debug_jkind.txt", "a") as debug:
        debug.write("Running jkind with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")

def run_fixpoint(file_path):
    args = ['java', '-jar', jkind_jar, '-jrealizability',
            '-fixpoint', '-timeout', '10000', '-n', '1000000', file_path]
    with open("debug_jkind.txt", "a") as debug:
        debug.write("Running jkind with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")


def run_fixpointwithcompaction(file_path):
    args = ['java', '-jar', jkind_jar, '-jrealizability',
            '-fixpoint', '-compact', '-timeout', '10000', '-n', '1000000', file_path]
    with open("debug_jkind.txt", "a") as debug:
        debug.write("Running jkind with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")


def run_realizability_synthesis(lus_file, experiments_dir):
    lus_path = os.path.join(experiments_dir, lus_file)
    run_realizability(lus_path)
    sys.stdout.write(".")
    sys.stdout.flush()

    lus_path = os.path.join(experiments_dir, lus_file)
    run_synthesis(lus_path)
    sys.stdout.write(".")
    sys.stdout.flush()

def run_last_fixpoint(lus_file, experiments_dir):
    lus_path = os.path.join(experiments_dir, lus_file)
    run_fixpoint(lus_path)
    sys.stdout.write(".")
    sys.stdout.flush()

def run_last_fixpointwithcompaction(lus_file, experiments_dir):
    lus_path = os.path.join(experiments_dir, lus_file)
    run_fixpointwithcompaction(lus_path)
    sys.stdout.write(".")
    sys.stdout.flush()

def move_impl(outpath, experiments_dir):
    impl_files = glob.glob("*_skolem.smt2")
    if len(impl_files) == 0:
        print("No implement files found in '" + experiments_dir + "' directory")
        sys.exit(-1)

    for i, impl_file in enumerate(impl_files):
        old_implPath = impl_file
        new_implPath = os.path.join(outpath, impl_file)
        shutil.move(old_implPath, new_implPath)

    #remove dummy smt2files
    smt_files = glob.glob("*.smt2")
    if (len(smt_files)!=0):
        for i, smt_file in enumerate(smt_files):
            os.remove(smt_file)


def run_smtlib2c(impl_file, implement_dir):
    file_path = os.path.join(implement_dir, impl_file)
    args = ['java', '-jar', smtlib2c_jar,
            '-iter', '1000000',
            '-c_harness', '-lustrec_harness', '-lustrecnode', 'top', file_path]
    with open(implement_dir+"/debug_smtlib2c.txt", "a") as debug:
        debug.write("Running SMTLib2C with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")


def run_makefile(file_path):
    args = ['make', 'FILE='+file_path]
    with open("debug_make.txt", "a") as debug:
        debug.write("Running make for file: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")


def run_executables(file_path):
    args = ['./'+file_path]
    with open("results.txt", "a") as debug:
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()


def getMax(nList):
    sList1 = sorted(nList, key=lambda x: float(x[1]))
    sList2 = sorted(nList, key=lambda x: float(x[2]))
    if (sList1[-1][1] >= sList2[-1][2]):
        return sList1[-1][1]
    else:
        return sList2[-1][2]


def parse(target, output):
    with open(target,'r') as f:
        with open(output, 'a') as op:
            for line in f:
                if ("REALIZABLE" in line):
                    op.write(line)

    op.close()
    f.close()


def writeOverhead(nestList, tempOverhead):
    with open(tempOverhead,'r') as f:
        count = 0
        index = 0
        for line in f:
            lst = line.split(" ")
            time = lst[-1].replace("s","").strip()
            m = 0
            h = 0
            if ("m" in lst[-2]):
                m = float(lst[-2].replace("m","")) * 60
            if ("h" in lst[-3]):
                h = float(lst[-3].replace("h","")) * 60 * 60

            temp = float(time) + m + h
            time = str(temp)

            nestList[index].append(time)
            count = count + 1
            if (count==3):
                index = index+1
                count = 0

    f.close()


def drawOverhead():
    font = {'family' : 'normal','weight' : 'bold', 'size' : 20}
    plt.rc('font', **font)

    pl1 = np.array([float(j[1]) for j in sorted(NestList_overhead,key=lambda  x: float(x[3]))])
    pl2 = np.array([float(j[2]) for j in sorted(NestList_overhead,key=lambda  x: float(x[3]))])
    pl3 = np.array([float(j[3]) for j in sorted(NestList_overhead,key=lambda  x: float(x[3]))])

    fig = plt.figure()

    plt.scatter(pl2,pl3,c="r", s = 100,edgecolor= "")

    plt.yscale('log')
    plt.xscale('log')
    plt.axis([0,(float(getMax(NestList_overhead))+20),0,(float(getMax(NestList_overhead))+20)])
    plt.plot([0,(float(getMax(NestList_overhead))+20)],[0,(float(getMax(NestList_overhead))+20)])

    plt.xlabel("JSYN")
    plt.ylabel("JSYN-VG")
    plt.title("Performance(seconds)")
    plt.legend(loc = 'upper left')
    fig.savefig("overhead.pdf")

    #plt.yscale('log')
    #plt.ylim(pow(10,-1), pow(10,2.8))

    #synthesis = plt.plot(pl2,'-r^', label = 'JSYN', markersize = 10)
    #fixpoint = plt.plot(pl3,'-bo', label = 'JSYN-VG',  markersize = 10)

    #plt.xlabel("Model")
    #plt.ylabel("Performance(seconds)")
    #plt.legend(loc = 'upper left')
    #fig.savefig("overhead.pdf")



def measureSizeOfC(path, NestList_size_name_var):
    os.chdir(path)
    for cname in NestList_size_name_var:
        os.system('wc -l ' + cname[0] + ' |grep -v total >> loc.txt' )
    os.chdir("..")
    os.chdir("..")


def drawSize():
    font = {'family' : 'normal', 'weight' : 'bold', 'size' : 20}
    plt.rc('font', **font)

    pl1 = np.array([j[1] for j in sorted(NestList_size, key=lambda x: float(x[2]))])
    pl2 = np.array([j[2] for j in sorted(NestList_size, key=lambda x: float(x[2]))])
# Plot the results


    fig = plt.figure()

    
    plt.scatter(pl1,pl2,c="r", s = 100,edgecolor= "")
    plt.yscale('log')
    plt.xscale('log')

    plt.axis([0,(float(getMax(NestList_size))+200000),0,(float(getMax(NestList_size))+200000)])
    plt.plot([0,(float(getMax(NestList_size))+200000)],[0,(float(getMax(NestList_size))+200000)])

    plt.xlabel("JSYN")
    plt.ylabel("JSYN-VG")
    plt.title("Lines of Code")
    plt.legend(loc = 'upper left')
    fig.savefig("loc.pdf")

    
    #plt.yscale('log')
    #plt.ylim(pow(10,1), pow(10,3.5))
    #synthesized = plt.plot(pl1,'-r^', label = 'JSYN', markersize = 10)
    #fixpoint = plt.plot(pl2,'-bo', label = 'JSYN-VG', markersize = 7)

    #plt.xlabel("Model")
    #plt.ylabel("Lines of Code")
    #plt.legend(loc = 'upper left')
    #fig.savefig("loc.pdf")

def drawFixpointReducedSize():
    font = {'family' : 'normal', 'weight' : 'bold', 'size' : 20}
    plt.rc('font', **font)


    pl1 = np.array([j[1] for j in sorted(NestList_size_compaction, key=lambda x: float(x[2]))])
    pl2 = np.array([j[2] for j in sorted(NestList_size_compaction, key=lambda x: float(x[2]))])
# Plot the results


    fig = plt.figure()


    plt.scatter(pl1,pl2,c="r", s = 100,edgecolor= "")

    plt.yscale('log')
    plt.xscale('log')
    
    plt.axis([0,(float(getMax(NestList_size_compaction))+20),0,(float(getMax(NestList_size_compaction))+20)])
    plt.plot([0,(float(getMax(NestList_size_compaction))+20)],[0,(float(getMax(NestList_size_compaction))+20)])

    plt.xlabel("JSYN-VG w/ compaction")
    plt.ylabel("JSYN-VG")
    plt.title("Lines of Code")
    plt.legend(loc = 'upper left')
    fig.savefig("loccompact.pdf")

    #plt.yscale('log')
    #plt.ylim(pow(10,1), pow(10,3.5))
    #synthesized = plt.plot(pl1,'-r^', label = 'JSYN-VG w/ compaction', markersize = 10)
    #fixpoint = plt.plot(pl2,'-bo', label = 'JSYN-VG', markersize = 7)

    #plt.xlabel("Model")
    #plt.ylabel("Lines of Code")
    #plt.legend(loc = 'upper left')
    #fig.savefig("loc.pdf")



def combineSizeTxt(file1, file2):
    global compaction
    with open(file1, "r") as f1:
        count= 0
        for line1 in f1:
            tempList1 = []
            lst = line1.strip().split(" ")

            tempList1.append(lst[1])
            tempList1.append(lst[0])

            with open(file2, "r") as f2:
                for line2 in f2:
                    tempList2 = line2.strip().split(" ")
                    if (tempList2[1] == tempList1[0]):
                        tempList1.append(tempList2[0])

            if compaction:
                NestList_size_compaction.append(tempList1)
            else:
                NestList_size.append(tempList1)

    f1.close()
    f2.close()

#same folder
def combineResultTxt(file1, file2):
    with open(file1, "r") as f1:
        count= 0
        for line1 in f1:
            tempList1 = []
            lst = line1.strip().split(" ")

            tempList1.append(lst[0])
            tempList1.append(lst[1])

            with open(file2, "r") as f2:
                for line2 in f2:
                    tempList2 = line2.strip().split(" ")

                    if (tempList2[0] == tempList1[0]):
                        tempList1.append(tempList2[1])

            NestList_performance.append(tempList1)


    f1.close()
    f2.close()


def drawPerformance():
    font = {'family' : 'normal','weight' : 'bold','size' : 20}
    plt.rc('font', **font)

    pl1 = np.array([float(j[1]) for j in NestList_performance])
    pl2 = np.array([float(j[2]) for j in NestList_performance])

    fig = plt.figure()

    plt.scatter(pl1,pl2,c="r", s = 100,edgecolor= "")
    plt.axis([0,(float(getMax(NestList_performance))+20),0,(float(getMax(NestList_performance))+20)])
    plt.plot([0,(float(getMax(NestList_performance))+20)],[0,(float(getMax(NestList_performance))+20)])

    plt.xlabel("JSYN")
    plt.ylabel("JSYN-VG")
    plt.title("Performance(milliseconds)")
    plt.legend(loc = 'upper left')
    fig.savefig("performance.pdf")



def writeCSV():
    if compaction:
        with open("locListCompaction.csv", "wb") as kc:
            writer = csv.writer(kc)
            writer.writerows(NestList_size_compaction)
        kc.close()
    else:
        with open("overheadList.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(NestList_overhead)
        f.close()
        with open("locList.csv", "wb") as k:
            writer = csv.writer(k)
            writer.writerows(NestList_size)
        k.close()
        with open("performanceList.csv", "wb") as p:
           writer = csv.writer(p)
           writer.writerows(NestList_performance)
        p.close()


################################################################################################
################################################################################################
################################################################################################

# Gather Lustre files

def execute(experiments_dir, push_path, another_push_path, implement_dir, another_implement_dir, NestList_size_name_var):
    global compaction
    if not os.path.exists(experiments_dir):
        print("'" + experiments_dir + "' directory does not exist")
        sys.exit(-1)
    os.chdir(experiments_dir)
    lus_files = glob.glob("*.lus")
    if len(lus_files) == 0:
        print("No Lustre files found in '" + experiments_dir + "' directory")
        sys.exit(-1)
    os.chdir("..")

#
# Find jkind.jar

    print("")
    print("====Running Jkind under " + experiments_dir + "===")
    print("")

#execute...................................................
    with open("lustreName.txt", "a") as file:
        if ((len(sys.argv)>1) and (sys.argv[1] == "-skipjkind")):
            print("skip the jkind")
            for i, lus_file in enumerate(lus_files):
                empty = []
                empty.append(lus_file)
                NestList_overhead.append(empty)


        else:
            for i, lus_file in enumerate(lus_files):
                empty = []
                empty.append(lus_file)
                NestList_overhead.append(empty)  # set the name of file

                file.write(lus_file+"\n")

                sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
                sys.stdout.flush()

                if compaction:
                    run_last_fixpointwithcompaction(lus_file, experiments_dir)
                else:
                    run_realizability_synthesis(lus_file, experiments_dir)
                
                os.chdir(experiments_dir)
                move_impl(push_path, experiments_dir)
                os.chdir("..")

                run_last_fixpoint(lus_file, experiments_dir)
                os.chdir(experiments_dir)
                move_impl(another_push_path, experiments_dir)
                os.chdir("..")


                sys.stdout.write("]\n")
                sys.stdout.flush()


    file.close()


#execute run_smtlib2c in kind

    if not os.path.exists(implement_dir):
        print("'" + implement_dir + "' directory does not exist")
        sys.exit(-1)
    os.chdir(implement_dir)
    impl_files = glob.glob("*_skolem.smt2")
    if len(impl_files) == 0:
        print("No Skolem files found in '" + implement_dir + "' directory")
        sys.exit(-1)
    os.chdir("..")
    os.chdir("..")


    print("")
    print("====Running smtlib2c under " + implement_dir + "===")
    print("")


    for i, impl_file in enumerate(impl_files):
        sys.stdout.write("({} of {}) {} [".format(i+1, len(impl_files), impl_file))
        sys.stdout.flush()
        run_smtlib2c(impl_file, implement_dir)
        sys.stdout.write(".")
        sys.stdout.flush()
        sys.stdout.write("]\n")
        sys.stdout.flush()


#execute run_smtlib2c in fixpoint

    if not os.path.exists(another_implement_dir):
        print("'" + another_implement_dir + "' directory does not exist")
        sys.exit(-1)
    os.chdir(another_implement_dir)
    impl_files = glob.glob("*_skolem.smt2")
    if len(impl_files) == 0:
        print("No Skolem files found in '" + another_implement_dir + "' directory")
        sys.exit(-1)
    os.chdir("..")
    os.chdir("..")


    print("")
    print("====Running run_smtlib2c under " + another_implement_dir + "===")
    print("")



    for i, impl_file in enumerate(impl_files):
        sys.stdout.write("({} of {}) {} [".format(i+1, len(impl_files), impl_file))
        sys.stdout.flush()
        run_smtlib2c(impl_file, another_implement_dir)
        sys.stdout.write(".")
        sys.stdout.flush()
        sys.stdout.write("]\n")
        sys.stdout.flush()


    if not os.path.exists(experiments_dir):
        print("'" + experiments_dir + "' directory does not exist")
        sys.exit(-1)
    os.chdir(experiments_dir)
    lus_files = glob.glob("*.lus")
    if len(lus_files) == 0:
        print("No Lustre files found in '" + experiments_dir + "' directory")
        sys.exit(-1)
    os.chdir("..")



#execute run_make in kind..................................

    print("")
    print("====Running Makefile under " + implement_dir + "===")
    print("")

    os.chdir(implement_dir)
    for i, lus_file in enumerate(lus_files):
        sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
        sys.stdout.flush()
        run_makefile(os.path.splitext(lus_file)[0])
        sys.stdout.write(".")
        sys.stdout.flush()
        sys.stdout.write("]\n")
        sys.stdout.flush()


#execute run_make in fixpoint..................................
    os.chdir("..")
    os.chdir("..")

    print("")
    print("====Running Makefile under " + another_implement_dir + "===")
    print("")

    os.chdir(another_implement_dir)
    for i, lus_file in enumerate(lus_files):
        sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
        sys.stdout.flush()
        run_makefile(os.path.splitext(lus_file)[0])
        sys.stdout.write(".")
        sys.stdout.flush()
        sys.stdout.write("]\n")
        sys.stdout.flush()

    os.chdir("..")
    os.chdir("..")

    if not os.path.exists(experiments_dir):
        print("'" + experiments_dir + "' directory does not exist")
        sys.exit(-1)
    os.chdir(experiments_dir)
    lus_files = glob.glob("*.lus")
    if len(lus_files) == 0:
        print("No Lustre files found in '" + experiments_dir + "' directory")
        sys.exit(-1)
    os.chdir("..")


#run executable in kind .........................
    print("")
    print("====Running Executable under " + implement_dir + "===")
    print("")


    os.chdir(implement_dir)

    for i, lus_file in enumerate(lus_files):
        sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
        sys.stdout.flush()
        run_executables(os.path.splitext(lus_file)[0])

        empty = []
        empty.append(os.path.splitext(lus_file)[0]+".c")
        NestList_size_name_var.append(empty)


        sys.stdout.write(".")
        sys.stdout.flush()
        sys.stdout.write("]\n")
        sys.stdout.flush()

    os.chdir("..")
    os.chdir("..")


#run executable in fixpoint .........................
    print("")
    print("====Running Executable under " + another_implement_dir + "===")
    print("")

    os.chdir(another_implement_dir)

    for i, lus_file in enumerate(lus_files):
        sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
        sys.stdout.flush()
        run_executables(os.path.splitext(lus_file)[0])

        sys.stdout.write(".")
        sys.stdout.flush()
        sys.stdout.write("]\n")
        sys.stdout.flush()

    os.chdir("..")
    os.chdir("..")




#################################################################################################
#################################################################################################
#################################################################################################

def main(argv):
    global jkind_jar
    global smtlib2c_jar
    global compaction
    try:
      opts, args = getopt.getopt(argv,"c",[])
    except getopt.GetoptError:
      print 'experiment.py -c'
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-c':
            compaction = True
    path = os.environ.get("JKIND_HOME") or os.environ.get("PATH") or os.environ.get("path")

    for dir in path.split(':'):
        jar = os.path.join(dir, "jkind.jar")
        if os.path.exists(jar):
            jkind_jar = jar
            break
    if jkind_jar is None:
        print("Unable to find jkind.jar in JKIND_HOME or PATH environment variables")
        sys.exit(-1)
    print("Using JKind: " + jkind_jar)


    path = os.environ.get("PATH") or os.environ.get("path")

    for dir in path.split(':'):
        jar = os.path.join(dir, "SMTLib2C.jar")
        if os.path.exists(jar):
            smtlib2c_jar = jar
            break
    if smtlib2c_jar is None:
        print("Unable to find SMTLib2C.jar in PATH environment variables")
        sys.exit(-1)

    print("Using SMTLib2C: " + smtlib2c_jar)



    #################################################################################
    print("deleting the remained files")
    if ((len(sys.argv)>1) and (sys.argv[1] == "-skipjkind")):
        print("skip the jkind")

    else:
        deleteAll()

    ##############################################################
    if compaction:
        execute(EXPERIMENTS_DIR, YAPP, ANOTHER_PUSH_PATH, YAID, ANOTHER_IMPLEMENT_DIR, NestList_size_name_verification)
        execute(SECOND_EXPERIMENTS_DIR, YAPP, ANOTHER_PUSH_PATH, YASID, SECOND_ANOTHER_IMPLEMENT_DIR, NestList_size_name_smaccm)
        execute(THIRD_EXPERIMENTS_DIR, YAPP, ANOTHER_PUSH_PATH, YATID, THIRD_ANOTHER_IMPLEMENT_DIR, NestList_size_name_other)
        execute(FOURTH_EXPERIMENTS_DIR, YAPP, ANOTHER_PUSH_PATH, YAFID, FOURTH_ANOTHER_IMPLEMENT_DIR, NestList_size_name_fixpoint_only)

        #create both verification (kind and fixpoint) loc.txt
        measureSizeOfC(ANOTHER_IMPLEMENT_DIR, NestList_size_name_verification)
        measureSizeOfC(YAID, NestList_size_name_verification)
        #create both smaccm (kind and fixpoint) loc.txt
        measureSizeOfC(SECOND_ANOTHER_IMPLEMENT_DIR, NestList_size_name_smaccm)
        measureSizeOfC(YASID, NestList_size_name_smaccm)
        #create both other (kind and fixpoint) loc.txt
        measureSizeOfC(THIRD_ANOTHER_IMPLEMENT_DIR, NestList_size_name_other)
        measureSizeOfC(YATID, NestList_size_name_other)
        #create both fixpoint_only (kind and fixpoint) loc.txt
        measureSizeOfC(FOURTH_ANOTHER_IMPLEMENT_DIR, NestList_size_name_fixpoint_only)
        measureSizeOfC(YAFID, NestList_size_name_fixpoint_only)

        #append to NestList_size
        combineSizeTxt(YAID+"/loc.txt", ANOTHER_IMPLEMENT_DIR+"/loc.txt")
        combineSizeTxt(YASID+"/loc.txt", SECOND_ANOTHER_IMPLEMENT_DIR+"/loc.txt")
        combineSizeTxt(YATID+"/loc.txt", THIRD_ANOTHER_IMPLEMENT_DIR+"/loc.txt")
        combineSizeTxt(YAFID+"/loc.txt", FOURTH_ANOTHER_IMPLEMENT_DIR+"/loc.txt")

        print("NestList_size_compaction")
        print(NestList_size_compaction)

        drawFixpointReducedSize()
        print("")

        min_size_f_compaction = min(float(a[2]) for a in NestList_size_compaction)
        max_size_f_compaction = max(float(a[2]) for a in NestList_size_compaction)
        avg_size_f_compaction = sum([float(a[2]) for a in NestList_size_compaction])/len(NestList_size_compaction)

        print("min_size_f_compaction")
        print(min_size_f_compaction)
        print("max_size_f_compaction")
        print(max_size_f_compaction)
        print("avg_size_f_compaction")
        print(avg_size_f_compaction)
    
    else:        
        execute(EXPERIMENTS_DIR, PUSH_PATH, ANOTHER_PUSH_PATH, IMPLEMENT_DIR, ANOTHER_IMPLEMENT_DIR, NestList_size_name_verification)
        execute(SECOND_EXPERIMENTS_DIR, PUSH_PATH, ANOTHER_PUSH_PATH, SECOND_IMPLEMENT_DIR,SECOND_ANOTHER_IMPLEMENT_DIR, NestList_size_name_smaccm)
        execute(THIRD_EXPERIMENTS_DIR, PUSH_PATH, ANOTHER_PUSH_PATH, THIRD_IMPLEMENT_DIR,THIRD_ANOTHER_IMPLEMENT_DIR, NestList_size_name_other)
        #fill the NestList_overhead
        parse("debug_jkind.txt", "overhead.txt")
        writeOverhead(NestList_overhead, "overhead.txt")
        drawOverhead()
        print("NestList_overhead")
        print(NestList_overhead)
        print("")

        #create both verification (kind and fixpoint) loc.txt
        measureSizeOfC(IMPLEMENT_DIR, NestList_size_name_verification)
        measureSizeOfC(ANOTHER_IMPLEMENT_DIR, NestList_size_name_verification)
        #create both smaccm (kind and fixpoint) loc.txt
        measureSizeOfC(SECOND_IMPLEMENT_DIR, NestList_size_name_smaccm)
        measureSizeOfC(SECOND_ANOTHER_IMPLEMENT_DIR, NestList_size_name_smaccm)
        #create both other (kind and fixpoint) loc.txt
        measureSizeOfC(THIRD_IMPLEMENT_DIR, NestList_size_name_other)
        measureSizeOfC(THIRD_ANOTHER_IMPLEMENT_DIR, NestList_size_name_other)

        #append to NestList_size
        combineSizeTxt(IMPLEMENT_DIR+"/loc.txt", ANOTHER_IMPLEMENT_DIR+"/loc.txt")
        combineSizeTxt(SECOND_IMPLEMENT_DIR+"/loc.txt", SECOND_ANOTHER_IMPLEMENT_DIR+"/loc.txt")
        combineSizeTxt(THIRD_IMPLEMENT_DIR+"/loc.txt", THIRD_ANOTHER_IMPLEMENT_DIR+"/loc.txt")

        print("NestList_size")
        print(NestList_size)

        drawSize()
        print("")

        #append to NestList_performance
        combineResultTxt(IMPLEMENT_DIR+"/results.txt",ANOTHER_IMPLEMENT_DIR+"/results.txt")
        combineResultTxt(SECOND_IMPLEMENT_DIR+"/results.txt",SECOND_ANOTHER_IMPLEMENT_DIR+"/results.txt")
        combineResultTxt(THIRD_IMPLEMENT_DIR+"/results.txt",THIRD_ANOTHER_IMPLEMENT_DIR+"/results.txt")


        print("NestList_performance")
        print(NestList_performance)

        drawPerformance()

        writeCSV()

        min_performance_s = min(float(a[1]) for a in NestList_performance)
        max_performance_s = max(float(a[1]) for a in NestList_performance)
        avg_performance_s = sum([float(a[1]) for a in NestList_performance])/len(NestList_performance)

        min_performance_f = min(float(a[2]) for a in NestList_performance)
        max_performance_f = max(float(a[2]) for a in NestList_performance)
        avg_performance_f = sum([float(a[2]) for a in NestList_performance])/len(NestList_performance)

        min_overhead_s = min(float(a[2]) for a in NestList_overhead)
        max_overhead_s = max(float(a[2]) for a in NestList_overhead)
        avg_overhead_s = sum([float(a[2]) for a in NestList_overhead])/len(NestList_overhead)

        min_overhead_f = min(float(a[3]) for a in NestList_overhead)
        max_overhead_f = max(float(a[3]) for a in NestList_overhead)
        avg_overhead_f = sum([float(a[3]) for a in NestList_overhead])/len(NestList_overhead)

        min_size_s = min(float(a[1]) for a in NestList_size)
        max_size_s = max(float(a[1]) for a in NestList_size)
        avg_size_s = sum([float(a[1]) for a in NestList_size])/len(NestList_size)

        min_size_f = min(float(a[2]) for a in NestList_size)
        max_size_f = max(float(a[2]) for a in NestList_size)
        avg_size_f = sum([float(a[2]) for a in NestList_size])/len(NestList_size)


        print("min_performance_s")
        print(min_performance_s)
        print("max_performance_s")
        print(max_performance_s)
        print("avg_performance_s")
        print(avg_performance_s)

        print("min_performance_f")
        print(min_performance_f)
        print("max_performance_f")
        print(max_performance_f)
        print("avg_performance_f")
        print(avg_performance_f)

        print("min_overhead_s")
        print(min_overhead_s)
        print("max_overhead_s")
        print(max_overhead_s)
        print("avg_overhead_s")
        print(avg_overhead_s)

        print("min_overhead_f")
        print(min_overhead_f)
        print("max_overhead_f")
        print(max_overhead_f)
        print("avg_overhead_f")
        print(avg_overhead_f)

        print("min_size_s")
        print(min_size_s)
        print("max_size_s")
        print(max_size_s)
        print("avg_size_s")
        print(avg_size_s)

        print("min_size_f")
        print(min_size_f)
        print("max_size_f")
        print(max_size_f)
        print("avg_size_f")
        print(avg_size_f)

if __name__ == '__main__':
    main(sys.argv[1:])