from diagrams import Diagram, Cluster, Edge

from diagrams.aws.analytics import (
    Glue, GlueCrawlers, GlueDataCatalog,
    KinesisDataFirehose, KinesisDataAnalytics, KinesisDataStreams,
    EMR, Athena, Quicksight, Redshift,) 
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, DDB
from diagrams.aws.integration import SF, Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.storage import S3

from diagrams.generic.storage import Storage

with Diagram("AWS Architecture", show=False, outformat="png", direction="LR"):

    with Cluster("Data Sources"):
        rds = RDS("Amazon RDS")
        ddb = DDB("DynamoDB")
        other = Storage("Other")
    
    with Cluster("Ingestion"):
        with Cluster("Batch"):
            lambda_aws = Lambda("AWS Lambda")
            glue = Glue("AWS Glue")
            emr = EMR("Amazon EMR")
            lambda_aws - glue - emr

        with Cluster("Streaming"):
            kinesis = KinesisDataFirehose("Kinesis Data Firehose")
            kinesis_streams = KinesisDataStreams("Kinesis Data Streams")
            kinesis_analytics = KinesisDataAnalytics("Kinesis Data Analytics")
            kinesis - kinesis_streams - kinesis_analytics
    
    with Cluster("Data Lake"):
        with Cluster("Staging Layer"):
            s3_staging = S3("AWS S3")
        with Cluster("Processed Layer"):
            s3_processed = S3("AWS S3")

    with Cluster("Data Catalogue"):
        glue_crawler = GlueCrawlers("Glue Crawler")
        glue_catalog = GlueDataCatalog("Glue Catalog")
        glue_crawler >> glue_catalog

    with Cluster("Transformations"):
        lambda_aws2 = Lambda("AWS Lambda")
        glue2 = Glue("AWS Glue")
        emr2 = EMR("Amazon EMR")
        lambda_aws2 - glue2 - emr2
    
    with Cluster("Data Warehouse"):
        redshift = Redshift("Amazon Redshift")

    with Cluster("Analytics"):
        athena = Athena("Amazon Athena")
        quicksight = Quicksight("Amazon Quicksight")
        athena << quicksight

    with Cluster("Orchestration"):
        glue_jobs = Glue("Glue Jobs")
        sf = SF("AWS Step Functions")
        eventbridge = Eventbridge("AWS Event Bridge")
        glue_jobs - sf - eventbridge
    
    with Cluster("Monitoring"):
        cloudwatch = Cloudwatch("Amazon CloudWatch")

    eventbridge - cloudwatch
    rds >> lambda_aws 
    ddb >> kinesis 
    emr >> s3_staging >> lambda_aws2
    kinesis_analytics >> s3_staging
    glue_crawler >> s3_processed << lambda_aws2
    glue_catalog << athena
    quicksight >> redshift << emr2