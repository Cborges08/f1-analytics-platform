with flags as (
    select * from {{ ref('stg_race_control') }}
),

summary as (
    select
        session_key,
        year,
        count(*) filter (where flag = 'YELLOW')                 as yellow_flags,
        count(*) filter (where flag = 'DOUBLE_YELLOW')          as double_yellow_flags,
        count(*) filter (where flag = 'RED')                    as red_flags,
        count(*) filter (where flag = 'SAFETY_CAR')             as safety_car_events,
        count(*) filter (where flag = 'VIRTUAL_SAFETY_CAR')     as vsc_events,
        count(*)                                                as total_incidents
    from flags
    group by session_key, year
)

select * from summary
