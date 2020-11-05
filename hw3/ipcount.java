mport java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
public class ipcount {
    public static class ipCountMapper
            extends Mapper<Object, Text, Text, IntWritable>{

        private final static IntWritable plugOne  = new IntWritable(1);
        private Text word = new Text();
        @Override

        public void map(Object key, Text value, Context context
        ) throws IOException, InterruptedException {
            StringTokenizer st = new StringTokenizer(value.toString());
            while (st.hasMoreTokens()) {
                word.set(st.nextToken());

                context.write(word, plugOne);
                break;
            }
        }
    }
    public static class ipCountReducer
            extends Reducer<Text,IntWritable,Text,IntWritable> {

        private IntWritable result = new IntWritable();

        @Override

        public void reduce(Text key, Iterable<IntWritable> values,

                           Context context

        ) throws IOException, InterruptedException {

            int reduceSum = 0;

            for (IntWritable val : values) {

                reduceSum += val.get();

            }

            result.set(reduceSum);

            context.write(key, result);

        }

    }



    public static void main(String[] args) throws Exception {

        Configuration config = new Configuration();

        Job job = Job.getInstance(config, "hadoop ip count example");

        job.setJarByClass(ipcount.class);

        job.setReducerClass(ipCountReducer.class);

        job.setMapperClass(ipCountMapper.class);


        job.setCombinerClass(ipCountReducer.class);

        job.setOutputKeyClass(Text.class);

        job.setOutputValueClass(IntWritable.class);


        FileInputFormat.addInputPath(job, new Path(args[0]));


        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);

    }

}

