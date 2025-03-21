from pyspark.sql.functions import explode

dental_info_df = (
    dental_info_df
    .select(explode(dental_info_df.networkcode).alias("Plan ID"))
    .filter(dental_info_df["Plan ID"].isin(["CD005", "CP023", "PA027"]))
)
