SELECT * 
FROM (
    SELECT 
        CAST(sdnu.NPI AS VARCHAR(100)) AS NPI,
        CAST(sdnu.SpecialityName AS VARCHAR(100)) AS SpecialityName,
        CONCAT(CAST(sdnu.NPI AS VARCHAR(100)), '||', LOWER(TRIM(CAST(sdnu.SpecialityName AS VARCHAR(100))))) AS sdnu_concat
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu
    WHERE sdnu.domainname = 'sPayer'

    UNION

    SELECT 
        CAST(sdnu.NPI AS VARCHAR(100)) AS NPI,
        CAST(sdnu.SpecialityName AS VARCHAR(100)) AS SpecialityName,
        CONCAT(CAST(sdnu.NPI AS VARCHAR(100)), '||A') AS sdnu_concat
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu
    WHERE sdnu.domainname = 'sPayer'
) a
ORDER BY 1;
