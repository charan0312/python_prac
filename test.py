SELECT DISTINCT pl.*,
  CASE
    WHEN sdl.ExternalCode IS NULL THEN 'Record Missing in OSS'
    
    WHEN COALESCE(a.LineNumber1, '') <> COALESCE(sdla.Address1, '') THEN 'Address Not matching in OSS'

    WHEN COALESCE(
           CASE 
             WHEN TRIM(UPPER(pl.TwentyFourHourCoverage)) = 'Y' THEN '1'
             WHEN TRIM(UPPER(pl.TwentyFourHourCoverage)) = 'N' THEN '0'
             ELSE ''
           END, ''
         ) 
         <> COALESCE(CAST(sdls.isopen24hours AS VARCHAR(1)), '') THEN '24-Hour Coverage Not matching in OSS'
         
  END AS comments
