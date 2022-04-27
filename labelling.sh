hadoop fs -rm -r hdfs:///dis_materials/outputs/output8
hadoop  jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -input hdfs:///dis_materials/outputs/output2/part-00000 -output hdfs:///dis_materials/outputs/output8 -mapper email_count_mapper.py -file email_count_mapper.py -file badwords4.json
