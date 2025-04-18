select * from HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu1 where sdnu1.DomainName = 'sPayer'
union
SELECT distinct sdnu2.NPI,
concat(cast(sdnu2.NPI as VARCHAR(100)), '||A' ) as SpecialityName
FROM HSLABCORNERSTONE.SDIR_NPI_UNIVERSE sdnu2
where sdnu2.domainname = 'sPayer'
