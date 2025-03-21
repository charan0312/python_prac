Fix this

dental_info_df = dental_info_df.select(explode(dental_info_df.networkcode).alias("Plan ID").filter("Plan ID".isin(["CD005", "CP023", "PA027"])))
