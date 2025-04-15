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
DELETE FROM HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_PRACTICELOCATIONS_FALLOUT;

-- INSERT RECORDS FROM Source TABLE for PRACTICELOCATIONS
--select top 5 isopen24hours from HSLABCORNERSTONE.PROV_SDIR_Locationschedul
INSERT INTO HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_PRACTICELOCATIONS_FALLOUT
SELECT DISTINCT pl.*,
       CASE
          WHEN sdl.ExternalCode IS NULL
          THEN
             'Record Missing in OSS'
          WHEN COALESCE (a.LineNumber1, '') <>
              COALESCE (sdla.Address1, '')
          THEN
             'Address Not matching in OSS'  
         WHEN COALESCE(
               CASE 
                  WHEN TRIM(UPPER(pl.TwentyFourHourCoverage)) = 'Y' THEN '1'
                  WHEN TRIM(UPPER(pl.TwentyFourHourCoverage)) = 'N' THEN '0'
                  ELSE ''
               END, ''
               ) 
               <> COALESCE(CAST(sdls.isopen24hours AS VARCHAR(1)), '') THEN '24-Hour Coverage Not matching in OSS'   
       END AS comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_practicelocations pl
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_Addresses a
ON pl.AddressID = a.AddressID
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
ON pl.LocationID = sdl.ExternalCode
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationAddress sdla
ON sdl.LocationID = sdla.LocationID
left join HSLABCORNERSTONE.PROV_SDIR_LocationSchedule sdls
on sdl.LocationID = sdls.LocationID
WHERE
((sdl.ExternalCode IS NULL)
           OR (COALESCE (a.LineNumber1, '') <>
              COALESCE (sdla.Address1, ''))
              OR (
               COALESCE(
               CASE 
                  WHEN TRIM(UPPER(pl.TwentyFourHourCoverage)) = 'Y' THEN '1'
                  WHEN TRIM(UPPER(pl.TwentyFourHourCoverage)) = 'N' THEN '0'
                  ELSE ''
               END, ''
               )
              )) AND pl.locationtypeid = 52819;




-- DELETE EXISITNG DATA FROM TABLE
DELETE FROM HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONPHONES_FALLOUT;

-- INSERT RECORDS FROM Source TABLE for LOCATIONPHONES
INSERT INTO HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONPHONES_FALLOUT
--Mgmt_Network_, PROV_SDIR_NetworkMgmt_Network
--PROV_SDIR_HealthPlan_HealthPlan
--PROV_SDIR_LocationContactPoint
-- Use Primary as phone type
SELECT DISTINCT lp.*,
       CASE
          WHEN sdlcp.LocationID IS NULL
          THEN
             'Record Missing in OSS'
          WHEN 
            COALESCE (p.PhoneNumber, '') <>
            COALESCE (sdlcp.ContactPointValue, '')
          THEN
             'Phone Number Not matching in OSS'
       END AS comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_practicelocations pl
LEFT JOIN PROVIDERDATASERVICE_CORE_V.prov_spayer_LOCATIONPHONES lp
ON pl.locationid = lp.locationid
LEFT JOIN PROVIDERDATASERVICE_CORE_V.prov_spayer_phones p
ON lp.PhoneID = p.PhoneID
LEFT JOIN PROVIDERDATASERVICE_CORE_V.prov_spayer_phonetypes pt
ON lp.PhoneTypeID = pt.PhoneTypeID
LEFT JOIN  HSLABCORNERSTONE.PROV_SDIR_Location sdl
ON lp.locationid = sdl.externalcode
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationContactPoint sdlcp
ON sdl.LocationID = sdlcp.LocationID
WHERE ((sdlcp.LocationID IS NULL)
   OR (COALESCE (p.PhoneNumber, '') <>
      COALESCE (sdlcp.ContactPointValue, ''))) AND pl.locationtypeid = 52819 
      and sdlcp.LocationContactPointSystemTypeID = 1 and pt.phonetypename = 'Primary';


-- DELETE EXISITNG DATA FROM TABLE
DELETE FROM HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONEMAILS_FALLOUT;

