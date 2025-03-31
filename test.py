SELECT DISTINCT ls.*,
       CASE
          WHEN sdl.ExternalCode IS NULL
          THEN
             'Record Missing in OSS'
          WHEN
          COALESCE (st.ServiceTypeName, '') =
              COALESCE (sdlft.featuretypename, '')
          THEN
             'Service Type Not matching in OSS'
       END AS comments

FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONSERVICES ls
LEFT JOIN PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_SERVICETYPES st
ON ls.ServiceTypeID = st.ServiceTypeID
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
ON ls.LocationID = sdl.ExternalCode
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationFeature sdlf
ON sdl.LocationID = sdlf.LocationID
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationFeatureItem sdlfi
ON sdlf.FeatureId = sdlfi.LocationFeatureItemId
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationFeatureType sdlft
ON sdlft.LocationFeatureTypeId = sdlft.LocationFeatureTypeId
WHERE 
sdl.ExternalCode IS NULL
OR COALESCE (st.ServiceTypeName, '') =
              COALESCE (sdlft.featuretypename, '');
