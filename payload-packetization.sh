hadoop fs -rm /commoncrawl/small.warc
hadoop fs -put crawl-data/small.warc /commoncrawl/small.warc
head -n 100000 "/home/ubuntu//dis_materials/crawl-data/CC-MAIN-2014-35/segments/1408500800168.29/warc/CC-MAIN-20140820021320-00000-ip-10-180-136-8.ec2.internal.warc" > crawl-data/small.warc

