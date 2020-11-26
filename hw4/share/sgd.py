
import random


# Add Spark Python Files to Python Path
import sys
import os
SPARK_HOME = "/opt/bitnami/spark" # Set this to wherever you have compiled Spark
os.environ["SPARK_HOME"] = SPARK_HOME # Add Spark path
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1" # Set Local IP
os.environ['JAVA_HOME'] = "/opt/bitnami/java/bin"
sys.path.append( SPARK_HOME + "/python") # Add python files to Python Path


from pyspark.mllib.classification import LogisticRegressionWithSGD
import numpy as np
from pyspark import SparkConf, SparkContext
from pyspark.mllib.regression import LabeledPoint





def iteration(X,Y,Wt, η):
    
    n=random.randint(0,len(X)-1)
    s=-Y[n]*Wt.dot(X[n])
    Wt=Wt+η/(1+np.exp(-s))*(Y[n]*(X[n]))
    
    return Wt

def SGD1(X,Y, epoch = 250000, η = 0.000001):

    Wt = np.zeros(X[0].shape)
    h=X.dot(Wt)-Y
    pre = (h.T.dot(h))/X.shape[0]
    best = pre

    for i in range(epoch):
        
        Wt = iteration(X,Y, Wt, η)
        h=X.dot(Wt)-Y
        Ein = (h.T.dot(h))/X.shape[0]
        # if (pre<Ein) and i>10000:
        #     print('break')
        #     break
        pre = Ein
        if best>Ein:
            best = Ein
        # if i%1000 == 0:
        #     print('Ein:', best)
        
    return best



def getSparkContext():
    """
    Gets the Spark Context
    """
    conf = (SparkConf()        
         .setMaster("local") # run on local
         .setAppName("Logistic Regression") # Name of App
         .set("spark.executor.memory", "1g")) # Set 1 gig of memory
    sc = SparkContext(conf = conf) 
    return sc

def mapper(line):
    """
    Mapper that converts an input line to a feature vector
    """    
    feats = line.strip().split(",") 
    # labels must be at the beginning for LRSGD
    
    features = [1.0] + [ float(feature) for feature in feats ] # need floats
    return np.array(features)

sc = getSparkContext()

# Load and parse the data
data = sc.textFile("/bitnami/spark/data_banknote_authentication.txt")
parsedData = np.array(data.map(mapper).collect())
# print(type(parsedData))




X = parsedData[:,:-1]
Y = parsedData[:,-1]

# Train model
Ein = SGD1(X,Y)

# Print some stuff
print("Training Error = " + str(Ein))







    
    