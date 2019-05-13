from data import db
from data.queries import Queries
import folium


def map_requests(location_data):
    from pathlib import Path

    f_map = folium.Map(location=[float(location_data[0]['latitude']), float(location_data[0]['longitude'])])
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
    print("Map saved to " + str(Path().absolute()) + "/map.html")


def chart_requests_by_occurrence(data):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.DataFrame(data,
                          columns=['requests', 'service_name']).nlargest(5, 'requests')

    plt.pie(df['requests'], autopct='%.0f%%', pctdistance=0.85, labels=df['service_name'], startangle=90)

    plt.axis('equal')
    # plt.title('Requests by Type')
    plt.tight_layout()
    plt.show()


def chart_department_performance(data):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.DataFrame(data,
                          columns=['agency_responsible', 'requests', 'opened', 'closed', 'avg_request_age', 'total_time_spent', 'avg_time_per_request', 'avg_resolution_time'])

    plt.plot(df['date'], df['opened'], color='orange', label='Opened')
    plt.fill_between(df['date'], df['opened'], color='orange')
    plt.plot(df['date'], df['closed'], color='green', label='Closed')
    plt.fill_between(df['date'], df['closed'], color='green')


def chart_request_trends(data):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    import pandas

    df = pandas.DataFrame(data,
                          columns=['total', 'opened', 'closed', 'date'])
    # df['date'] = pandas.to_datetime(df.date).dt.strftime('%d/%m/%Y')

    plt.plot(df['date'], df['opened'], color='orange', label='Opened')
    plt.plot(df['date'], df['closed'], color='green', label='Closed')

    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.xlabel('Date')
    plt.xticks(rotation=45)
    plt.ylabel('Requests')
    plt.title('Service Requests by Day')
    plt.legend(loc='center right')
    plt.show()


def chart_requests_by_agency(data):
    import matplotlib.pyplot as plt
    import pandas

    df = pandas.DataFrame(data,
                          columns=['agency_responsible', 'requests', 'open', 'closed', 'avg_request_age',
                                   'total_time_spent', 'avg_time_per_request', 'avg_resolution_time'])\
        .sort_values('requests')

    plt1 = plt.bar(df['agency_responsible'], df['closed'], color='green')
    plt2 = plt.bar(df['agency_responsible'], df['open'], color='orange', bottom=df['closed'])

    plt.xlabel('Department')
    plt.xticks(rotation=45, horizontalalignment='right')
    plt.ylabel('Requests')
    plt.title('Service Request Count By Department')
    plt.legend((plt1[0], plt2[0]), ('Closed', 'Open'))
    plt.show()


def main():

    queries = Queries(db)

    # Uncomment any one of the following functions and enter the city of your choice.

    # Create a pie chart of requests according to frequency.
    chart_requests_by_occurrence(queries.request_types('peoria'))

    # Generate a map of requests (saved in the project's root directory).
    # map_requests(queries.location())

    # Generate a line chart of requests over time. Enter the starting date after the city.
    # chart_request_trends(queries.trends('peoria', '5/10/2019'))

    # Generate a bar chart of requests categorized by agency/department.
    # chart_requests_by_agency(queries.department_performance('bloomington'))


main()
