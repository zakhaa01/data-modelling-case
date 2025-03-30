with
    final as (
        select
            g.genre_id,
            g.genre_name,
            count(m.movie_id) as movie_count,
            round(avg(m.popularity)::numeric, 2) as avg_genre_popularity
        from {{ ref('stg__daily_genres') }} g
        left join {{ ref('stg__daily_movies') }} m
        on g.movie_id=m.movie_id
        group by g.genre_id, g.genre_name
    )

select * from final
