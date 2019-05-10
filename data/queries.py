class Queries:

    def __init__(self, db):
        self.db = db

    def full(self):
        self.db.execute("SELECT raw_data ->> 'service_request_id' AS service_request_id,"
                        "raw_data ->> 'status_notes' AS status_notes,"
                        "raw_data ->> 'service_name' AS service_name,"
                        "raw_data ->> 'service_code' AS service_code,"
                        "raw_data ->> 'description' AS description,"
                        "raw_data ->> 'agency_responsible' AS agency_responsible,"
                        "raw_data ->> 'service_notice' AS service_notice,"
                        "raw_data ->> 'expected_datetime' AS expected_datetime,"
                        "raw_data ->> 'address' AS address,"
                        "raw_data ->> 'zipcode' AS zipcode,"
                        "raw_data ->> 'media_url' AS media_url,"
                        "*"
                        "FROM service_requests")
        return self.db.fetchall()

    def location(self):
        self.db.execute("SELECT slug,"
                        "raw_data ->> 'service_name' AS service_name,"
                        "raw_data ->> 'description' AS description,"
                        "status,"
                        "raw_data ->> 'media_url' AS media_url,"
                        "raw_data ->> 'address' AS address,"
                        "raw_data ->> 'zipcode' AS zipcode,"
                        "raw_data ->> 'lat' AS latitude,"
                        "raw_data ->> 'long' AS longitude,"
                        "geometry "
                        "FROM service_requests "
                        "JOIN cities ON service_requests.city_id = cities.id AND cities.slug = 'bloomington' "
                        "WHERE raw_data ->> 'address' is not null "
                        "LIMIT 100")
        return self.db.fetchall()

    def trends(self):
        self.db.execute("SELECT COUNT(*) as total,"
                        "COUNT(1) FILTER (WHERE status <> 'closed') AS opened,"
                        "COUNT(1) FILTER (WHERE status = 'closed') AS closed,"
                        "ROUND(COUNT(1) FILTER (WHERE status = 'closed') / GREATEST(COUNT(1), 1) ::DECIMAL, 2) as closed_rate,"
                        "DATE_TRUNC('day', requested_datetime) AS aggregator "
                        "FROM service_requests "
                        "JOIN cities on service_requests.city_id = cities.id "
                        "AND cities.slug = 'brookline' "
                        "GROUP BY aggregator "
                        "ORDER BY aggregator")
        return self.db.fetchall()

    def trends_with_service_name(self):
        self.db.execute("SELECT COUNT(*) as total,"
                        "COUNT(1) FILTER (WHERE status <> 'closed') AS opened,"
                        "COUNT(1) FILTER (WHERE status = 'closed') AS closed,"
                        "ROUND(COUNT(1) FILTER (WHERE status = 'closed') / GREATEST(COUNT(1), 1) ::DECIMAL, 2) as closed_rate,"
                        "DATE_TRUNC('day', requested_datetime) AS aggregator, "
                        "raw_data ->> 'service_name' AS service_name "
                        "FROM service_requests "
                        "JOIN cities on service_requests.city_id = cities.id "
                        "AND cities.slug = 'brookline' "
                        "GROUP BY service_name, aggregator "
                        "ORDER BY aggregator")
        return self.db.fetchall()

    def trends_with_department_name(self):
        self.db.execute("SELECT COUNT(*) as total,"
                        "COUNT(1) FILTER (WHERE status <> 'closed') AS opened,"
                        "COUNT(1) FILTER (WHERE status = 'closed') AS closed,"
                        "ROUND(COUNT(1) FILTER (WHERE status = 'closed') / GREATEST(COUNT(1), 1) ::DECIMAL, 2) as closed_rate,"
                        "DATE_TRUNC('day', requested_datetime) AS aggregator, "
                        "raw_data ->> 'agency_responsible' AS agency_responsible "
                        "FROM service_requests "
                        "JOIN cities on service_requests.city_id = cities.id "
                        "AND cities.slug = 'bloomington' "
                        "GROUP BY agency_responsible, aggregator "
                        "ORDER BY aggregator")
        return self.db.fetchall()