from pyspark.sql.functions import explode, col

# Step 1: Add "Plan_ID" while keeping all columns
dental_info_df = dental_info_df.withColumn("Plan_ID", explode(col("networkcode")))

# Step 2: Filter based on "Plan_ID"
dental_info_df = dental_info_df.filter(dental_info_df["Plan_ID"].isin(["CD005", "CP023", "PA027"]))

# Step 3: Drop "Plan_ID" after filtering
dental_info_df = dental_info_df.drop("Plan_ID")

# Show the final DataFrame
dental_info_df.show(10, truncate=False)


from pyspark.sql.functions import col, when, row_number
from pyspark.sql.window import Window

# Define your 6 target columns (replace with actual column names)
target_cols = ["col1", "col2", "col3", "col4", "col5", "col6"]

# Build the non-null count expression inline
non_null_expr = sum(when(col(c).isNotNull(), 1).otherwise(0) for c in target_cols)

# Apply window and filtering in one go
window_spec = Window.partitionBy("npi").orderBy(non_null_expr.desc())

# Add row number and filter only top 1 per NPI
dental_info_df = (
    dental_info_df
    .withColumn("rn", row_number().over(window_spec))
    .filter("rn = 1")
    .drop("rn")
)



from pyspark.sql.functions import col, when, row_number
from pyspark.sql.window import Window

# Your 6 target columns
target_cols = ["col1", "col2", "col3", "col4", "col5", "col6"]

# Build expression to count non-null values
non_null_expr = sum(when(col(c).isNotNull(), 1).otherwise(0) for c in target_cols)

# Inline conditional partitioning logic inside the window spec
window_spec = Window.partitionBy(
    when(col("npi").isNotNull(), col("npi")).otherwise(col("providerId"))
).orderBy(non_null_expr.desc())

# Apply row_number and filter top row per group
dental_info_df = (
    dental_info_df
    .withColumn("rn", row_number().over(window_spec))
    .filter("rn = 1")
    .drop("rn")
)



