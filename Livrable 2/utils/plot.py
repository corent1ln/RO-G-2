
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap

class Plot: #todo optimize all
    _node_positions = {}
    _used_colors = []
    _available_colors = ['green', 'blue', 'pink', 'cyan', 'purple', 'brown', 'black']

    @staticmethod
    def get_color():
        if len(Plot._used_colors) >= len(Plot._available_colors):
            Plot._used_colors = []
        for color in Plot._available_colors:
            if color not in Plot._used_colors:
                Plot._used_colors.append(color)
                return color

    @staticmethod
    def plot_graph(graph, algorithms_paths=None):

        if graph.id not in Plot._node_positions: # store graph node position to plot same graph foreach call (same nodes positions) 
            Plot._node_positions[graph.id] = nx.spring_layout(graph, seed=0)

        node_positions = Plot._node_positions[graph.id]

        for node, coord in node_positions.items():
            plt.scatter(coord[0], coord[1], color='red', s=100)
            plt.text(coord[0], coord[1], f"{node}", fontsize=8, ha='center', va='center', color='white')

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
            plt.plot(x_coords, y_coords, 'gray', linewidth=0.5)

        if algorithms_paths:
            for algo_idx, (algo_name, vehicles_paths) in enumerate(algorithms_paths.items()):
                for vehicle, path in vehicles_paths.items():
                    if path:
                        path_coords = [node_positions[node] for node in path if node in node_positions]
                        x_coords, y_coords = zip(*path_coords)
                        plt.plot(x_coords, y_coords, label=f"{algo_name}", color=Plot.get_color(),linewidth=2)
                           

        plt.legend()
        plt.title("Best path of graph" if algorithms_paths else "Graph")
        plt.axis('off') 
        plt.show()

    @staticmethod
    def plot_map(city_coordinates, graph = None, algorithms_paths=None, show_graph = False):
        
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
        m = Basemap(projection='merc', llcrnrlat=min_lat, urcrnrlat=max_lat,llcrnrlon=min_lon, urcrnrlon=max_lon, resolution='i') #todo see cartopy
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


        # Plot paths for each algorithm and vehicle
        if algorithms_paths:
            for algo_idx, (algo_name, vehicles_paths) in enumerate(algorithms_paths.items()):
                for vehicle, path in vehicles_paths.items():
                    if path:
                        path_coords = [city_to_coords[city] for city in path if city in city_to_coords]
                        x_coords, y_coords = zip(*path_coords)
                        plt.plot(x_coords, y_coords, label=f"{algo_name}",color=Plot.get_color(), linewidth=2)



        plt.legend()
        plt.title("Comparison of Algorithms Paths" if algorithms_paths else "Map Graph")
        plt.show()

    @staticmethod
    def plot_distance_over_iterations_comparison(algorithms_results):
        for algo_name, distances in algorithms_results.items():
            plt.plot(distances, label=algo_name, linewidth=2)

        plt.title("Comparison of Trip Length Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Distance")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_iterations_over_node_sizes(algorithms_results):
            plt.plot(algorithms_results, linewidth=2)
            plt.title("Comparison of total iterations over node size")
            plt.xlabel("Node size")
            plt.ylabel("Iteration")
            plt.legend()
            plt.show()

    def plot_time_over_iterations_comparison(algorithms_results,step):
        for algo_name, execution_time in algorithms_results.items():
            iterations = range(step, step * len(execution_time) + 1, step)
            plt.plot(iterations,execution_time, label=algo_name, linewidth=2)

        plt.title("Comparison of execution time over iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Time (in s)")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_iterations_over_node_sizes(algorithms_results):
            plt.plot(algorithms_results, linewidth=2)
            plt.title("Comparison of total iterations over node size")
            plt.xlabel("Node size")
            plt.ylabel("Iteration")
            plt.legend()
            plt.show()


    @staticmethod
    def plot_time_vs_blocked_edges(blocked_percentages, times):
        import matplotlib.pyplot as plt

        plt.figure()
        plt.plot(blocked_percentages, times, marker='o')
        plt.title("Temps d'exécution vs % d'arêtes bloquées")
        plt.xlabel("% d'arêtes bloquées")
        plt.ylabel("Temps d'exécution (s)")
        plt.grid(True)
        plt.show()


    @staticmethod
    def plot_time_vs_node_count(node_counts, times):
        # Filtrer les valeurs None ou invalides
        filtered = [(n, t) for n, t in zip(node_counts, times) if t is not None]
        if not filtered:
            print("Aucune donnée valide à tracer.")
            return

        x, y = zip(*filtered)

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='blue')
        plt.title("Temps d'exécution en fonction du nombre de sommets")
        plt.xlabel("Nombre de sommets")
        plt.ylabel("Temps d'exécution (secondes)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_time_vs_tabu_size(tabu_sizes, times):
        filtered = [(s, t) for s, t in zip(tabu_sizes, times) if t is not None]
        if not filtered:
            print("Aucune donnée valide à tracer.")
            return

        x, y = zip(*filtered)

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='green')
        plt.title("Temps d'exécution en fonction de la taille de la liste tabou")
        plt.xlabel("Taille de la liste tabou")
        plt.ylabel("Temps d'exécution (secondes)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_time_vs_vehicle_count(vehicle_counts, times):
        plt.figure(figsize=(8, 5))
        plt.plot(vehicle_counts, times, marker='o', linestyle='-', color='blue')
        plt.title("Temps d'exécution vs Nombre de véhicules")
        plt.xlabel("Nombre de véhicules")
        plt.ylabel("Temps d'exécution (s)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_distance_vs_node_count(node_counts, distances):
        filtered = [(n, d) for n, d in zip(node_counts, distances) if d is not None]
        if not filtered:
            print("Aucune donnée valide à tracer.")
            return

        x, y = zip(*filtered)

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='purple')
        plt.title("Distance moyenne en fonction du nombre de sommets")
        plt.xlabel("Nombre de sommets")
        plt.ylabel("Distance totale moyenne")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


    @staticmethod
    def plot_distance_vs_tabu_size(tabu_sizes, distances):
        filtered = [(s, d) for s, d in zip(tabu_sizes, distances) if d is not None]
        if not filtered:
            print("Aucune donnée valide à tracer.")
            return

        x, y = zip(*filtered)

        plt.figure(figsize=(8, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='orange')
        plt.title("Distance moyenne en fonction de la taille de la liste tabou")
        plt.xlabel("Taille de la liste tabou")
        plt.ylabel("Distance totale moyenne")
        plt.grid(True)
        plt.tight_layout()
        
    def plot_average_algorithms_distances(algorithms_results):
        for algo_name, stats in algorithms_results.items():
            plt.plot(stats["best"], label=f"{algo_name} - Best", linestyle='--', linewidth=2)
            plt.plot(stats["worst"], label=f"{algo_name} - Worst", linestyle=':', linewidth=2)
            plt.plot(stats["average"], label=f"{algo_name} - Average", linewidth=2)

        plt.title("Algorithm Reliability: Best, Worst, and Average Distances")
        plt.xlabel("Iterations")
        plt.ylabel("Distance")
        plt.legend()
        plt.grid()

        plt.show()
