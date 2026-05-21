with suburb_prices as (

    select *
    from {{ ref('agg_monthly_suburb_prices') }}

),

suburb_summary as (

    select
        suburb,
        postcode,

        sum(sale_count) as total_sale_count,
        avg(avg_purchase_price) as avg_purchase_price,
        percentile_approx(median_purchase_price, 0.5) as median_purchase_price,
        min(min_purchase_price) as min_purchase_price,
        max(max_purchase_price) as max_purchase_price

    from suburb_prices

    group by
        suburb,
        postcode

),

ranked as (

    select
        *,

        dense_rank() over (
            order by median_purchase_price desc
        ) as median_price_rank,

        dense_rank() over (
            order by avg_purchase_price desc
        ) as avg_price_rank,

        dense_rank() over (
            order by total_sale_count desc
        ) as sales_volume_rank

    from suburb_summary

)

select *
from ranked
