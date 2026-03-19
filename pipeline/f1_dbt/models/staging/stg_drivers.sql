with source as (
    select * from {{ source('public', 'drivers') }}
),

cleaned as (
    select distinct on (driver_number, year)
        driver_number,
        full_name,
        name_acronym,
        team_name,
        country_code,
        year
    from source
    order by driver_number, year, created_at desc
)

select * from cleaned