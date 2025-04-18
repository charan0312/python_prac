

select * from (
SELECT sdnu.NPI, sdnu.SpecialityName,
concat(cast(sdnu.NPI as VARCHAR(100)), '||' ,LOWER(TRIM(sdnu.SpecialityName))) as sdnu_concat
FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu
where sdnu.domainname = 'sPayer'
union
SELECT sdnu.NPI, sdnu.SpecialityName,
concat(cast(sdnu.NPI as VARCHAR(100)), '||A' ) as sdnu_concat
FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu
where sdnu.domainname = 'sPayer') a
order by 1
