from pyspark.sql.functions import explode, col

# Step 1: Add "Plan_ID" while keeping all columns
dental_info_df = dental_info_df.withColumn("Plan_ID", explode(col("networkcode")))

# Step 2: Filter based on "Plan_ID"
dental_info_df = dental_info_df.filter(dental_info_df["Plan_ID"].isin(["CD005", "CP023", "PA027"]))

# Step 3: Drop "Plan_ID" after filtering
dental_info_df = dental_info_df.drop("Plan_ID")

# Show the final DataFrame
dental_info_df.show(10, truncate=False)
