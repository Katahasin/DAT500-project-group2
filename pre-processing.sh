hadoop fs -rm -r hdfs:///dis_materials/outputs/output2
python3 MRpreProcess.py --hadoop-streaming-jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -r hadoop hdfs:///commoncrawl/small.warc --output-dir hdfs:///dis_materials/outputs/output2 --no-cat-output
