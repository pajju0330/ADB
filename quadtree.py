# Vaishnavi Ladda PRN:21610076
import pyodbc
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary = boundary
        self.points = []
        self.children = [None, None, None, None]

    def is_leaf(self):
        return all(child is None for child in self.children)
    
    

class QuadTree:
    def __init__(self, boundary, max_points=4, max_depth=10):
        self.root = QuadTreeNode(boundary)
        self.max_points = max_points
        self.max_depth = max_depth

    def insert(self, point):
        self._insert_recursive(self.root, point, depth=0)

    def _contains(self, boundary, point):
        return boundary.x_min <= point.x <= boundary.x_max and boundary.y_min <= point.y <= boundary.y_max

    def _insert_recursive(self, node, point, depth):
        if not self._contains(node.boundary, point):
            return False  # Point is outside the node's boundary

        if len(node.points) < self.max_points or depth >= self.max_depth:
            node.points.append(point)
            return True

        if all(child is None for child in node.children):
            self._split_node(node)  # Split the node if it's a leaf and reached max points or max depth

        # Recursively insert the point into one of the child nodes
        for child in node.children:
            if self._insert_recursive(child, point, depth + 1):
                return True

        return False
    
    def _split_node(self, node):
        x_mid = (node.boundary.x_min + node.boundary.x_max) / 2
        y_mid = (node.boundary.y_min + node.boundary.y_max) / 2

        # Create four child nodes with updated boundaries
        node.children[0] = QuadTreeNode(Boundary(node.boundary.x_min, x_mid, node.boundary.y_min, y_mid))  # NW
        node.children[1] = QuadTreeNode(Boundary(x_mid, node.boundary.x_max, node.boundary.y_min, y_mid))  # NE
        node.children[2] = QuadTreeNode(Boundary(node.boundary.x_min, x_mid, y_mid, node.boundary.y_max))  # SW
        node.children[3] = QuadTreeNode(Boundary(x_mid, node.boundary.x_max, y_mid, node.boundary.y_max))  # SE

        # Reinsert existing points into child nodes
        for point in node.points:
            for child in node.children:
                if self._contains(child.boundary, point):
                    self._insert_recursive(child, point, depth=0)

        node.points = [] 

    def display_tree(self):
        self._display_recursive(self.root, depth=0)

    def _display_recursive(self, node, depth):
        if node is None:
            return

        prefix = "  " * depth
        print(f"{prefix}Depth {depth}: Boundary ({node.boundary.x_min}, {node.boundary.y_min}) to ({node.boundary.x_max}, {node.boundary.y_max})")

        if node.is_leaf():
            points_info = ", ".join([f"({point.x}, {point.y})" for point in node.points])
            print(f"{prefix}  Leaf Node with {len(node.points)} points: {points_info}")
        else:
            for child_idx, child in enumerate(node.children):
                print(f"{prefix}  Child {child_idx + 1}:")
                self._display_recursive(child, depth + 1)

    def serialize(self):
        return pickle.dumps(self.root)

    @staticmethod
    def deserialize(serialized_data):
        root_node = pickle.loads(serialized_data)
        quadtree = QuadTree(Boundary(0, 100, 0, 100))  # Create a new QuadTree instance with default boundary
        quadtree.root = root_node
        return quadtree
    
   
    
class Boundary:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

# Connect to MSSQL Server
conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=DESKTOP-U4LPBNM\SQLEXPRESS;'
                      'DATABASE=ADT;'
                      'UID=sa;'
                      'PWD=1234')

cursor = conn.cursor()

# Create a table to store Quadtree data if it doesn't exist
cursor.execute('''IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'QuadtreeData')
                    CREATE TABLE QuadtreeData (
                        id INT PRIMARY KEY IDENTITY(1,1),
                        serialized_data VARBINARY(MAX)
                    )''')
conn.commit()

# Example usage
boundary = Boundary(x_min=0, x_max=100, y_min=0, y_max=100)
quadtree = QuadTree(boundary)

points_to_insert = [(20, 30), (40, 50), (60, 70), (80, 90)]
for x, y in points_to_insert:
    point = Point(x, y)
    quadtree.insert(point)

# Insert Quadtree into the database
serialized_quadtree = quadtree.serialize()
cursor.execute('INSERT INTO QuadtreeData (serialized_data) VALUES (?)', (serialized_quadtree,))
conn.commit()

# Retrieve Quadtree from the database
cursor.execute('SELECT TOP 1 serialized_data FROM QuadtreeData ORDER BY id DESC')
serialized_data = cursor.fetchone()[0]
# print(serialized_data)
reconstructed_quadtree = QuadTree.deserialize(serialized_data)
# print("Reconstructed Quadtree:", reconstructed_quadtree)
reconstructed_quadtree.display_tree()


# Close the database connection
conn.close()