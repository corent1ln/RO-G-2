
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap

class Plot:
    _node_positions = {}
    @staticmethod
    def plot_graph(graph, path=None):

        if graph.id not in Plot._node_positions: # store graph node position to plot same graph foreach call (same nodes positions) 
            Plot._node_positions[graph.id] = nx.spring_layout(graph, seed=0)

        node_positions = Plot._node_positions[graph.id]

        for node, coord in node_positions.items():
            plt.scatter(coord[0], coord[1], color='red', s=100, label="Node" if node == list(graph.nodes)[0] else "")
            plt.text(coord[0], coord[1], f"{node}", fontsize=8, ha='center', va='center', color='white')

        if path:
            path_edges = list(zip(path, path[1:]))
        else:
            path_edges = []

        #plot blocked edges in yellow
        for u, v, data in graph.blocked_edges:
            x_coords = [node_positions[u][0], node_positions[v][0]]
            y_coords = [node_positions[u][1], node_positions[v][1]]
            plt.plot(x_coords, y_coords, '#FF6600', linewidth=0.5, linestyle='--')

        #plot costly edges in red, todo do it in the edges plot with a costly edges list check
        for u, v, data in graph.costly_edges:
            x_coords = [node_positions[u][0], node_positions[v][0]]
            y_coords = [node_positions[u][1], node_positions[v][1]]
            plt.plot(x_coords, y_coords, 'red', linewidth=2, alpha=0.7)

        #plot edges and path edges
        for u, v in graph.edges:
            x_coords = [node_positions[u][0], node_positions[v][0]]
            y_coords = [node_positions[u][1], node_positions[v][1]]
            
            if (u, v) in path_edges or (v, u) in path_edges:
                plt.plot(x_coords, y_coords, 'blue', linewidth=1)
            else:
                plt.plot(x_coords, y_coords, 'gray', linewidth=0.5)

        plt.title("Best path of graph" if path else "Graph")
        plt.axis('off') 
        plt.show()

    @staticmethod
    def plot_map(city_coordinates, graph = None, path=None, show_graph = False):
        
        #focus based on the nodes of graph
        latitudes = [coord[0] for coord in city_coordinates.values()]
        longitudes = [coord[1] for coord in city_coordinates.values()]
        
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)
        
        lat_margin = (max_lat - min_lat) * 0.1
        lon_margin = (max_lon - min_lon) * 0.1
        
        min_lat -= lat_margin
        max_lat += lat_margin
        min_lon -= lon_margin
        max_lon += lon_margin

        plt.figure(figsize=(10, 8))
        m = Basemap(projection='merc', llcrnrlat=min_lat, urcrnrlat=max_lat,llcrnrlon=min_lon, urcrnrlon=max_lon, resolution='i')
        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary(fill_color='lightblue')
        m.fillcontinents(color='lightgreen', lake_color='lightblue')

         # Plot nodes
        city_to_coords = {}
        for city, (lat, lon) in city_coordinates.items():
            x, y = m(lon, lat)
            city_to_coords[city] = (x, y)
            plt.plot(x, y, 'ro', markersize=5)
            plt.text(x, y, city, fontsize=8, ha='left', color='black')

        # Plot all edges if requested
        if graph and show_graph:
            for u, v in graph.edges():
                if u in city_to_coords and v in city_to_coords:
                    x_coords = [city_to_coords[u][0], city_to_coords[v][0]]
                    y_coords = [city_to_coords[u][1], city_to_coords[v][1]]
                    plt.plot(x_coords, y_coords, 'gray', linewidth=0.5)
                    
            # Plot costly edges
            for u, v,data in graph.costly_edges:
                if u in city_to_coords and v in city_to_coords:
                    x_coords = [city_to_coords[u][0], city_to_coords[v][0]]
                    y_coords = [city_to_coords[u][1], city_to_coords[v][1]]
                    plt.plot(x_coords, y_coords, 'red', linewidth=2, alpha=0.7)

            #Plot blocked edges
            for u, v,data in graph.blocked_edges:
                if u in city_to_coords and v in city_to_coords:
                    x_coords = [city_to_coords[u][0], city_to_coords[v][0]]
                    y_coords = [city_to_coords[u][1], city_to_coords[v][1]]
                    plt.plot(x_coords, y_coords, '#FF6600', linewidth=0.5, linestyle='--')


        # Plot path if provided
        if path:
            path_coords = [city_to_coords[city] for city in path if city in city_to_coords]
            path_x, path_y = zip(*path_coords)
            plt.plot(path_x, path_y, 'b-', linewidth=2, label='Chemin optimal')
            plt.plot(path_x[0], path_y[0], 'go', markersize=8, label='Départ/Arrivée')

        plt.legend()
        plt.title("Best path of map graph" if path else "Map Graph")
        plt.show()

    @staticmethod
    def plot_comparison_distance_over_iterations(algorithms_results):
        for algo_name, distances in algorithms_results.items():
            plt.plot(distances, label=algo_name, linewidth=2)

        plt.title("Comparison of Trip Length Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Distance")
        plt.legend()
        plt.show()
