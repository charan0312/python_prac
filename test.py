SELECT
    lh.LocationID,
    lh.DayOfWeekID,
    lh.StartTime,
    lh.EndTime,
    CASE
        WHEN MAX(CASE 
                    WHEN sdlos.LocationID IS NOT NULL 
                         AND CAST(lh.StartTime AS TIME) = sdlos.OpeningTime 
                         AND CAST(lh.EndTime AS TIME) = sdlos.ClosingTime 
                    THEN 1 ELSE 0 END) = 1 
            THEN NULL -- Perfect match exists, exclude in outer filter
        WHEN MAX(CASE WHEN sdlos.LocationID IS NULL THEN 1 ELSE 0 END) = 1
            THEN 'Missing in SDIR'
        ELSE 'Time mismatch in SDIR'
    END AS Comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONHOURS lh
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
    ON TRIM(lh.LocationID) = TRIM(sdl.ExternalCode)
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sdlos
    ON sdl.LocationID = sdlos.LocationID
   AND lh.DayOfWeekID = sdlos.WeekdayTypeID
GROUP BY lh.LocationID, lh.DayOfWeekID, lh.StartTime, lh.EndTime
HAVING
    MAX(CASE 
            WHEN sdlos.LocationID IS NOT NULL 
                 AND CAST(lh.StartTime AS TIME) = sdlos.OpeningTime 
                 AND CAST(lh.EndTime AS TIME) = sdlos.ClosingTime 
            THEN 1 ELSE 0 END) = 0  -- Only keep unmatched or mismatched
ORDER BY lh.LocationID, lh.DayOfWeekID;
