with pit_stops as (
    select * from {{ ref('stg_pit_stops') }}
),

summary as (
    select
        session_key,
        driver_number,
        year,
        count(*)                        as total_pit_stops,
        round(avg(pit_duration)::numeric, 3)   as avg_pit_duration,
        round(min(pit_duration)::numeric, 3)   as fastest_pit,
        round(sum(pit_duration)::numeric, 3)   as total_pit_time,
        min(lap_number)                 as first_pit_lap
    from pit_stops
    group by session_key, driver_number, year
)

select * from summary