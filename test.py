SELECT DISTINCT
    lh.LocationID,
    lh.DayOfWeekID,
    lh.StartTime,
    lh.EndTime,
    CASE
        WHEN sdlos.LocationID IS NULL THEN 'Missing in SDIR'
        WHEN CAST(lh.StartTime AS TIME) <> sdlos.OpeningTime 
          OR CAST(lh.EndTime AS TIME) <> sdlos.ClosingTime THEN 'Time mismatch in SDIR'
        ELSE NULL
    END AS Comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONHOURS lh
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
    ON TRIM(lh.LocationID) = TRIM(sdl.ExternalCode)
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sdlos
    ON sdl.LocationID = sdlos.LocationID
   AND lh.DayOfWeekID = sdlos.WeekdayTypeID
WHERE
    sdlos.LocationID IS NULL
    OR CAST(lh.StartTime AS TIME) <> sdlos.OpeningTime
    OR CAST(lh.EndTime AS TIME) <> sdlos.ClosingTime
ORDER BY lh.LocationID, lh.DayOfWeekID;
