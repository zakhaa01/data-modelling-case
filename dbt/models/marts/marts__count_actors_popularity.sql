with
    final as (
        select
            c.actor_id,
            c.actor_name,
            count(c.movie_id) as movie_count,
            round(avg(m.rating_avg)::numeric, 2) as avg_rating
        from {{ ref('stg__daily_credits') }} c
        left join {{ ref('stg__daily_movies') }} m
        on c.movie_id=m.movie_id
        group by c.actor_id, c.actor_name
    )

select * from final
