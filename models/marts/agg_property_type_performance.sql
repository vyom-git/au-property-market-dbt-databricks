with property_sales as (

    select *
    from {{ ref('fct_property_sales') }}

),

property_type_performance as (

    select
        property_purpose_group,

        count(*) as sale_count,
        avg(purchase_price) as avg_purchase_price,
        min(purchase_price) as min_purchase_price,
        max(purchase_price) as max_purchase_price

    from property_sales

    group by
        property_purpose_group

)

select *
from property_type_performance