fix this


select top 5 * from 
(
select a.npi, 
case when a.qnxt_specialty = '' then a.npiu2_concat
else concat(cast(a.npi as VARCHAR(100)), '||' ,LOWER(TRIM(a.qnxt_specialty))) 
end as qnxt_specialty
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
    ) a) tst1
   left join
   (
   select b.npi, 
case when b.SpecialityName = '' then b.sdnu1_concat
else concat(cast(b.npi as VARCHAR(100)), '||' ,LOWER(TRIM(b.SpecialityName))) 
end as SpecialityName
from(
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
        CAST('' AS VARCHAR(100)) AS sdnu_concat
    FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu2
    WHERE sdnu2.domainname = 'sPayer') b
   ) tst2
   on tst1.qnxt_specialty = tst2.SpecialityName
)) npiu
order by 1