-- INSERT RECORDS FROM Source TABLE for PRACTICELOCATIONS
-- Use location contact with filter as 3
INSERT INTO HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONEMAILS_FALLOUT
SELECT DISTINCT lem.*,
       CASE
          WHEN sdlcp.LocationID IS NULL
          THEN
             'Record Missing in OSS'
          WHEN COALESCE (e.EmailAddress, '') <>
              COALESCE (sdlcp.ContactPointValue, '')
          THEN
             'Email Not matching in OSS'
       END AS comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_practicelocations pl
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_locationemails lem
ON pl.locationid = lem.locationid
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_emails e
ON lem.EmailID = e.EmailID
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_EMAILTYPES ety
ON lem.EmailTypeID = ety.EmailTypeID
LEFT JOIN  HSLABCORNERSTONE.PROV_SDIR_Location sdl
ON lem.locationid = sdl.externalcode
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationContactPoint sdlcp
ON sdl.LocationID = sdlcp.LocationID
WHERE ((sdlcp.LocationID IS NULL)
           OR (COALESCE (e.EmailAddress, '') <>
              COALESCE (sdlcp.ContactPointValue, ''))) AND pl.locationtypeid = 52819 
              and sdlcp.LocationContactPointSystemTypeID = 3;


-- DELETE EXISITNG DATA FROM TABLE
DELETE FROM HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONHOURS_FALLOUT;
-- INSERT RECORDS FROM Source TABLE for LOCATIONHOURS
INSERT INTO HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONHOURS_FALLOUT
SELECT DISTINCT lh.*,
       CASE
          WHEN sdlos.LocationID IS NULL
          THEN
             'Record Missing in OSS'
         WHEN CAST(lh.StartTime AS TIME) <> sdlos.OpeningTime
          OR CAST(lh.EndTime AS TIME) <> sdlos.ClosingTime THEN 'Hours Not matching in OSS'
       END AS comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_practicelocations pl
LEFT JOIN PROVIDERDATASERVICE_CORE_V.prov_spayer_LOCATIONHOURS lh
ON pl.locationid = lh.locationid
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
ON lh.LocationID = sdl.ExternalCode
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sdlos
ON sdl.locationid = sdlos.LocationID and lh.DayOfWeekID = sdlos.WeekdayTypeID
WHERE ((sdlos.LocationID IS NULL)
OR (CAST(lh.StartTime AS TIME) <> sdlos.OpeningTime)
OR (CAST(lh.EndTime AS TIME) <> sdlos.ClosingTime)) AND pl.locationtypeid = 52819;


-- DELETE EXISITNG DATA FROM TABLE
DELETE FROM HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONSERVICES_FALLOUT;

-- INSERT RECORDS FROM Source TABLE for LOCATIONSERVICES
--servicecategorytypename PROV_SPAYER_SERVICEcategoryTYPES
--locationcategoryname locationcategory
INSERT INTO HSLABCORNERSTONE.DMOM_SPAYER_SDIRECTORY_LOCATIONSERVICES_FALLOUT
SELECT DISTINCT ls.*,
       CASE
          WHEN sdl.ExternalCode IS NULL
          THEN
             'Record Missing in OSS'
          WHEN
          COALESCE (sct.servicecategorytypename, '') <>
              COALESCE (sdlc.locationcategoryname, '')
          THEN
             'Service Type Not matching in OSS'
       END AS comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_practicelocations pl
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONSERVICES ls
ON pl.locationid = ls.locationid
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_SERVICEcategoryTYPES sct
ON ls.ServiceCategoryTypeID = sct.ServiceCategoryTypeID
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
ON ls.LocationID = sdl.ExternalCode
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_locationcategory sdlc
on sdl.LocationCategoryID = sdlc.LocationCategoryID
WHERE 
((sdl.ExternalCode IS NULL)
OR (COALESCE (sct.servicecategorytypename, '') <>
              COALESCE (sdlc.locationcategoryname, ''))) AND pl.locationtypeid = 52819;


INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES ('SPAYER_PRACTICES_RECON',CURRENT_TIMESTAMP,2,'SPAYER_PRACTICES_RECON Completed');

END;
