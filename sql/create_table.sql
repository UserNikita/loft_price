CREATE TABLE IF NOT EXISTS loft.price
(
    datetime DateTime CODEC(Delta, ZSTD),
    lat Float32 CODEC(Delta, ZSTD),
    lon Float32 CODEC(Delta, ZSTD),
    price UInt32,



    h3_resolution_7 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 7) CODEC(Delta, ZSTD),
    h3_resolution_8 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 8) CODEC(Delta, ZSTD),
    h3_resolution_9 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 9) CODEC(Delta, ZSTD),
    h3_resolution_10 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 10) CODEC(Delta, ZSTD),
    h3_resolution_11 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 11) CODEC(Delta, ZSTD),
    h3_resolution_12 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 12) CODEC(Delta, ZSTD),
    h3_resolution_13 MATERIALIZED geoToH3(toFloat64(lon),  toFloat64(lat), 13) CODEC(Delta, ZSTD)
)
ENGINE=MergeTree()
ORDER BY (datetime, price)