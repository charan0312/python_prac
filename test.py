INSERT INTO HSLABCORNERSTONE.DMOM_SDIRECTORY_DENTAL_PROVIDER_DETAILS_FALLOUT
SELECT 
    ob_pd.*,
    'Record Not Matching OSS'
FROM DMOM_OB_DENTAL_PROVIDER_DETAILS ob_pd
LEFT JOIN (
    -- Subquery: Provider Details + Language Pivots
    SELECT 
        pa_1.ProviderID, 
        pa_1.HealthSystemID,
        pa_1.DisplayFirstName AS HsFirstName,
        pa_1.DisplayMiddleName AS HsMiddleName,
        pa_1.DisplayLastName AS HsLastName,
        pa_1.ProfessionalTitle,
        pa_1.Gender,
        p_l.Language1,
        p_l.Language2,
        p_l.Language3
    FROM HSLABCORNERSTONE.PROV_SDIR_ProviderAttribute pa_1
    INNER JOIN HSLABCORNERSTONE.PROV_SDIR_ProviderLocation ploc_1 
        ON pa_1.ProviderID = ploc_1.ProviderID
    INNER JOIN HSLABCORNERSTONE.PROV_SDIR_Location loc_1 
        ON ploc_1.LocationID = loc_1.LocationID
       AND loc_1.locationtypeid = 721
    LEFT JOIN (
        -- Subquery: Pivot Languages
        SELECT 
            p.ProviderID,
            MAX(CASE WHEN rn = 1 THEN p.LanguageName END) AS Language1,
            MAX(CASE WHEN rn = 2 THEN p.LanguageName END) AS Language2,
            MAX(CASE WHEN rn = 3 THEN p.LanguageName END) AS Language3
        FROM (
            -- Sub-subquery: Row numbering each language
            SELECT 
                pl_inner.ProviderID,
                l.LanguageName,
                ROW_NUMBER() OVER (PARTITION BY pl_inner.ProviderID 
                                   ORDER BY l.LanguageName) AS rn
            FROM HSLABCORNERSTONE.PROV_SDIR_ProviderLanguage pl_inner
            LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Language l 
                ON pl_inner.LanguageID = l.LanguageID
        ) p
        GROUP BY p.ProviderID
    ) p_l 
        ON pa_1.ProviderID = p_l.ProviderID
) oss_pd 
    ON ob_pd."Provider ID" = oss_pd.ProviderID
WHERE 
    COALESCE(ob_pd."First Name", '') <> COALESCE(oss_pd.HsFirstName, '') 
 OR COALESCE(ob_pd."Middle Name", '') <> COALESCE(oss_pd.HsMiddleName, '') 
 OR COALESCE(ob_pd."Last Name", '') <> COALESCE(oss_pd.HsLastName, '') 
 OR COALESCE(ob_pd."Professional Title", '') <> COALESCE(oss_pd.ProfessionalTitle, '') 
 OR COALESCE(ob_pd."Gender", '') <> COALESCE(oss_pd.Gender, '') 
 OR COALESCE(ob_pd."Language 1", '') <> COALESCE(oss_pd.Language1, '') 
 OR COALESCE(ob_pd."Language 2", '') <> COALESCE(oss_pd.Language2, '') 
 OR COALESCE(ob_pd."Language 3", '') <> COALESCE(oss_pd.Language3, '');
