#from pyspark import SparkContext
#sc = SparkContext("local", "First App")
#
#logFile = "file:///C:/Users/athulrajputhalath/Downloads/spark-2.4.0-bin-hadoop2.7/README.md"
#logData = sc.textFile(logFile).cache()
#numAs = logData.filter(lambda s: 'a' in s).count()
#print(f"Lines with a:{numAs}")