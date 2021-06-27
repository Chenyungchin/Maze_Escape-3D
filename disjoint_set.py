def initialize(width, height):
    n = width*height
    leader = [i for i in range(n)]
    rank = [0]*n
    edges = []
    for i in range(height):
        for j in range(width):
            if j != width-1:
                edges.append((i*width+j, i*width+j+1))
            if i != height-1:
                edges.append((i*width+j, (i+1)*width+j))
    return leader, rank, edges

def find(x, leader):
    if x == leader[x]:
        return x
    return find(leader[x], leader)

def merge(x, y, leader, rank):
    x = find(x, leader)
    y = find(y, leader)
    if x == y:
        return False
    if rank[x] > rank[y]:
        leader[y] = x
    else:
        leader[x] = y
        if rank[x] == rank[y]:
            rank[y] += 1
    return True
    
if __name__ == "__main__":
    leader, rank, edges = initialize(4, 3)
    print(edges)