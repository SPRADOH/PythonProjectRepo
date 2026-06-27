import random
import os

class Room:
    """Represents a room in the dungeon"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + width // 2
        self.center_y = y + height // 2

class DungeonGenerator:
    """Generates dungeon maps using rooms and corridors"""
    
    def __init__(self, width=60, height=30, room_count=10):
        self.width = width
        self.height = height
        self.room_count = room_count
        self.rooms = []
        self.map = [['#' for _ in range(width)] for _ in range(height)]
    
    def generate(self):
        """Generate the dungeon map"""
        self.rooms = []
        self.map = [['#' for _ in range(self.width)] for _ in range(self.height)]
        
        # Generate rooms
        for _ in range(self.room_count):
            room_width = random.randint(4, 10)
            room_height = random.randint(4, 8)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            
            new_room = Room(x, y, room_width, room_height)
            
            # Check if overlaps with existing rooms
            overlaps = False
            for room in self.rooms:
                if (x < room.x + room.width and x + room_width > room.x and
                    y < room.y + room.height and y + room_height > room.y):
                    overlaps = True
                    break
            
            if not overlaps:
                self.rooms.append(new_room)
                self._carve_room(new_room)
        
        # Connect rooms with corridors
        for i in range(len(self.rooms) - 1):
            self._connect_rooms(self.rooms[i], self.rooms[i + 1])
        
        return self.map
    
    def _carve_room(self, room):
        """Carve a room into the map"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                self.map[y][x] = '.'
    
    def _connect_rooms(self, room1, room2):
        """Connect two rooms with an L-shaped corridor"""
        x1, y1 = room1.center_x, room1.center_y
        x2, y2 = room2.center_x, room2.center_y
        
        # Horizontal then vertical
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[y1][x] = '.'
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[y][x2] = '.'
    
    def display(self):
        """Display the dungeon map as ASCII"""
        print("\n" + "=" * (self.width + 4))
        print("🗺️ DUNGEON MAP")
        print("=" * (self.width + 4))
        
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if self.map[y][x] == '#':
                    row += "█"
                else:
                    row += " "
            print(row)
        
        print("=" * (self.width + 4))
        print(f"Rooms: {len(self.rooms)}")
        print("█ = Wall, (space) = Floor")
        print("=" * (self.width + 4))
    
    def save_to_file(self, filename="dungeon.txt"):
        """Save the dungeon map to a text file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("DUNGEON MAP\n")
            f.write("=" * self.width + "\n")
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    if self.map[y][x] == '#':
                        row += "█"
                    else:
                        row += " "
                f.write(row + "\n")
            f.write("=" * self.width + "\n")
            f.write(f"Rooms: {len(self.rooms)}\n")
        return filename

class DungeonApp:
    """Main application class for dungeon generation"""
    
    def __init__(self):
        self.generator = None
        self.filename = "dungeon.txt"
    
    def run(self):
        """Run the dungeon generator menu"""
        while True:
            self._show_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self._generate_new_dungeon()
            elif choice == '2':
                self._show_dungeon()
            elif choice == '3':
                self._save_dungeon()
            elif choice == '4':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Try again.")
    
    def _show_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 50)
        print("🏰 DUNGEON GENERATOR")
        print("=" * 50)
        print("1. Generate new dungeon")
        print("2. Show dungeon")
        print("3. Save dungeon to file")
        print("4. Exit")
        print("=" * 50)
    
    def _generate_new_dungeon(self):
        """Generate a new dungeon map"""
        try:
            width = int(input("Enter width (default 60): ") or "60")
            height = int(input("Enter height (default 30): ") or "30")
            rooms = int(input("Enter number of rooms (default 10): ") or "10")
        except ValueError:
            print("❌ Invalid input. Using defaults.")
            width, height, rooms = 60, 30, 10
        
        self.generator = DungeonGenerator(width, height, rooms)
        self.generator.generate()
        print(f"✅ New dungeon generated with {len(self.generator.rooms)} rooms!")
    
    def _show_dungeon(self):
        """Display the current dungeon"""
        if self.generator:
            self.generator.display()
        else:
            print("❌ No dungeon generated yet. Generate one first!")
    
    def _save_dungeon(self):
        """Save the dungeon to a file"""
        if self.generator:
            filename = self.generator.save_to_file()
            print(f"✅ Dungeon saved to {filename}")
        else:
            print("❌ No dungeon to save. Generate one first!")

if __name__ == '__main__':
    app = DungeonApp()
    app.run()