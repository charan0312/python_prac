SELECT 
    -- Practitioner Basic Information
    p.practitionerid,
    p.practitionertypeid,
    pt.practitionertypename,
    p.firstname,
    p.middlename,
    p.lastname,
    p.suffixid,
    p.birthdate,
    p.nationalproviderid,
    p.statustypeid,
    st.statustypename,
    ss.statussetname,
    g.gendername,

    -- Practitioner Languages
    STRING_AGG(l.languagename, ', ') AS languages,

    -- Education
    STRING_AGG(
        pe.institution || ' (' || d.degreename || ')', ', '
    ) AS education_details,

    -- Specialties
    STRING_AGG(s.specialtyname, ', ') AS specialties,

    -- Certifications
    STRING_AGG(cb.boardname, ', ') AS certification_boards,

    -- Taxonomies
    STRING_AGG(t.taxonomycode, ', ') AS taxonomy_codes

FROM practitioners p
-- Join Practitioner Type
LEFT JOIN practitionertypes pt 
    ON p.practitionertypeid = pt.practitionertypeid

-- Join Gender
LEFT JOIN genders g 
    ON p.genderid = g.genderid

-- Join Status
LEFT JOIN statustypes st 
    ON p.statustypeid = st.statustypeid
LEFT JOIN statussets ss 
    ON st.statustypeid = ss.statussetid

-- Join Languages
LEFT JOIN practitionerlanguages pl 
    ON p.practitionerid = pl.practitionerid
LEFT JOIN languages l 
    ON pl.languageid = l.languageid

-- Join Education
LEFT JOIN practitionereducation pe 
    ON p.practitionerid = pe.practitionerid
LEFT JOIN degrees d 
    ON pe.degreeid = d.degreeid

-- Join Specialties
LEFT JOIN practitionorspecialties ps 
    ON p.practitionerid = ps.practitionerid
LEFT JOIN specialties s 
    ON ps.specialtyid = s.specialtyid

-- Join Certifications
LEFT JOIN certificationboards cb 
    ON s.certificationboardid = cb.certificationboardid

-- Join Taxonomies
LEFT JOIN taxonomies t 
    ON s.specialtyid = t.specialtyid

GROUP BY 
    p.practitionerid, 
    p.practitionertypeid, 
    pt.practitionertypename,
    p.firstname, 
    p.middlename, 
    p.lastname, 
    p.suffixid, 
    p.birthdate, 
    p.nationalproviderid, 
    p.statustypeid,
    st.statustypename,
    ss.statussetname,
    g.gendername;
