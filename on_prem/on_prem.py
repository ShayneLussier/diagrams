from diagrams import Diagram, Cluster, Edge

from diagrams.onprem.analytics import (
    Dbt, Spark, Tableau, PowerBI, Flink)
from diagrams.onprem.database import MongoDB, PostgreSQL
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.queue import Kafka
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.container import Docker
from diagrams.saas.analytics import Snowflake, Stitch
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Redshift
from diagrams.gcp.analytics import BigQuery

from diagrams.generic.storage import Storage
from diagrams.generic.blank import Blank
from diagrams.programming.flowchart import SummingJunction

blank = Edge(color="#FFFFFF00")

with Diagram("On-premise Architecture", show=False, outformat="png", direction="LR"):

    with Cluster("Data Sources"):
        rdbms = PostgreSQL("PostgreSQL")
        nosql = MongoDB("MongoDB")
        other = Storage("Other")
    
    with Cluster("Ingestion"):
        with Cluster("Batch"):
            talend = SummingJunction("Talend")
            informatica = SummingJunction("Informatica")
            stitch = Stitch("Stitch")
            talend - blank - informatica - blank - stitch

        with Cluster("Streaming"):
            kafka = Kafka("Kafka")
            flink = Flink("Flink")
            spark = Spark("Spark")
            kafka - blank - flink - blank - spark
    
    with Cluster("Data Lake"):
        with Cluster("Staging Layer"):
            s3_staging = S3("S3")
        with Cluster("Processed Layer"):
            s3_processed = S3("S3")

    with Cluster("Data Catalogue"):
        atlation = SummingJunction("Atlation")

    with Cluster("Transformations"):
        spark2 = Spark("Spark")
        dbt = Dbt("dbt")
    
    with Cluster("Data Warehouse"):
        snowflake = Snowflake("Snowflake")
        redshift = Redshift("Redshift")
        big_query = BigQuery("BigQuery")
        snowflake - blank - redshift - blank - big_query

    with Cluster("Analytics"):
        power_bi = PowerBI("Power BI")
        tableau = Tableau("Tableau")
        power_bi - blank - tableau

    with Cluster("Orchestration"):
        airflow = Airflow("Airflow")
        luigi = SummingJunction("Luigi")
        airflow - Edge(color="#FFFFFF00") - luigi
    
    with Cluster("Monitoring"):
        grafana = Grafana("Grafana")
        grafana << Prometheus("Prometheus")

    rdbms >> talend
    stitch >> s3_staging
    nosql >> kafka
    spark >> s3_staging >> spark2
    s3_processed << dbt >> snowflake
    s3_processed << atlation << power_bi
    tableau << big_query


    luigi - blank - grafana