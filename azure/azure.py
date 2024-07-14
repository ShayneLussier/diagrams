from diagrams import Diagram, Cluster, Edge

from diagrams.azure.analytics import (
    Databricks, DataFactories, SynapseAnalytics,
    StreamAnalyticsJobs, EventHubs)
from diagrams.azure.compute import FunctionApps
from diagrams.azure.database import SQLDatabases, CosmosDb, DataLake
from diagrams.azure.integration import DataCatalog, LogicApps, EventGridTopics
from diagrams.azure.storage import BlobStorage

from diagrams.onprem.analytics import PowerBI
from diagrams.generic.storage import Storage
from diagrams.generic.blank import Blank

with Diagram("Azure Architecture", show=False, outformat="png", direction="LR"):

    with Cluster("Data Sources"):
        sql = SQLDatabases("SQLDatabases")
        cosmos = CosmosDb("CosmosDB")
        other = Storage("Other")
    
    with Cluster("Ingestion"):
        with Cluster("Batch"):
            function_app = FunctionApps("Function App")
            data_factories = DataFactories("Data Factories")
            databricks = Databricks("Databricks")
            function_app - data_factories - databricks

        with Cluster("Streaming"):
            stream_analytics = StreamAnalyticsJobs("Stream Analytics")
            eventhub = EventHubs("Event Hubs")
            eventhub - stream_analytics
    
    with Cluster("Data Lake"):
        with Cluster("Staging Layer"):
            blob_staging = BlobStorage("Blob Storage")
            data_lake_staging = DataLake("ADLS Gen2")
            blob_staging - data_lake_staging
        with Cluster("Processed Layer"):
            blob_processed = BlobStorage("Blob Storage")
            data_lake_processed = DataLake("ADLS Gen2")
            blob_processed - data_lake_processed

    with Cluster("Data Catalogue"):
        data_factories3 = DataFactories("Data Factories:\nData flow mapping")
        catalog = DataCatalog("Data Catalog")
        data_factories3 >> catalog

    with Cluster("Transformations"):
        function_app2 = FunctionApps("Function App")
        data_factories2 = DataFactories("Data Factories")
        databricks2 = Databricks("Databricks")
        function_app2 - data_factories2 - databricks2
    
    with Cluster("Data Warehouse"):
        synapse = SynapseAnalytics("Synapse Analytics")

    with Cluster("Analytics"):
        synapse2 = SynapseAnalytics("Synapse Analytics:\nSQL On-demand")
        power_bi = PowerBI("Power BI")
        synapse2 << power_bi

    with Cluster("Orchestration"):
        data_factories4 = DataFactories("Data Factories")
        logic_apps = LogicApps("Azure Logic Apps")
        event_grid = EventGridTopics("Event Grid")
        data_factories4 - logic_apps - event_grid
    
    with Cluster("Monitoring"):
        azure_monitor = Blank("Azure Monitor")

    sql >> function_app
    databricks >> blob_staging
    cosmos >> eventhub
    stream_analytics >> blob_processed
    data_lake_staging >> function_app2
    data_factories3 >> blob_processed
    data_lake_processed << function_app2
    catalog << synapse2 << power_bi >> synapse << databricks2
    event_grid - azure_monitor