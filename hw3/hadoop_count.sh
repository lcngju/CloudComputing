hadoop \
        jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.1.2.jar \
        -file mapper.py -mapper mapper.py \
        -file reducer.py -reducer reducer.py \
        -input "wordcount/access_log.txt" \
        -output "ipcount_outdir"

