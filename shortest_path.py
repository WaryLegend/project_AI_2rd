import heapq
from math import sqrt

# Tính toán khoảng cách giữa 2 tỉnh liền kề
def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Tạo ra đồ thị của bản đồ
def create_province_graph(southern_vietnam, provinces, adjacency_list):
    G = {}
    # Thêm các tỉnh vào đồ thị với vị trí của chúng
    for province in provinces:
        province_shape = southern_vietnam[southern_vietnam['NAME_1'] == province]
        coords = province_shape.geometry.centroid
        G[province] = {'pos': (coords.x.iloc[0], coords.y.iloc[0]), 'neighbors': {}}
    
    # Tính khoảng cách giữa các tỉnh liền kề và cập nhật đồ thị
    for province1, province2 in adjacency_list:
        coord1 = G[province1]['pos']
        coord2 = G[province2]['pos']
        distance = calculate_distance(coord1, coord2)
        # Vì là đồ thị vô hướng
        G[province1]['neighbors'][province2] = distance
        G[province2]['neighbors'][province1] = distance  
    
    return G

# Tìm đường đi ngắn nhất 
# Thuật toán Dijkstra
def find_shortest_path(graph, start, end):
    # Khoảng cách ngắn nhất từ start tới mọi node, ban đầu đặt là vô cực
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Lưu trữ đường đi (parent) để truy vết đường đi ngắn nhất
    previous_nodes = {node: None for node in graph}
    # Hàng đợi ưu tiên, ban đầu chỉ có điểm start với khoảng cách 0
    priority_queue = [(0, start)]  # (distance, node)
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        # Nếu đã đến đích, kết thúc
        if current_node == end:
            break
        # Nếu khoảng cách hiện tại lớn hơn khoảng cách đã biết, bỏ qua
        if current_distance > distances[current_node]:
            continue
        # Duyệt qua các đỉnh lân cận
        for neighbor, weight in graph[current_node]['neighbors'].items():
            distance = current_distance + weight
            # Nếu tìm được đường đi ngắn hơn, cập nhật khoảng cách và parent
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    # Truy vết đường đi từ start đến end
    path = []
    current_node = end
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    
    return path

def plot_shortest_path(ax, graph, path):
    coords = [graph[province]['pos'] for province in path]
    x, y = zip(*coords)
    return ax.plot(x, y, color='blue', linewidth=1, marker='o')