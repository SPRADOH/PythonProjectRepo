MAX_VOLUME = 8

items = {
    'r': {'price': 25, 'volume': 3},
    'p': {'price': 15, 'volume': 2},
    'a': {'price': 15, 'volume': 2},
    'm': {'price': 20, 'volume': 2},
    'i': {'price': 5, 'volume': 1},
    'k': {'price': 15, 'volume': 1},
    'x': {'price': 20, 'volume': 3},
    't': {'price': 25, 'volume': 1},
    'f': {'price': 15, 'volume': 1},
    'd': {'price': 10, 'volume': 1},
    's': {'price': 20, 'volume': 2},
    'c': {'price': 20, 'volume': 2},
}

START_POINTS = 15


def knapsack_dp(items, max_volume=MAX_VOLUME):
    item_list = list(items.keys())
    n = len(item_list)
    
    total_all_points = sum(items[item]['price'] for item in items)
    
    table = [[0 for _ in range(max_volume + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        item = item_list[i - 1]
        price = items[item]['price']
        volume = items[item]['volume']
        
        for w in range(1, max_volume + 1):
            if volume > w:
                table[i][w] = table[i - 1][w]
            else:
                table[i][w] = max(table[i - 1][w], 
                                 table[i - 1][w - volume] + price)
    
    w = max_volume
    selected_items = []
    
    for i in range(n, 0, -1):
        if table[i][w] != table[i - 1][w]:
            item = item_list[i - 1]
            selected_items.append(item)
            w -= items[item]['volume']
    
    selected_points = table[n][max_volume]
    unselected_points = total_all_points - selected_points
    total_value = START_POINTS + selected_points - unselected_points
    
    return selected_items, total_value


def display_inventory(selected_items, items):
    inventory = [['[ ]' for _ in range(4)] for _ in range(2)]
    pos = 0
    
    for item in selected_items:
        volume = items[item]['volume']
        for _ in range(volume):
            if pos < 8:
                row = pos // 4
                col = pos % 4
                inventory[row][col] = f'[{item}]'
                pos += 1
    
    for row in inventory:
        print(','.join(row))


if __name__ == '__main__':
    selected, score = knapsack_dp(items)
    display_inventory(selected, items)
    print(f'\nИтоговые очки выживания: {score}')