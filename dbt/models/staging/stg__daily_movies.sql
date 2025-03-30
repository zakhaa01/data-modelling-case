with
    final as (
        select
            movie_id,
            title,
            country_code,
            tagline,
            overview,
            release_date,
            popularity,
            rating_avg,
            vote_count,
            budget_usd,
            revenue_usd,
            extracted_at_utc

        from {{ source("raw", "movies") }}
        where extracted_at_utc::date = current_date
    )

select * from final
