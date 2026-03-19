with source as (
    select * from {{ source('public', 'pit_stops') }}
),

cleaned as (
    select
        session_key,
        driver_number,
        lap_number,
        pit_duration,
        year,
        case
            when pit_duration < 20 then 'FAST'
            when pit_duration < 30 then 'NORMAL'
            else 'SLOW'
        end as pit_category
    from source
    where pit_duration is not null
      and pit_duration > 0
      and pit_duration < 120  -- remove outliers (red flag stops, etc)
)

select * from cleaned