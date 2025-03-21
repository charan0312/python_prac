I want to filter out the dental_info_df on column documentId where the string contains ADP. Example: "documentId": "0079610!D0079610DHMOCD005216339",

import boto3
import logging
import time
import pyspark
import sys
import json
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession
from awsglue.dynamicframe import DynamicFrame
import pandas as pd
from s3fs import S3FileSystem
from datetime import datetime
from pyspark.sql.functions import from_unixtime,unix_timestamp,col,lit,udf,concat_ws,collect_set,regexp_extract,explode,regexp_replace,when,concat,substring
from pyspark.sql.types import IntegerType
import pandas
from sdirectoryCommonUtil import archive_s3_files
from pyspark.sql.functions import row_number
from pyspark.sql.window import Window
secrets_manager = boto3.client('secretsmanager')

args = getResolvedOptions(sys.argv, ["JOB_NAME", 'bucket', "processDate", "app_version","ECSR_number", "outbound_path","archive_path"])
# args = getResolvedOptions(sys.argv, ['JOB_NAME'])

job_name = args["JOB_NAME"]
bucket_name = args["bucket"]
app_version = args["app_version"]
processDate = args["processDate"]
dental_ecsr_number = json.loads(secrets_manager.get_secret_value(
    SecretId=args["ECSR_number"]
)['SecretString'])["ecsr_number"]
outbound_path = args["outbound_path"]
dest_key = args["archive_path"]

sc = SparkContext().getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(job_name, args)
s3_write = S3FileSystem()

job_date_dot = datetime.strptime(processDate, "%Y%m%d").strftime("%Y.%m.%d")
job_date_no_dashes = datetime.strptime(processDate, "%Y%m%d").strftime("%Y%m%d")
job_timestamp = datetime.strptime(processDate, "%Y%m%d").strftime("%Y-%m-%d-%H:%M:%S")
job_year = datetime.strptime(processDate, "%Y%m%d").strftime("%Y")


msg_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
datetime_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(format=msg_format, datefmt=datetime_format)
logger = logging.getLogger("DentistInformation")
logger.setLevel(logging.INFO)
logger.info(f"DentistInformationGenerator")

sparkParquetData = SparkSession.builder.appName("sDirectory Dental Job").getOrCreate()
log_group_name = "/aws-glue/jobs/gbs-dev2-sdirectory-dental-glue-job"


#File archival to archive folder

source_file = outbound_path[1:]
s3_client = boto3.client('s3')

archive_s3_files(bucket_name,source_file,dest_key,s3_client,logger)

#################### READING FILES ####################
##########
########## Reading dental JSON file
##########
json_dental_info_path ="s3://" + bucket_name + "/inbound/" + app_version + "/dental/" + job_date_no_dashes + "/"
json_dental_info_dyf = glueContext.create_dynamic_frame_from_options(
    "s3", format="json", connection_options={"paths": [json_dental_info_path]}
)
dental_info_df = json_dental_info_dyf.toDF()
dental_info_df.show(10, truncate=False)
dental_info_df = dental_info_df.select(
                                        substring(dental_info_df.locationId,1,100).alias("Location_External_Code"),
                                        dental_info_df.detail.product.locations[0].openHours.alias("openHours"),
                                        substring(dental_info_df.nationalProviderIdentifiers[0],1,100).alias("npi"),
                                        substring(dental_info_df.detail.product.locations[0].facilityName,1,100).alias("location_name"),
                                        substring(dental_info_df.detail.emailaddress,1,100).alias("emailaddress"),
                                        substring(dental_info_df.detail.product.locations[0].streetName,1,100).alias("addressLine1"),
                                        substring(dental_info_df.detail.product.locations[0].addressLine2,1,100).alias("addressLine2"),
                                        substring(dental_info_df.detail.product.locations[0].city,1,50).alias("city"),
                                        substring(dental_info_df.detail.product.locations[0].stateCode,1,50).alias("stateCode"),
                                        substring(dental_info_df.detail.product.locations[0].zipCode,1,5).alias("zipCode"),
                                        substring(dental_info_df.providerId,1,100).alias("providerId"),
                                        dental_info_df.acceptingNewPatientIndicator,
                                        substring(dental_info_df.detail.firstName,1,50).alias("firstName"),
                                        substring(dental_info_df.detail.middleInitial,1,50).alias("middleInitial"),
                                        substring(dental_info_df.detail.lastName,1,50).alias("lastName"),
                                        substring(dental_info_df.detail.gender.code,1,10).alias("gendercode"),
                                        dental_info_df.detail.product.locations[0].networkDetails.alias("networkdetails"),
                                        substring(dental_info_df.detail.product.locations[0].phones[0],1,15).alias("phones"),
                                        dental_info_df.detail.languages.alias("languages"),
                                        dental_info_df.detail.product.locations[0].licenses.licenseState.alias("LicenseState"),
                                        dental_info_df.detail.product.locations[0].licenses.license.alias("LicenseNumber"),
                                        dental_info_df.detail.product.specialties.alias("specialties"),
                                        dental_info_df.detail.schools[0].alias("schools"),
                                        substring(dental_info_df.detail.schoolGraduationYear,1,6).alias("endyear"),
                                        substring(dental_info_df.detail.degrees[0],1,100).alias("degrees"),
                                        explode(dental_info_df.specialtyDescriptions).alias("specialtiesgr"),
                                        dental_info_df.detail.product.locations[0].handicapAccessIndicator.alias("handicap"),
                                        substring(dental_info_df.detail.typeDescription,1,100).alias("type"), 
                                        substring(dental_info_df.detail.brighterProfileImageThumbNailURL,1,500).alias("image"),
                                        dental_info_df.detail.product.locations[0].acceptingNewPatientCode.alias("newpatient"),
                                        dental_info_df.detail.product.locations[0].acceptingNewPatientIndicator.alias("newpatientind"),
                                        dental_info_df.detail.product.locations[0].locationLevelParticipatingProducts.networkCode.alias("networkcode"),
                                        dental_info_df.boardCertificationFlag.alias("boardcertificationflag"),
                                        dental_info_df.primarySpecialtyCode,
                                        dental_info_df.adaCmplncIndicator.alias("adaindicator"),
                                        dental_info_df.documentId
                                    )
dental_info_df = dental_info_df.groupBy("Location_External_Code", "openHours", "npi", "location_name", "emailaddress", "addressLine1", "addressLine2",
                                        "city", "stateCode", "zipCode", "providerId", "acceptingNewPatientIndicator", "firstName", "middleInitial", "lastName",
                                        "genderCode","networkdetails","phones","languages","LicenseState","LicenseNumber","specialties", "schools",
                                        "endyear", "adaindicator", "degrees", "handicap", "type", "image" , "newpatient", "networkcode", "boardcertificationflag", "primarySpecialtyCode", "newpatientind", "documentId" )\
                                .agg(concat_ws('~', collect_set("specialtiesgr")).alias("specialtiesgr")).distinct()

dental_info_df.show(10, truncate=False)
