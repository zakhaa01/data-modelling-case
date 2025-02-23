with
    final as (
        select
            movie_id,
            title,
            country_code,
            tagline,
            overview,
            release_date,
            rating_avg,
            budget_usd,
            revenue_usd,
            extracted_at_utc::date as extracted_date_utc,
            extracted_at_utc

        from {{ source("raw", "movies") }}
        limit 10
    )

select * from final
