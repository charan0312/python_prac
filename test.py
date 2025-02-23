

REPLACE PROCEDURE  HSLABCORNERSTONE.SP_DMOM_sDIRECTORY_OSS_DENTAL_PROVIDER_DETAILS_RECON()

SQL SECURITY INVOKER
MAIN: BEGIN
DECLARE EXIT HANDLER
   FOR SQLEXCEPTION
    BEGIN
      INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES('DENTAL_PROVIDER_DETAILS_RECON',CURRENT_TIMESTAMP,-1,'SQLSTATE : '||:SQLSTATE||' SQLCODE : '||:SQLCODE);
    END;


INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES ('DENTAL_PROVIDER_DETAILS_RECON',CURRENT_TIMESTAMP,1,'DENTAL_PROVIDER_DETAILS_RECON Begin');


-- DELETE EXISITNG DATA FROM TABLE
DELETE FROM HSLABCORNERSTONE.DMOM_SDIRECTORY_DENTAL_PROVIDER_DETAILS_FALLOUT;

-- INSERT RECORDS FROM Source TABLE
INSERT INTO HSLABCORNERSTONE.DMOM_SDIRECTORY_DENTAL_PROVIDER_DETAILS_FALLOUT
SELECT ob_pd.*,
       CASE
          WHEN oss_pd.ProviderID IS NULL
          THEN
             'Record Not Matching OSS'
          WHEN COALESCE (ob_pd."First Name", '') <>
               COALESCE (oss_pd.HsFirstName, '')
          THEN
             'First Name Not matching in OSS'
          WHEN COALESCE (ob_pd."Middle Name", '') <>
               COALESCE (oss_pd.HsMiddleName, '')
          THEN
             'Middle Name Not matching in OSS'
          WHEN COALESCE (ob_pd."Last Name", '') <>
               COALESCE (oss_pd.HsLastName, '')
          THEN
             'Last Name Not matching in OSS'
          WHEN COALESCE (ob_pd."Professional Title", '') <>
               COALESCE (oss_pd.ProfessionalTitle, '')
          THEN
             'Professional Title Not matching in OSS'
          WHEN COALESCE (ob_pd."Gender", '') <> COALESCE (oss_pd.Gender, '')
          THEN
             'Gender Not matching in OSS'
          WHEN COALESCE (ob_pd."Language 1", '') <>
               COALESCE (oss_pd.Language1, '')
          THEN
             'Language 1 Not matching in OSS'
          WHEN COALESCE (ob_pd."Language 2", '') <>
               COALESCE (oss_pd.Language2, '')
          THEN
             'Language 2 Not matching in OSS'
          WHEN COALESCE (ob_pd."Language 3", '') <>
               COALESCE (oss_pd.Language3, '')
          THEN
             'Language 3 Not matching in OSS'
       END AS comments
FROM DMOM_OB_DENTAL_PROVIDER_DETAILS ob_pd
     LEFT JOIN
     (SELECT pa_den.ProviderID,
             pa_den.HealthSystemID,
             pa_den.ProfessionalTitle,
             pa_den.Gender,
             pa_den.HsFirstName,
             pa_den.HsMiddleName,
             pa_den.HsLastName,
             p_l.Language1,
             p_l.Language2,
             p_l.Language3
      FROM (SELECT pa_1.ProviderID,
                   pa_1.HealthSystemID,
                   pa_1.DisplayFirstName,
                   pa_1.DisplayMiddleName,
                   pa_1.DisplayLastName,
                   pa_1.ProfessionalTitle,
                   pa_1.Gender,
                   pa_1.HsFirstName,
                   pa_1.HsMiddleName,
                   pa_1.HsLastName
            FROM HSLABCORNERSTONE.PROV_SDIR_ProviderAttribute pa_1
                 INNER JOIN
                 HSLABCORNERSTONE.PROV_SDIR_ProviderLocation ploc_1
                    ON pa_1.ProviderID = ploc_1.ProviderID
                 INNER JOIN HSLABCORNERSTONE.PROV_SDIR_Location loc_1
                    ON ploc_1.LocationID = loc_1.LocationID
            WHERE loc_1.locationtypeid = 721) pa_den
           INNER JOIN
           (SELECT p.ProviderID,
                   MAX (CASE WHEN rn = 1 THEN p.languagename END)
                      AS Language1,
                   MAX (CASE WHEN rn = 2 THEN p.languagename END)
                      AS Language2,
                   MAX (CASE WHEN rn = 3 THEN p.languagename END)
                      AS Language3
            FROM (SELECT pl.ProviderID,
                         l.LanguageName,
                         ROW_NUMBER ()
                         OVER (PARTITION BY pl.providerid
                               ORDER BY l.languagename) AS rn
                  FROM HSLABCORNERSTONE.PROV_SDIR_ProviderLanguage pl
                       LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Language l
                          ON pl.LanguageID = l.LanguageID) p
            GROUP BY p.providerid) p_l
              ON pa_den.ProviderID = p_l.ProviderID) oss_pd
        ON ob_pd."Provider ID" = oss_pd.ProviderID
WHERE    oss_pd.ProviderID IS NULL
      OR COALESCE (ob_pd."First Name", '') <>
         COALESCE (oss_pd.HsFirstName, '')
      OR COALESCE (ob_pd."Middle Name", '') <>
         COALESCE (oss_pd.HsMiddleName, '')
      OR COALESCE (ob_pd."Last Name", '') <> COALESCE (oss_pd.HsLastName, '')
      OR COALESCE (ob_pd."Professional Title", '') <>
         COALESCE (oss_pd.ProfessionalTitle, '')
      OR COALESCE (ob_pd."Gender", '') <> COALESCE (oss_pd.Gender, '')
      OR -- COALESCE(ob_pd."Primary Specialty", '') <> COALESCE(oss_pd.PrimarySpecialty, '') OR
         -- COALESCE(ob_pd."Specialty 2", '') <> COALESCE(oss_pd.Specialty2, '') OR
         -- COALESCE(ob_pd."Specialty 3", '') <> COALESCE(oss_pd.Specialty3, '') OR
         -- COALESCE(ob_pd."Specialty 4", '') <> COALESCE(oss_pd.Specialty4, '') OR
         -- COALESCE(ob_pd."Specialty 5", '') <> COALESCE(oss_pd.Specialty5, '') OR
         COALESCE (ob_pd."Language 1", '') <> COALESCE (oss_pd.Language1, '')
      OR COALESCE (ob_pd."Language 2", '') <> COALESCE (oss_pd.Language2, '')
      OR COALESCE (ob_pd."Language 3", '') <> COALESCE (oss_pd.Language3, '');


INSERT INTO HSLABCORNERSTONE.DMOM_SDIR_RECON_LOAD_LOGS VALUES ('DENTAL_PROVIDER_DETAILS_RECON',CURRENT_TIMESTAMP,2,'DENTAL_PROVIDER_DETAILS_RECON Completed');

END;
