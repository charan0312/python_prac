fix this

select a.npi, a.qnxt_specialty, a.npiu2_concat,
case when a.qnxt_specialty is null then a.npiu2_concat
else concat(cast(a.npi as VARCHAR(100)), '||' ,LOWER(TRIM(a.qnxt_specialty))) 
end as test

from
(
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
   order by 1
