with property_sales as (

    select *
    from {{ ref('stg_property_sales') }}

),

cleaned as (

    select
        property_id,
        sale_counter,
        downloaded_at,

        property_name,
        property_unit_number,
        property_house_number,
        property_street_name,
        suburb,
        postcode,

        area,
        area_type,

        contract_date,
        settlement_date,
        purchase_price,

        zoning,
        nature_of_property,
        primary_purpose,
        property_purpose_group,

        strata_lot_number,
        dealing_number,
        property_legal_description,

        case
            when suburb is not null
             and purchase_price is not null
             and purchase_price > 0
             and contract_date is not null
            then true
            else false
        end as is_analytics_usable

    from property_sales

)

select *
from cleaned