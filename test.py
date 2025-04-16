SELECT npiu.*,
       CASE
         WHEN NOT EXISTS (
             SELECT 1 FROM HSLABCORNERSTONE.PROV_SDIR_Provider sdp WHERE sdp.NPI = npiu.NPI
         ) THEN 'Record Missing in OSS'
         WHEN NOT EXISTS (
             SELECT 1 FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu
             WHERE sdnu.NPI = npiu.NPI
               AND LOWER(COALESCE(sdnu.SpecialityName, '')) = LOWER(COALESCE(npiu.qnxt_specialty, ''))
         ) THEN 'Specialty NOT matching in OSS'
       END AS comments
FROM HSLABCORNERSTONE.Directory_NPI_Universe npiu
