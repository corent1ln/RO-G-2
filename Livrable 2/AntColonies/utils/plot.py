
import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.basemap import Basemap

class Plot:

    @staticmethod
    def plot_graph(graph, path=None):

        node_positions = nx.spring_layout(graph)

        for node, coord in node_positions.items():
            plt.scatter(coord[0], coord[1], color='red', s=100, label="Node" if node == list(graph.nodes)[0] else "")
            plt.text(coord[0], coord[1], f"{node}", fontsize=8, ha='center', va='center', color='white')

        for u, v, data in graph.edges(data=True):
            x_coords = [node_positions[u][0], node_positions[v][0]]
            y_coords = [node_positions[u][1], node_positions[v][1]]
            
            if path and (u, v) in zip(path, path[1:]) or (v, u) in zip(path, path[1:]):
                plt.plot(x_coords, y_coords, 'blue', linewidth=2)
            else:
                plt.plot(x_coords, y_coords, 'gray', linewidth=0.5) 

        plt.title("Best path of graph")
        plt.axis('off') 
        plt.show()

    @staticmethod
    def plot_france_map(city_coordinates, path=None):
        plt.figure(figsize=(10, 8))
        m = Basemap(projection='merc', llcrnrlat=41, urcrnrlat=51.5, llcrnrlon=-5, urcrnrlon=9, resolution='i')

        m.drawcoastlines()
        m.drawcountries()
        m.drawmapboundary(fill_color='lightblue')
        m.fillcontinents(color='lightgreen', lake_color='lightblue')

        for city, (lat, lon) in city_coordinates.items():
            x, y = m(lon, lat)
            plt.plot(x, y, 'ro', markersize=5)
            plt.text(x, y, city, fontsize=8, ha='left', color='black')

        if path:
            path_coords = [m(city_coordinates[city][1], city_coordinates[city][0]) for city in path]
            path_x, path_y = zip(*path_coords)
            plt.plot(path_x, path_y, 'b-', linewidth=2, label='Chemin optimal')
            plt.plot(path_x[0], path_y[0], 'go', markersize=8, label='Départ/Arrivée') 
            
        plt.legend()
        plt.title("Carte de la France avec le chemin optimal")
        plt.show()

    # Plotting the distance over iterations (second plot) - Shows how the path length improves over time
    @staticmethod
    def plot_distance_over_iterations(best_distance_history):
        # Plot the best distance found in each iteration (should decrease over time)
        plt.plot(best_distance_history, color='green', linewidth=2)
        plt.title("Trip Length Over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Distance")
        plt.show()
