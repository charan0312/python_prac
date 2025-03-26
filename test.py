I'm seeing this warning while creating this stored procedure in teradata. 
[Teradata Database] [5526] SPL5000:W(L40), E(3813):The positional assignment list has too many values.

This is the error after execution: SQLSTATE : 42000 SQLCODE :   3813

Fix this Stored procedure:

REPLACE PROCEDURE  HSLABCORNERSTONE.SP_DMOM_sPayer_sDIRECTORY_PRACTICES_RECON()

SQL SECURITY INVOKER
MAIN: BEGIN
DECLARE EXIT HANDLER
   FOR SQLEXCEPTION
    BEGIN
      INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES('SPAYER_PRACTICES_RECON',CURRENT_TIMESTAMP,-1,'SQLSTATE : '||:SQLSTATE||' SQLCODE : '||:SQLCODE);
    END;


INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES ('SPAYER_PRACTICES_RECON',CURRENT_TIMESTAMP,1,'SPAYER_PRACTICES_RECON Begin');


-- DELETE EXISITNG DATA FROM TABLE
DELETE FROM HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_PRACTICES_FALLOUT;

-- INSERT RECORDS FROM Source TABLE for PRACTICELOCATIONS
INSERT INTO HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_PRACTICES_FALLOUT
select DISTINCT pl.*,
       CASE
          WHEN sdl.ExternalCode is NULL
          THEN
             'Record Missing in OSS'
          WHEN COALESCE (a.LineNumber1, '') <>
              COALESCE (sdla.Address1, '')
          THEN
             'Address Not matching in OSS'
       END AS comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_practicelocations pl
left join PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_Addresses a
on pl.AddressID = a.AddressID
inner join HSLABCORNERSTONE.PROV_SDIR_Location sdl
on pl.LocationID = sdl.ExternalCode
left join HSLABCORNERSTONE.PROV_SDIR_LocationAddress sdla
on sdl.LocationID = sdla.LocationID
--left join HSLABCORNERSTONE.PROV_SDIR_LocationSchedule sdls
--on sdl.LocationID = sdls.LocationID
WHERE 
sdl.ExternalCode is NULL;
           --OR COALESCE (a.LineNumber1, '') <>
            --  COALESCE (sdla.Address1, '');
              

INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES ('SPAYER_PRACTICES_RECON',CURRENT_TIMESTAMP,2,'SPAYER_PRACTICES_RECON Completed');

END;
    

