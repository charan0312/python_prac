REPLACE PROCEDURE HSLABCORNERSTONE.SP_FALLOUT_NPI_SPECIALITY()
BEGIN

-- Step 0: Create fallout table
CREATE VOLATILE TABLE fallout_table (
    NPI VARCHAR(20),
    SpecialityName VARCHAR(100),
    Comment VARCHAR(100)
) ON COMMIT PRESERVE ROWS;

-- Step 1: NPI Missing (no matching NPI with DomainName = 'sPayer')
INSERT INTO fallout_table (NPI, SpecialityName, Comment)
SELECT A.NPI, A.SpecialityName, 'NPI Missing'
FROM HSLABCORNERSTONE.Directory_NPI_Universe A
LEFT JOIN (
    SELECT DISTINCT NPI
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE
    WHERE DomainName = 'sPayer'
) B
ON A.NPI = B.NPI
WHERE B.NPI IS NULL;

-- Step 2: Speciality Not Matching
-- For NPIs that exist in sPayer domain, but this specific speciality does not match
-- And only if the NPI has no exact NPI-speciality match (to follow the "at least 1 match then ignore" rule)
INSERT INTO fallout_table (NPI, SpecialityName, Comment)
SELECT A.NPI, A.SpecialityName, 'Speciality Not Matching'
FROM HSLABCORNERSTONE.Directory_NPI_Universe A
WHERE A.NPI IN (
    SELECT DISTINCT NPI
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE
    WHERE DomainName = 'sPayer'
)
AND NOT EXISTS (
    SELECT 1
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE B
    WHERE A.NPI = B.NPI
      AND A.SpecialityName = B.SpecialityName
      AND B.DomainName = 'sPayer'
)
AND A.NPI NOT IN (
    SELECT DISTINCT A2.NPI
    FROM HSLABCORNERSTONE.Directory_NPI_Universe A2
    INNER JOIN HSLABCORNERSTONE.SDIR_NPI_UNIVERSE B2
        ON A2.NPI = B2.NPI
       AND A2.SpecialityName = B2.SpecialityName
       AND B2.DomainName = 'sPayer'
);

-- Step 3: Return result
SELECT * FROM fallout_table;

END;
