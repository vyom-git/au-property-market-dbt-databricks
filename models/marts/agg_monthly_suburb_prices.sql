with property_sales as (

    select *
    from {{ ref('fct_property_sales') }}

),

monthly_suburb_prices as (

    select
        suburb,
        postcode,

        date_trunc('month', contract_date) as contract_month,

        count(*) as sale_count,
        avg(purchase_price) as avg_purchase_price,
        min(purchase_price) as min_purchase_price,
        max(purchase_price) as max_purchase_price

    from property_sales

    group by
        suburb,
        postcode,
        date_trunc('month', contract_date)

)

select *
from monthly_suburb_prices