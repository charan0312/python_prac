WITH ProviderDetails AS (
    SELECT 
        pa_1.ProviderID, 
        pa_1.HealthSystemID,
        pa_1.DisplayFirstName AS HsFirstName,
        pa_1.DisplayMiddleName AS HsMiddleName,
        pa_1.DisplayLastName AS HsLastName,
        pa_1.ProfessionalTitle,
        pa_1.Gender
    FROM HSLABCORNERSTONE.PROV_SDIR_ProviderAttribute pa_1
    INNER JOIN HSLABCORNERSTONE.PROV_SDIR_ProviderLocation ploc_1 
        ON pa_1.ProviderID = ploc_1.ProviderID
    INNER JOIN HSLABCORNERSTONE.PROV_SDIR_Location loc_1 
        ON ploc_1.LocationID = loc_1.LocationID
    WHERE loc_1.locationtypeid = 721
),
ProviderLanguages AS (
    SELECT 
        pl.ProviderID,
        MAX(CASE WHEN rn = 1 THEN l.LanguageName END) AS Language1,
        MAX(CASE WHEN rn = 2 THEN l.LanguageName END) AS Language2,
        MAX(CASE WHEN rn = 3 THEN l.LanguageName END) AS Language3
    FROM (
        SELECT 
            pl.ProviderID,
            l.LanguageName,
            ROW_NUMBER() OVER (PARTITION BY pl.ProviderID ORDER BY l.LanguageName) AS rn
        FROM HSLABCORNERSTONE.PROV_SDIR_ProviderLanguage pl
        LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Language l 
            ON pl.LanguageID = l.LanguageID
    ) p
    GROUP BY p.ProviderID
),
OSSProvider AS (
    SELECT 
        pd.ProviderID,
        pd.HealthSystemID,
        pd.HsFirstName,
        pd.HsMiddleName,
        pd.HsLastName,
        pd.ProfessionalTitle,
        pd.Gender,
        pl.Language1,
        pl.Language2,
        pl.Language3
    FROM ProviderDetails pd
    LEFT JOIN ProviderLanguages pl ON pd.ProviderID = pl.ProviderID
)
INSERT INTO HSLABCORNERSTONE.DMOM_SDIRECTORY_DENTAL_PROVIDER_DETAILS_FALLOUT
SELECT ob_pd.*, 'Record Not Matching OSS'
FROM DMOM_OB_DENTAL_PROVIDER_DETAILS ob_pd
LEFT JOIN OSSProvider oss_pd
ON ob_pd."Provider ID" = oss_pd.ProviderID
WHERE 
    COALESCE(CAST(ob_pd."First Name" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.HsFirstName AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Middle Name" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.HsMiddleName AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Last Name" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.HsLastName AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Professional Title" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.ProfessionalTitle AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Gender" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.Gender AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Language 1" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.Language1 AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Language 2" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.Language2 AS VARCHAR(255)), '') 
    OR COALESCE(CAST(ob_pd."Language 3" AS VARCHAR(255)), '') <> COALESCE(CAST(oss_pd.Language3 AS VARCHAR(255)), '');
