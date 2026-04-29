WITH adwords AS (SELECT * FROM {{ ref('stg_adwords') }}),
facebook AS (SELECT * FROM {{ ref('stg_facebook') }}),

combined AS (
    SELECT * FROM adwords
    UNION ALL
    SELECT * FROM facebook
),

final AS (
    SELECT
        date_date,
        campaign_key,
        campaign_name,
        platform,
        SUM(ads_cost)         AS ads_cost,
        SUM(ads_impressions)  AS ads_impressions,
        SUM(ads_clicks)       AS ads_clicks,
        CASE WHEN SUM(ads_impressions) > 0
             THEN SUM(ads_clicks) * 1.0 / SUM(ads_impressions)
             ELSE 0
        END                   AS click_through_rate,
        CASE WHEN SUM(ads_clicks) > 0
             THEN SUM(ads_cost) / SUM(ads_clicks)
             ELSE 0
        END                   AS cost_per_click
    FROM combined
    GROUP BY date_date, campaign_key, campaign_name, platform
)
SELECT * FROM final
