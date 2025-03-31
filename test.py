SELECT
    lh.LocationID,
    lh.DayOfWeekID,
    lh.StartTime,
    lh.EndTime,
    CASE
        WHEN MAX(CASE WHEN sdlos.LocationID IS NULL THEN 1 ELSE 0 END) = 1 THEN 'Missing in SDIR'
        ELSE 'Time mismatch in SDIR'
    END AS Comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONHOURS lh
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
    ON TRIM(lh.LocationID) = TRIM(sdl.ExternalCode)
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sdlos
    ON sdl.LocationID = sdlos.LocationID
   AND lh.DayOfWeekID = sdlos.WeekdayTypeID
GROUP BY
    lh.LocationID,
    lh.DayOfWeekID,
    lh.StartTime,
    lh.EndTime
HAVING
    MAX(CASE 
        WHEN sdlos.LocationID IS NOT NULL
         AND sdlos.OpeningTime = CAST(lh.StartTime AS TIME)
         AND sdlos.ClosingTime = CAST(lh.EndTime AS TIME)
        THEN 1 ELSE 0
    END) = 0  -- means no perfect match
ORDER BY lh.LocationID, lh.DayOfWeekID;
