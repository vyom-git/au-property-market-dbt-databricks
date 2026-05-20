with source as (

    select *
    from {{ source('bronze', 'raw_property_sales') }}

),

cleaned as (

    select
        cast(property_id as bigint) as property_id,
        cast(sale_counter as bigint) as sale_counter,

        to_timestamp(download_date_time, 'yyyyMMdd HH:mm') as downloaded_at,

        nullif(trim(property_name), '') as property_name,
        nullif(trim(property_unit_number), '') as property_unit_number,
        nullif(trim(property_house_number), '') as property_house_number,
        nullif(trim(property_street_name), '') as property_street_name,

        {{ standardise_suburb('property_locality') }} as suburb,

        cast(property_post_code as int) as postcode,

        cast(area as double) as area,
        nullif(trim(area_type), '') as area_type,

        to_date(contract_date, 'yyyyMMdd') as contract_date,
        to_date(settlement_date, 'yyyyMMdd') as settlement_date,

        cast(purchase_price as double) as purchase_price,

        nullif(trim(zoning), '') as zoning,
        nullif(trim(nature_of_property), '') as nature_of_property,
        nullif(trim(primary_purpose), '') as primary_purpose,

        cast(strata_lot_number as bigint) as strata_lot_number,

        nullif(trim(dealing_number), '') as dealing_number,
        nullif(trim(property_legal_description), '') as property_legal_description,

        _rescued_data

    from source

),

final as (

    select
        *,
        case
            when purchase_price <= 0 then true
            else false
        end as is_invalid_purchase_price,

        case
            when lower(primary_purpose) like '%residence%' then 'Residential'
            when lower(primary_purpose) like '%commercial%' then 'Commercial'
            when lower(primary_purpose) like '%vacant%' then 'Vacant Land'
            else 'Other'
        end as property_purpose_group

    from cleaned

)

select *
from final