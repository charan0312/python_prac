-- Step 1: Subquery with perfect matches
SELECT DISTINCT
    lh.LocationID,
    lh.DayOfWeekID,
    lh.StartTime,
    lh.EndTime,
    CASE
        WHEN sdl.LocationID IS NULL THEN 'Missing in SDIR'
        WHEN CAST(lh.StartTime AS TIME) <> sdlos.OpeningTime
          OR CAST(lh.EndTime AS TIME) <> sdlos.ClosingTime THEN 'Time mismatch in SDIR'
    END AS Comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONHOURS lh
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
    ON TRIM(lh.LocationID) = TRIM(sdl.ExternalCode)
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sdlos
    ON sdl.LocationID = sdlos.LocationID
   AND lh.DayOfWeekID = sdlos.WeekdayTypeID
WHERE NOT EXISTS (
    SELECT 1
    FROM HSLABCORNERSTONE.PROV_SDIR_Location sdl2
    JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sdlos2
      ON sdl2.LocationID = sdlos2.LocationID
    WHERE TRIM(sdl2.ExternalCode) = TRIM(lh.LocationID)
      AND sdlos2.WeekdayTypeID = lh.DayOfWeekID
      AND CAST(lh.StartTime AS TIME) = sdlos2.OpeningTime
      AND CAST(lh.EndTime AS TIME) = sdlos2.ClosingTime
)
ORDER BY lh.LocationID, lh.DayOfWeekID;
