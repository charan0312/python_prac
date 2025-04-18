SELECT * 
FROM (
    SELECT 
        CAST(npiu2.NPI AS VARCHAR(100)) AS NPI,
        CAST('' AS VARCHAR(100)) AS qnxt_specialty,
        CONCAT(CAST(npiu2.NPI AS VARCHAR(100)), '||A') AS npiu2_concat
    FROM HSLABCORNERSTONE.Directory_NPI_Universe npiu2

    UNION ALL

    SELECT 
        CAST(npiu1.NPI AS VARCHAR(100)) AS NPI,
        CAST(npiu1.qnxt_specialty AS VARCHAR(100)) AS qnxt_specialty,
        CAST('' AS VARCHAR(100)) AS npiu2_concat
    FROM HSLABCORNERSTONE.Directory_NPI_Universe npiu1
) a
ORDER BY 1;
