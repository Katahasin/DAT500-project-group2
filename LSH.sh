hadoop fs -rm -r hdfs:///dis_materials/outputs/output9
hadoop  jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -input hdfs:///dis_materials/outputs/output8/part-00000 -output hdfs:///dis_materials/outputs/output9 -mapper MVtest.py -file MVtest.py
