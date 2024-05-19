import heapq

def dijkstra(members, start_id, end_id):
    distances = {member_id: float('inf') for member_id in members}
    distances[start_id] = 0
    priority_queue = [(0, start_id)]
    predecessors = {start_id: None}

    while priority_queue:
        current_distance, current_id = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_id]:
            continue
        
        for neighbor in members[current_id].following:
            distance = current_distance + 1  # Each edge has weight 1
            if distance < distances[neighbor.member_id]:
                distances[neighbor.member_id] = distance
                predecessors[neighbor.member_id] = current_id
                heapq.heappush(priority_queue, (distance, neighbor.member_id))

    path = []
    current_id = end_id
    while current_id is not None:
        path.insert(0, current_id)
        current_id = predecessors.get(current_id)
    
    if distances[end_id] == float('inf'):
        return None
    return path

def find_highest_engagement_path(members, start_id, end_id):
    # Priority queue to keep track of highest engagement paths
    heap = [(-members[start_id].total_engagement(), start_id, [start_id])]
    best_path = None
    max_engagement = float('-inf')
    visited_paths = set()

    while heap:
        current_engagement, current_id, path = heapq.heappop(heap)
        current_engagement = -current_engagement  # Convert back to positive engagement
        path_tuple = tuple(path)

        if path_tuple in visited_paths:
            continue
        
        visited_paths.add(path_tuple)

        if current_id == end_id:
            if current_engagement > max_engagement:
                max_engagement = current_engagement
                best_path = path
            continue
        
        for neighbor in members[current_id].following:
            if neighbor.member_id not in path:
                new_engagement = current_engagement + neighbor.total_engagement()
                new_path = path + [neighbor.member_id]
                heapq.heappush(heap, (-new_engagement, neighbor.member_id, new_path))
                print(f"    Adding path: {new_path} with engagement {new_engagement}")
    
    return best_path, max_engagement if best_path else (None, None)



