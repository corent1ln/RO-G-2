import random
import networkx as nx
import matplotlib.pyplot as plt
import random as rd


def generate_weighted_matrix(n, min_degree=2, max_degree=5, min_weight=1, max_weight=20):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    degrees = [0] * n

    # Liste des paires possibles
    all_pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    random.shuffle(all_pairs)

    for i, j in all_pairs:
        if degrees[i] < max_degree and degrees[j] < max_degree:
            weight = random.randint(min_weight, max_weight)
            matrix[i][j] = weight
            matrix[j][i] = weight
            degrees[i] += 1
            degrees[j] += 1

    # Correction : s'assurer qu'aucun sommet n'a moins que le degré minimum
    for i in range(n):
        while degrees[i] < min_degree:
            # Trouver un sommet j qui peut accepter une arête
            possible = [j for j in range(n) if j != i and matrix[i][j] == 0 and degrees[j] < max_degree]
            if not possible:
                break
            j = random.choice(possible)
            weight = random.randint(min_weight, max_weight)
            matrix[i][j] = weight
            matrix[j][i] = weight
            degrees[i] += 1
            degrees[j] += 1

    return matrix



# Générer et dessiner le graphe
matrix = generate_weighted_matrix(10)
matrix = [[0, 0, 4, 0, 7, 18, 0, 16, 2, 0], [0, 0, 0, 0, 0, 0, 12, 0, 12, 17], [4, 0, 0, 16, 0, 5, 0, 16, 11, 0], [0, 0, 16, 0, 8, 5, 12, 16, 0, 0], [7, 0, 0, 8, 0, 10, 0, 1, 0, 5], [18, 0, 5, 5, 10, 0, 17, 0, 0, 0], [0, 12, 0, 12, 0, 17, 0, 0, 11, 11], [16, 0, 16, 16, 1, 0, 0, 0, 0, 10], [2, 12, 11, 0, 0, 0, 11, 0, 0, 3], [0, 17, 0, 0, 5, 0, 11, 10, 3, 0]]



def afficher_graphe(G):
    pos = nx.spring_layout(G, seed=42) 
    edge_labels = nx.get_edge_attributes(G, 'weight')

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Graphe Pondéré")
    plt.axis('off') 
    plt.show()


def construire_graphe(matrice):
    G = nx.Graph()  
    n = len(matrice)
    for i in range(n):
        for j in range(n):
            poids = matrice[i][j]
            if poids != 0:
                G.add_edge(i, j, weight=poids)
    return G


def get_chemins(matrix,points_de_livraison, point_depart):
    chemins = []
    points_de_livraison.insert(0,point_depart)
    for i in points_de_livraison: 
        for j in points_de_livraison:
            if i != j:
                path = nx.dijkstra_path(matrix,i,j)
                chemins.append(path)
            else:
                chemins.append([i, j])
    return chemins


def get_sousmatrice(chemins, matrix, points_demandes):
    matrice_modifiee = []
    taille = len(matrix)
    pointA = []
    pointB = []
    row=[]
    G = nx.Graph()

    for i, j in enumerate(chemins): 
        if j[0] == j[-1]:
            ponderation_chemin = 0
        else:
            ponderation_chemin = calculer_distance_total(j, matrix) 
            G.add_edge(j[0], j[-1], weight=ponderation_chemin)

    return G


 
def generer_voisins(tour):
    neighbors = []
    for i in range(len(tour)):
        for j in range(i + 1, len(tour)):
            neighbor = tour[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append((neighbor, (i, j))) 
    return neighbors

def calculer_distance_total(tour, graph):
    distance = 0
    for i in range(len(tour)-1):
        u = tour[i]
        v = tour[(i + 1)]
        try:
            distance += graph[u][v]['weight']
        
        except KeyError:
            # Pas de chemin direct entre u et v
            distance += float('inf')  # Ou gérer comme tu veux
    return distance



def generer_solution_aleatoire(matrix, points_de_livraison, point_de_depart, seed=None):
    points_de_livraison.remove(0)
    if seed is not None:
        random.seed(seed)
    random.shuffle(points_de_livraison)
    points_de_livraison.insert(0,point_de_depart)
    points_de_livraison.append(point_de_depart)

    print("Solution générée :", points_de_livraison)
    return points_de_livraison




def recherche_tabou(matrix, iterations,point_de_depart, points_de_livraison, taille_liste_tabou):
    afficher_graphe(matrix)
    chemin = get_chemins(matrix, points_de_livraison, point_de_depart)
    matrice_modifiee = get_sousmatrice(chemin,matrix, points_demandes)
    afficher_graphe(matrice_modifiee)

    n = len(points_de_livraison)
    current_solution = generer_solution_aleatoire(matrice_modifiee,points_de_livraison, point_de_depart )
    best_solution = current_solution[:]
    best_distance = calculer_distance_total(current_solution, matrice_modifiee)
    print(best_distance)
    liste_tabou = []
    for i in range (iterations):
        
        neighbors = generer_voisins(current_solution)
        neighbors = sorted(neighbors, key=lambda x: calculer_distance_total(x[0], matrice_modifiee))

        for neighbor, move in neighbors:
            if move not in liste_tabou:
                current_solution = neighbor
                current_distance = calculer_distance_total(current_solution, matrice_modifiee)

                if current_distance < best_distance:
                    best_solution = current_solution[:]
                    best_distance = current_distance

                liste_tabou.append(move)
                if len(liste_tabou) > taille_liste_tabou:
                    liste_tabou.pop(0)
                break

        #print(f"Iteration {i+1}: Best Distance = {best_distance}")

    final_path = [points_de_livraison[i] for i in best_solution]
    return final_path, best_distance


points_demandes = [1, 2, 4, 3, 6, 7]

best_tour, best_distance = recherche_tabou(construire_graphe(matrix), iterations=50,point_de_depart=0, points_de_livraison=points_demandes, taille_liste_tabou=10)
#print("Best tour (points demandés) :", best_tour)
#print("Best distance :", best_distance)