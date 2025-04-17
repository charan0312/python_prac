REPLACE PROCEDURE HSLABCORNERSTONE.SP_FALLOUT_NPI_SPECIALITY()
BEGIN

-- Step 0: Create a volatile table to collect fallout
CREATE VOLATILE TABLE fallout_table (
    NPI VARCHAR(20),
    SpecialityName VARCHAR(100),
    Comment VARCHAR(100)
) ON COMMIT PRESERVE ROWS;

-- Step 1: Add NPI Missing records
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

-- Step 2: Add Speciality Missing records
-- (NPI exists, but **none** of the specialties match, so include ALL specialties for that NPI from Table A)
INSERT INTO fallout_table (NPI, SpecialityName, Comment)
SELECT A.NPI, A.SpecialityName, 'Speciality Missing'
FROM HSLABCORNERSTONE.Directory_NPI_Universe A
WHERE A.NPI IN (
    -- NPIs that exist in B under sPayer domain
    SELECT DISTINCT NPI
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE
    WHERE DomainName = 'sPayer'
)
AND A.NPI NOT IN (
    -- But NONE of the specialties match for this NPI
    SELECT DISTINCT A2.NPI
    FROM HSLABCORNERSTONE.Directory_NPI_Universe A2
    INNER JOIN HSLABCORNERSTONE.SDIR_NPI_UNIVERSE B2
        ON A2.NPI = B2.NPI
       AND A2.SpecialityName = B2.SpecialityName
    WHERE B2.DomainName = 'sPayer'
);

-- Step 3: Return fallout results (optional if using it interactively)
SELECT * FROM fallout_table;

END;
