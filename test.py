SELECT 
    A.NPI,
    A.SPECIALTY,
    CASE
        WHEN C.NPI IS NULL THEN 'NPI Missing'
        WHEN B.SPECIALTY IS NULL THEN 'Specialty Not Matching'
        ELSE 'Matched'
    END AS COMMENT
FROM TABLE1 A

-- Step 1: Join for exact NPI + Specialty match (case-insensitive)
LEFT JOIN (
    SELECT NPI, SPECIALTY
    FROM TABLE2
    WHERE DomainName = 'sPayer'
) B
  ON A.NPI = B.NPI
 AND LOWER(A.SPECIALTY) = LOWER(B.SPECIALTY)

-- Step 2: Join for NPI presence check only
LEFT JOIN (
    SELECT DISTINCT NPI
    FROM TABLE2
    WHERE DomainName = 'sPayer'
) C
  ON A.NPI = C.NPI;
