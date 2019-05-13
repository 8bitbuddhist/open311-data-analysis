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

    def location(self, city):
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
                        "JOIN cities ON service_requests.city_id = cities.id "
                        "AND cities.slug = '" + city + "' "
                        "WHERE raw_data ->> 'address' is not null "
                        "LIMIT 100")
        return self.db.fetchall()

    def request_types(self, city):
        self.db.execute("SELECT "
                        "COUNT(raw_data ->> 'service_request_id') AS requests, "
                        "raw_data ->> 'service_name' AS service_name "
                        "FROM service_requests "
                        "JOIN cities ON service_requests.city_id = cities.id "
                        "AND cities.slug = '" + city + "' "
                        "GROUP BY service_name "
                        "ORDER BY requests DESC")
        return self.db.fetchall()

    def trends(self, city, from_date):
        self.db.execute("SELECT "
                        "COUNT(*) as total, "
                        "COUNT(1) FILTER (WHERE status <> 'closed') AS opened, "
                        "COUNT(1) FILTER (WHERE status = 'closed') AS closed, "
                        "DATE_TRUNC('day', requested_datetime) AS date "
                        "FROM service_requests "
                        "JOIN cities ON service_requests.city_id = cities.id "
                        "AND cities.slug = '" + city + "' "
                        "WHERE requested_datetime >= '" + from_date + "' "
                        "GROUP BY date "
                        "ORDER BY date ASC")
        return self.db.fetchall();

    def department_performance(self, city):
        self.db.execute("SELECT "
                        "raw_data ->> 'agency_responsible' AS agency_responsible, "
                        "COUNT(service_request_id) AS requests, "
                        "COUNT(1) FILTER (WHERE status <> 'closed') AS open, "
                        "COUNT(1) FILTER (WHERE status = 'closed') AS closed, "
                        "AVG(NOW() - requested_datetime) AS avg_request_age, "
                        "SUM(updated_datetime - requested_datetime) AS total_time_spent, "
                        "AVG(updated_datetime - requested_datetime) FILTER (WHERE updated_datetime <> requested_datetime) AS avg_time_per_request, "
                        "AVG(updated_datetime - requested_datetime) FILTER (WHERE status = 'closed') AS avg_resolution_time "
                        "FROM service_requests "
                        "JOIN cities on service_requests.city_id = cities.id "
                        "AND cities.slug = '" + city + "' "
                        "GROUP BY agency_responsible")
        return self.db.fetchall()