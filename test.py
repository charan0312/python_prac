-- Full fallout classification using WHERE clause logic
SELECT 
    A.NPI,
    A.SpecialityName,
    'NPI Missing' AS COMMENT
FROM HSLABCORNERSTONE.Directory_NPI_Universe A
WHERE A.NPI NOT IN (
    SELECT DISTINCT NPI
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE
    WHERE DomainName = 'sPayer'
)

UNION ALL

SELECT 
    A.NPI,
    A.SpecialityName,
    'Speciality Not Matching' AS COMMENT
FROM HSLABCORNERSTONE.Directory_NPI_Universe A
WHERE A.NPI IN (
    SELECT DISTINCT NPI
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE
    WHERE DomainName = 'sPayer'
)
AND (A.NPI, LOWER(TRIM(A.SpecialityName))) NOT IN (
    SELECT B.NPI, LOWER(TRIM(B.SpecialityName))
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE B
    WHERE DomainName = 'sPayer'
)

UNION ALL

SELECT 
    A.NPI,
    A.SpecialityName,
    'Matched' AS COMMENT
FROM HSLABCORNERSTONE.Directory_NPI_Universe A
WHERE (A.NPI, LOWER(TRIM(A.SpecialityName))) IN (
    SELECT B.NPI, LOWER(TRIM(B.SpecialityName))
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE B
    WHERE DomainName = 'sPayer'
);
