with clean_sales as (

    select *
    from {{ ref('int_clean_property_sales') }}

),

final as (

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
        property_legal_description

    from clean_sales
    where is_analytics_usable = true

)

select *
from final