SELECT DISTINCT
    lh.LocationID,
    lh.DayOfWeekID,
    lh.StartTime,
    lh.EndTime,
    CASE
        WHEN sdl.LocationID IS NULL THEN 'Missing in SDIR'
        WHEN matched.MatchFlag = 0 THEN 'Time mismatch in SDIR'
    END AS Comments
FROM PROVIDERDATASERVICE_CORE_V.PROV_SPAYER_LOCATIONHOURS lh
LEFT JOIN HSLABCORNERSTONE.PROV_SDIR_Location sdl
    ON TRIM(lh.LocationID) = TRIM(sdl.ExternalCode)
LEFT JOIN (
    -- This sub-join flags perfect matches
    SELECT DISTINCT
        TRIM(sdir.ExternalCode) AS ExternalCode,
        sched.WeekdayTypeID,
        sched.OpeningTime,
        sched.ClosingTime,
        1 AS MatchFlag
    FROM HSLABCORNERSTONE.PROV_SDIR_Location sdir
    JOIN HSLABCORNERSTONE.PROV_SDIR_LocationOperatingSchedule sched
      ON sdir.LocationID = sched.LocationID
) matched
  ON TRIM(lh.LocationID) = matched.ExternalCode
 AND lh.DayOfWeekID = matched.WeekdayTypeID
 AND matched.OpeningTime = CAST(lh.StartTime AS TIME)
 AND matched.ClosingTime = CAST(lh.EndTime AS TIME)
WHERE
    sdl.LocationID IS NULL
    OR matched.MatchFlag IS NULL
ORDER BY lh.LocationID, lh.DayOfWeekID;
