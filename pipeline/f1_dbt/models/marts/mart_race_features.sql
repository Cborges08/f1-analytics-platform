with results as (
    select * from {{ ref('stg_race_results') }}
),

sessions as (
    select * from {{ ref('stg_sessions') }}
),

drivers as (
    select * from {{ ref('stg_drivers') }}
),

pits as (
    select * from {{ ref('int_race_pit_summary') }}
),

flags as (
    select * from {{ ref('int_race_flags_summary') }}
),

final as (
    select
        -- Identifiers
        r.session_key,
        r.driver_number,
        r.year,

        -- Session info
        s.race_date,
        s.circuit_short_name,
        s.country_name,

        -- Driver info
        d.full_name          as driver_name,
        d.name_acronym,
        d.team_name,

        -- Race result (target variable for ML)
        r.position           as finish_position,
        r.result_category,

        -- Pit stop features
        coalesce(p.total_pit_stops, 0)      as total_pit_stops,
        coalesce(p.avg_pit_duration, 0)     as avg_pit_duration,
        coalesce(p.fastest_pit, 0)          as fastest_pit,
        coalesce(p.total_pit_time, 0)       as total_pit_time,
        coalesce(p.first_pit_lap, 0)        as first_pit_lap,

        -- Race chaos features
        coalesce(f.yellow_flags, 0)         as yellow_flags,
        coalesce(f.double_yellow_flags, 0)  as double_yellow_flags,
        coalesce(f.red_flags, 0)            as red_flags,
        coalesce(f.safety_car_events, 0)    as safety_car_events,
        coalesce(f.vsc_events, 0)           as vsc_events,
        coalesce(f.total_incidents, 0)      as total_incidents

    from results r
    left join sessions s on s.session_key = r.session_key
    left join drivers d on d.driver_number = r.driver_number
                       and d.year = r.year
    left join pits p on p.session_key = r.session_key
                    and p.driver_number = r.driver_number
    left join flags f on f.session_key = r.session_key
)

select * from final
order by race_date, finish_position