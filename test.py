SELECT 
    tst3.*, 
    COUNT(tst3.SpecialityName) OVER (PARTITION BY tst3.npi) AS cnt
FROM (
    SELECT 
        tst1.NPI, 
        tst1.qnxt_specialty, 
        tst2.NPI AS npi2, 
        tst2.SpecialityName
    FROM (
        SELECT 
            a.npi, 
            CASE 
                WHEN TRIM(a.qnxt_specialty) = '' THEN a.npiu2_concat
                ELSE CONCAT(CAST(a.npi AS VARCHAR(100)), '||', LOWER(TRIM(CAST(a.qnxt_specialty AS VARCHAR(100)))))
            END AS qnxt_specialty
        FROM (
            SELECT 
                CAST(npiu2.NPI AS VARCHAR(100)) AS NPI,
                CAST('' AS VARCHAR(100)) AS qnxt_specialty,
                CONCAT(CAST(npiu2.NPI AS VARCHAR(100)), '||A') AS npiu2_concat
            FROM HSLABCORNERSTONE.Directory_NPI_Universe npiu2

            UNION

            SELECT 
                CAST(npiu1.NPI AS VARCHAR(100)) AS NPI,
                CAST(npiu1.qnxt_specialty AS VARCHAR(100)) AS qnxt_specialty,
                CAST('' AS VARCHAR(100)) AS npiu2_concat
            FROM HSLABCORNERSTONE.Directory_NPI_Universe npiu1
        ) a
    ) tst1
    LEFT JOIN (
        SELECT 
            b.npi, 
            CASE 
                WHEN TRIM(b.SpecialityName) = '' THEN b.sdnu1_concat
                ELSE CONCAT(CAST(b.npi AS VARCHAR(100)), '||', LOWER(TRIM(CAST(b.SpecialityName AS VARCHAR(100)))))
            END AS SpecialityName
        FROM (
            SELECT 
                CAST(sdnu1.NPI AS VARCHAR(100)) AS NPI,
                CAST('' AS VARCHAR(100)) AS SpecialityName,
                CONCAT(CAST(sdnu1.NPI AS VARCHAR(100)), '||A') AS sdnu1_concat
            FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu1
            WHERE sdnu1.domainname = 'sPayer'

            UNION

            SELECT 
                CAST(sdnu2.NPI AS VARCHAR(100)) AS NPI,
                CAST(sdnu2.SpecialityName AS VARCHAR(100)) AS SpecialityName,
                CAST('' AS VARCHAR(100)) AS sdnu1_concat
            FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu2
            WHERE sdnu2.domainname = 'sPayer'
        ) b
    ) tst2
    ON tst1.qnxt_specialty = tst2.SpecialityName
) tst3
WHERE tst3.npi = '1003001256'
ORDER BY 1;
