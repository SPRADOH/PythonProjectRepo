WIDTH = 4
HEIGHT = 2
MAX_SIZE = WIDTH * HEIGHT

items = {
    'r': {'points': 25, 'size': 3},
    'p': {'points': 15, 'size': 2},
    'a': {'points': 15, 'size': 2},
    'm': {'points': 20, 'size': 2},
    'i': {'points': 5,  'size': 1},
    'k': {'points': 15, 'size': 1},
    'x': {'points': 20, 'size': 3},
    't': {'points': 25, 'size': 1},
    'f': {'points': 15, 'size': 1},
    'd': {'points': 10, 'size': 1},
    's': {'points': 20, 'size': 2},
    'c': {'points': 20, 'size': 2},
}

START_POINTS = 15


def knapsack_dp(items, max_size=MAX_SIZE):
    item_list = list(items.keys())
    n = len(item_list)
    
    total_all_points = sum(items[item]['points'] for item in items)
    
    table = [[0 for _ in range(max_size + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = item_list[i - 1]
        points = items[item]['points']
        size = items[item]['size']
        
        for w in range(1, max_size + 1):
            if size > w:
                table[i][w] = table[i - 1][w]
            else:
                table[i][w] = max(table[i - 1][w], 
                                 table[i - 1][w - size] + points)
    
    w = max_size
    selected_items = []
    
    for i in range(n, 0, -1):
        if table[i][w] != table[i - 1][w]:
            item = item_list[i - 1]
            selected_items.append(item)
            w -= items[item]['size']
    
    selected_points = table[n][max_size]
    unselected_points = total_all_points - selected_points
    total_value = START_POINTS + selected_points - unselected_points
    
    return selected_items, total_value


def display_inventory(selected_items, items):
    inventory = [['[ ]' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    pos = 0
    
    for item in selected_items:
        size = items[item]['size']
        for _ in range(size):
            if pos < MAX_SIZE:
                row = pos // WIDTH
                col = pos % WIDTH
                inventory[row][col] = f'[{item}]'
                pos += 1
    
    for row in inventory:
        print(','.join(row))


if __name__ == '__main__':
    selected, score = knapsack_dp(items)
    display_inventory(selected, items)
    print(f'\nFinal survival points: {score}')