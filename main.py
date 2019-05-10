from data import db
from data.queries import Queries
import folium


# Optional: Check Pandas library https://pandas.pydata.org/


def generate_map(location_data):
    mahrow = location_data[0]
    f_map = folium.Map(location=[float(mahrow['latitude']), float(mahrow['longitude'])])
    for row in location_data:
        coordinates = [float(row['latitude'].strip(' "')), float(row['longitude'].strip(' "'))]

        # Add request type, details, and image (if applicable) to popup menu
        popup = "<b>" + row['service_name'] + "</b>"
        if row['description'] is not None:
            popup += "<p style='width:350px; white-space: no-wrap; overflow: hidden; text-overflow: ellipses'>" + row[
                'description'] + "</p>"
        if row['media_url'] is not None:
            popup += "<img src='" + row['media_url'] + "' width='350' />"

        # Add icon (green if request is complete, orange if incomplete)
        if row['status'] == 'closed':
            icon = folium.Icon(color='green', icon='check-square')
        else:
            icon = folium.Icon(color='orange', icon='exclamation-triangle')

        # Add marker to map
        folium.Marker(location=coordinates,
                      popup=popup,
                      icon=icon).add_to(f_map)

    f_map.save("map.html")


def generate_line_graph(trend_data):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.DataFrame(trend_data,
                          columns=['total', 'opened', 'closed', 'closed_rate', 'aggregator'])

    plt.plot(df['aggregator'], df['opened'], color='orange', label='Opened', solid_joinstyle='round')
    plt.plot(df['aggregator'], df['closed'], color='green', label='Closed', solid_joinstyle='round')

    # df = pandas.DataFrame(trend_data, columns=['total', 'opened', 'closed', 'closed_rate', 'aggregator', 'service_name'])
    # for service_name, sub_df in dataframe.groupby(by='service_name'):
    # plt.plot(sub_df['aggregator'], sub_df['opened'], label=service_name)

    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Requests')
    plt.title('Service Requests - 5/4/2019 to 5/10/2019')
    plt.legend(loc='center right')
    plt.show()


def generate_line_chart_by_agency(trend_data):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.DataFrame(trend_data,
                          columns=['total', 'opened', 'closed', 'closed_rate', 'aggregator', 'agency_responsible'])
    for agency, sub_df in df.groupby(by='agency_responsible'):
        plt.plot(sub_df['aggregator'], sub_df['opened'], label=agency, solid_joinstyle='round')
        # plt.plot(df['aggregator'], df['opened'], color='orange', label='Opened', solid_joinstyle='round')
        # plt.plot(df['aggregator'], df['closed'], color='green', label='Closed', solid_joinstyle='round')

    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title('Service Request Response Over Time By Agency')
    plt.legend()
    plt.show()


def generate_bubble_chart(trend_data):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.DataFrame(trend_data,
                          columns=['total', 'opened', 'closed', 'closed_rate', 'aggregator', 'service_name'])
    for service_name, sub_df in df.groupby(by='service_name'):
        plt.scatter(sub_df['aggregator'], service_name, sub_df['opened'])
        plt.scatter(sub_df['aggregator'], service_name, sub_df['closed'])

    # plt.xlabel('Date')
    # plt.ylabel('Count')
    # plt.title('Service Request Response Over Time')
    plt.legend()
    plt.show()


def main():
    queries = Queries(db)
    # generate_map(queries.location())
    generate_line_graph(queries.trends())
    # generate_bubble_chart(queries.trends_with_service_name())
    # generate_line_chart_by_agency(queries.trends_with_department_name())


main()
