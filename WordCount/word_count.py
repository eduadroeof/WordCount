import boto
import time
import datetime

from boto.emr.step import StreamingStep


def word_count(instances):

    # Connect to AWS
    ec2 = boto.connect_ec2()
    max_number_instances = 20
    instances_occupied = 0

    # Check if this job will have instances to work
    while True:

        # Get all occupied instances
        all_instances = ec2.get_all_instances();
        instances_occupied = len(all_instances)

        # Remove instances that are enable to be used
        for r in all_instances:
            if r.instances[0].state == 'terminated':
                instances_occupied -= 1

        # Check if the number of instances running plus instances requested is less or equal to the max number of instances
        if instances_occupied + instances <= max_number_instances:
            break

        print 'Waiting for instances...'
        time.sleep(60.0)
        instances_occupied = 0

    sleep_time = 5.0
    print_time = sleep_time * 10

    # Create a step
    step = StreamingStep(name='jobflow_eof',
                         mapper='s3n://elasticmapreduce/samples/wordcount/wordSplitter.py',
                         reducer='aggregate',
                         input='s3n://eof-bucket/input',
                         output='s3n://eof-bucket/output/wordcount_instances-' + str(instances) + '_' + str(datetime.datetime.today()))

    # Connect to amazon mapreduce
    connection = boto.connect_emr()

    # Run jobflow
    job_id = connection.run_jobflow(name='wordcount_' + str(datetime.datetime.today()),
                                    log_uri='s3://eof-bucket/jobflow_logs',
                                    steps=[step],
                                    num_instances=instances)

    time_start = datetime.datetime.today()

    # Check if intances string needs to be in the singular
    instance_string = 'instance'
    if instances > 1:
        instance_string += 's'

    print 'Job State with ' + str(instances) + ' ' + instance_string + ':'
    job_state = ''
    i_print = 30

    # Print job status while it didn't complete or fail
    while(job_state != 'COMPLETED' and job_state != 'FAILED'):

        # Get job state
        job_state = connection.describe_jobflow(job_id).state

        # Print job state in some seconds
        if i_print == print_time:
            print str(datetime.datetime.today()) + ' - ' + job_state
            i_print = 0

        time.sleep(sleep_time)
        i_print += sleep_time

    print str(datetime.datetime.today()) + ' - ' + job_state + '\n'
    return 'DONE'
