below is my query I'm getting nulls in specialty columns foix it for teradata

select * from
(SELECT npiu2.NPI,'' as qnxt_specialty,
concat(cast(npiu2.NPI as VARCHAR(100)), '||A' ) as npiu2_concat
FROM HSLABCORNERSTONE.Directory_NPI_Universe npiu2
union all
select npiu1.NPI, npiu1.qnxt_specialty , '' as npiu1_concat from HSLABCORNERSTONE.Directory_NPI_Universe npiu1) a
order by 1
