import random
import datetime
import re
import traceback
from typing import List, Dict, Any, Tuple, Set

from backend.database.connection import SessionLocal

from backend.models.user import User
from backend.models.question import Question
from backend.models.solve import Solve
from backend.models.revision import Revision
from backend.models.recommendation import Recommendation

random.seed(42)
BATCH_SIZE = 2000

# ============================================================
# NAMES & EMAIL DATA
# ============================================================

FIRST_NAMES = [
    "James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia",
    "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Charlotte", "Alexander",
    "Amelia", "Daniel", "Harper", "Michael", "Evelyn", "Ethan", "Abigail",
    "Sebastian", "Emily", "Jack", "Elizabeth", "Owen", "Sofia", "Aiden",
    "Avery", "Samuel", "Ella", "Ryan", "Scarlett", "Nathan", "Grace",
    "Leo", "Chloe", "Adam", "Victoria", "Dylan", "Riley", "Oscar", "Aria",
    "Matthew", "Lily", "David", "Aurora", "Joseph", "Zoey", "Andrew", "Nora",
    "John", "Camila", "Robert", "Hannah", "Luke", "Layla", "Thomas", "Lillian",
    "Marcus", "Addison", "Kevin", "Eleanor", "Brian", "Stella", "Jason",
    "Natalie", "Chris", "Zoe", "Patrick", "Leah", "Jordan", "Hazel", "Eric",
    "Violet", "Brandon", "Savannah", "Tyler", "Audrey", "Carlos", "Brooklyn",
    "Mason", "Bella", "Caleb", "Claire", "Isaac", "Skylar", "Joshua", "Lucy",
    "Evan", "Paisley", "Angel", "Ellie", "Ian", "Peyton", "Miles", "Anna",
    "Blake", "Caroline", "Juan", "Nova", "Diego", "Genesis", "Alex", "Emilia",
    "Adrian", "Kennedy", "Carter", "Maya", "Luis", "Sarah", "Jaxon", "Madelyn",
    "Hunter", "Alexa", "Gavin", "Ariana", "Connor", "Elena", "Jayden",
    "Gabriella", "Xavier", "Naomi", "Jose", "Alice", "Chase", "Sadie", "Gael",
    "Hailey", "Landon", "Eva", "Roman", "Nico", "Aaliyah", "Ezra", "Eliana",
    "Kai", "Willow", "Theo", "Ivy", "Finn", "Luna", "Axel", "Ruby",
    "Ryder", "Penelope", "Jasper", "Clara", "Sawyer", "Vivian", "Declan",
    "Madeline", "Oliver", "Isabelle", "Silas", "Rylee", "Beau", "Sophie",
    "Hugo", "Emmett", "Emery", "Atlas", "Piper", "Felix", "Lydia", "Winston",
    "Ayla", "Nash", "Lyla", "Rowan", "Kinsley", "Graham", "Jade", "Dominic",
    "Serenity", "Colton", "Valentina", "Camden", "Delilah", "Ryker", "Jace",
    "Samantha", "Grant", "Cora", "Thiago", "Kaylee", "Brayden", "Fiona",
    "Giovanni", "Tessa", "Malachi", "Sienna", "Walter", "Natalia", "Dean",
    "Brielle", "Harrison", "Callie", "Braxton", "Beckett", "Adalyn", "Maddox",
    "Emerson", "Londyn", "Paxton", "Eden", "Greyson", "Fallon", "Hope",
    "Remy", "Julia", "Enzo", "Athena", "Arlo", "Iris", "Gideon", "Quinn",
    "Bennett", "Daisy", "Caden", "Ximena", "Shane", "Cecilia", "Kingston",
    "Alina", "Milo", "Allison", "Hendrix", "Lena", "Bryce", "Harley", "River",
    "Gianna", "Knox", "Lila", "Sean", "Elsie", "Dante", "Reagan", "Rocco",
    "Mackenzie", "Chance", "Myra", "Phoenix", "Caden", "Brooks", "Haven",
    "Karter", "Makenna", "Brantley", "Sariah", "Jett", "Raelynn", "Dax",
    "Lainey", "Kash", "Marlee", "Colt", "Ansley", "Zeke", "Kaydence", "Beckham",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz",
    "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
    "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan",
    "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos",
    "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez",
    "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long",
    "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell",
    "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales",
    "Griffin", "Sanders", "Hayes", "Murray", "Ford", "Marshall", "Owens",
]

EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com",
    "icloud.com", "mail.com", "zoho.com", "fastmail.com", "tutanota.com",
]


def slugify_title(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[\(\)\[\]]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    s = re.sub(r"-+", "-", s)
    return s


# ============================================================
# 500 REAL LEETCODE PROBLEMS
# Format: (title, topic, pattern, difficulty, [tags])
# ============================================================

QUESTIONS_RAW: List[Tuple[str, str, str, str, List[str]]] = [
    # --- Arrays (35) ---
    ("Two Sum", "Arrays", "Hashing", "Easy", ["Array", "Hash Table"]),
    ("Best Time to Buy and Sell Stock", "Arrays", "Greedy", "Easy", ["Array", "Dynamic Programming"]),
    ("Contains Duplicate", "Arrays", "Hashing", "Easy", ["Array", "Hash Table"]),
    ("Product of Array Except Self", "Arrays", "Arrays", "Medium", ["Array", "Prefix Sum"]),
    ("Maximum Subarray", "Arrays", "Dynamic Programming", "Medium", ["Array", "Divide and Conquer", "Dynamic Programming"]),
    ("Find Minimum in Rotated Sorted Array", "Arrays", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Search in Rotated Sorted Array", "Arrays", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Three Sum", "Arrays", "Two Pointers", "Medium", ["Array", "Two Pointers", "Sorting"]),
    ("Container With Most Water", "Arrays", "Two Pointers", "Medium", ["Array", "Two Pointers", "Greedy"]),
    ("Trapping Rain Water", "Arrays", "Two Pointers", "Hard", ["Array", "Two Pointers", "Stack", "Dynamic Programming"]),
    ("Rotate Array", "Arrays", "Arrays", "Medium", ["Array", "Math", "Two Pointers"]),
    ("Jump Game", "Arrays", "Greedy", "Medium", ["Array", "Dynamic Programming", "Greedy"]),
    ("Jump Game II", "Arrays", "Greedy", "Medium", ["Array", "Greedy", "Dynamic Programming"]),
    ("Merge Sorted Array", "Arrays", "Two Pointers", "Easy", ["Array", "Two Pointers", "Sorting"]),
    ("Remove Duplicates from Sorted Array", "Arrays", "Two Pointers", "Easy", ["Array", "Two Pointers"]),
    ("Move Zeroes", "Arrays", "Two Pointers", "Easy", ["Array", "Two Pointers"]),
    ("Majority Element", "Arrays", "Hashing", "Easy", ["Array", "Hash Table", "Divide and Conquer", "Sorting", "Counting"]),
    ("Top K Frequent Elements", "Arrays", "Heap", "Medium", ["Array", "Hash Table", "Divide and Conquer", "Sorting", "Heap", "Bucket Sort", "Counting"]),
    ("Subarray Sum Equals K", "Arrays", "Hashing", "Medium", ["Array", "Hash Table", "Prefix Sum"]),
    ("Sliding Window Maximum", "Arrays", "Monotonic Stack", "Hard", ["Array", "Heap", "Sliding Window", "Monotonic Queue", "Deque"]),
    ("First Missing Positive", "Arrays", "Arrays", "Hard", ["Array", "Hash Table"]),
    ("Spiral Matrix", "Arrays", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),
    ("Rotate Image", "Arrays", "Matrix", "Medium", ["Array", "Matrix", "Math"]),
    ("Set Matrix Zeroes", "Arrays", "Matrix", "Medium", ["Array", "Hash Table", "Matrix"]),
    ("Pascal's Triangle", "Arrays", "Dynamic Programming", "Easy", ["Array", "Dynamic Programming"]),
    ("Pascal's Triangle II", "Arrays", "Dynamic Programming", "Easy", ["Array", "Dynamic Programming"]),
    ("Plus One", "Arrays", "Arrays", "Easy", ["Array", "Math"]),
    ("Spiral Matrix II", "Arrays", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),
    ("Merge Intervals", "Arrays", "Intervals", "Medium", ["Array", "Sorting"]),
    ("Insert Interval", "Arrays", "Intervals", "Medium", ["Array"]),
    ("4Sum", "Arrays", "Two Pointers", "Medium", ["Array", "Two Pointers", "Sorting"]),
    ("Combination Sum", "Arrays", "Backtracking", "Medium", ["Array", "Backtracking"]),
    ("Subarray Product Less Than K", "Arrays", "Sliding Window", "Medium", ["Array", "Sliding Window"]),
    ("Find Peak Element", "Arrays", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Search a 2D Matrix", "Arrays", "Binary Search", "Medium", ["Array", "Binary Search", "Matrix"]),

    # --- Strings (30) ---
    ("Longest Substring Without Repeating Characters", "Strings", "Sliding Window", "Medium", ["Hash Table", "String", "Sliding Window"]),
    ("Longest Repeating Character Replacement", "Strings", "Sliding Window", "Medium", ["Hash Table", "String", "Sliding Window"]),
    ("Minimum Window Substring", "Strings", "Sliding Window", "Hard", ["Hash Table", "String", "Sliding Window"]),
    ("Valid Anagram", "Strings", "Hashing", "Easy", ["Hash Table", "String", "Sorting"]),
    ("Group Anagrams", "Strings", "Hashing", "Medium", ["Array", "Hash Table", "String", "Sorting"]),
    ("Valid Parentheses", "Strings", "Stack", "Easy", ["String", "Stack"]),
    ("Reverse String", "Strings", "Two Pointers", "Easy", ["Two Pointers", "String"]),
    ("Find the Index of the First Occurrence in a String", "Strings", "Two Pointers", "Easy", ["Two Pointers", "String", "String Matching"]),
    ("String to Integer (atoi)", "Strings", "Strings", "Medium", ["String"]),
    ("Longest Common Prefix", "Strings", "Strings", "Easy", ["String", "Trie"]),
    ("Palindromic Substrings", "Strings", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Decode String", "Strings", "Stack", "Medium", ["String", "Stack", "Recursion"]),
    ("Count and Say", "Strings", "Recursion", "Medium", ["String"]),
    ("Reverse Words in a String", "Strings", "Strings", "Medium", ["Two Pointers", "String"]),
    ("Roman to Integer", "Strings", "Math", "Easy", ["Hash Table", "Math", "String"]),
    ("Integer to Roman", "Strings", "Math", "Medium", ["Hash Table", "Math", "String"]),
    ("Longest Palindromic Substring", "Strings", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Zigzag Conversion", "Strings", "Strings", "Medium", ["String"]),
    ("Add Binary", "Strings", "Math", "Easy", ["Math", "String", "Simulation"]),
    ("Multiply Strings", "Strings", "Math", "Medium", ["Math", "String"]),
    ("Length of Last Word", "Strings", "Strings", "Easy", ["String"]),
    ("Repeated Substring Pattern", "Strings", "Strings", "Easy", ["String", "String Matching"]),
    ("Longest Valid Parentheses", "Strings", "Stack", "Hard", ["String", "Dynamic Programming", "Stack"]),
    ("Minimum Add to Make Parentheses Valid", "Strings", "Stack", "Medium", ["String", "Stack", "Greedy"]),
    ("Add Strings", "Strings", "Math", "Easy", ["Math", "String", "Simulation"]),
    ("Partition Labels", "Strings", "Greedy", "Medium", ["Hash Table", "Two Pointers", "String", "Greedy"]),
    ("Isomorphic Strings", "Strings", "Hashing", "Easy", ["Hash Table", "String"]),
    ("Word Pattern", "Strings", "Hashing", "Easy", ["Hash Table", "String"]),
    ("Compare Version Numbers", "Strings", "Two Pointers", "Medium", ["Two Pointers", "String"]),
    ("Ransom Note", "Strings", "Hashing", "Easy", ["Hash Table", "String", "Counting"]),

    # --- Hashing (15) ---
    ("Longest Consecutive Sequence", "Hashing", "Hashing", "Medium", ["Array", "Hash Table", "Union Find"]),
    ("Happy Number", "Hashing", "Hashing", "Easy", ["Hash Table", "Math", "Two Pointers"]),
    ("Contains Duplicate II", "Hashing", "Hashing", "Easy", ["Array", "Hash Table", "Sliding Window"]),
    ("Single Number", "Hashing", "Bit Manipulation", "Easy", ["Bit Manipulation"]),
    ("Find the Duplicate Number", "Hashing", "Two Pointers", "Medium", ["Array", "Two Pointers", "Binary Search", "Bit Manipulation"]),
    ("Valid Sudoku", "Hashing", "Hashing", "Medium", ["Array", "Hash Table", "Matrix"]),
    ("Sort Characters By Frequency", "Hashing", "Heap", "Medium", ["Hash Table", "String", "Sorting", "Heap", "Bucket Sort", "Counting"]),
    ("Top K Frequent Words", "Hashing", "Heap", "Medium", ["Hash Table", "String", "Trie", "Sorting", "Heap", "Bucket Sort"]),
    ("Keyboard Row", "Hashing", "Hashing", "Easy", ["Array", "Hash Table", "String"]),
    ("Find Anagram Mappings", "Hashing", "Hashing", "Easy", ["Array", "Hash Table"]),
    ("Subarray Sums Divisible by K", "Hashing", "Hashing", "Medium", ["Array", "Hash Table", "Prefix Sum"]),
    ("Longest Harmonious Subsequence", "Hashing", "Hashing", "Easy", ["Array", "Hash Table", "Sorting"]),
    ("Set Mismatch", "Hashing", "Hashing", "Easy", ["Array", "Hash Table", "Math", "Bit Manipulation", "Sorting"]),
    ("Distribute Candies", "Hashing", "Hashing", "Easy", ["Array", "Hash Table"]),
    ("Image Smoother", "Hashing", "Matrix", "Easy", ["Array", "Matrix"]),

    # --- Two Pointers (18) ---
    ("Valid Palindrome", "Two Pointers", "Two Pointers", "Easy", ["Two Pointers", "String"]),
    ("Two Sum II - Input Array Is Sorted", "Two Pointers", "Two Pointers", "Medium", ["Array", "Two Pointers", "Binary Search"]),
    ("3Sum Closest", "Two Pointers", "Two Pointers", "Medium", ["Array", "Two Pointers", "Sorting"]),
    ("Sort Colors", "Two Pointers", "Two Pointers", "Medium", ["Array", "Two Pointers", "Sorting"]),
    ("Minimum Size Subarray Sum", "Two Pointers", "Sliding Window", "Medium", ["Array", "Binary Search", "Sliding Window", "Prefix Sum"]),
    ("Squares of a Sorted Array", "Two Pointers", "Two Pointers", "Easy", ["Array", "Two Pointers", "Sorting"]),
    ("Backspace String Compare", "Two Pointers", "Two Pointers", "Easy", ["Two Pointers", "String", "Stack", "Simulation"]),
    ("Is Subsequence", "Two Pointers", "Two Pointers", "Easy", ["Two Pointers", "String", "Dynamic Programming"]),
    ("Reverse Vowels of a String", "Two Pointers", "Two Pointers", "Easy", ["Two Pointers", "String"]),
    ("Shortest Word Distance", "Two Pointers", "Two Pointers", "Easy", ["Array", "String", "Two Pointers"]),
    ("Valid Word Abbreviation", "Two Pointers", "Two Pointers", "Easy", ["Two Pointers", "String"]),
    ("Boats to Save People", "Two Pointers", "Greedy", "Medium", ["Array", "Two Pointers", "Sorting", "Greedy"]),
    ("Sum of Square Numbers", "Two Pointers", "Two Pointers", "Medium", ["Math", "Two Pointers"]),
    ("Valid Triangle Number", "Two Pointers", "Two Pointers", "Medium", ["Array", "Two Pointers", "Binary Search", "Sorting"]),

    # --- Sliding Window (15) ---
    ("Permutation in String", "Sliding Window", "Sliding Window", "Medium", ["Hash Table", "Two Pointers", "String", "Sliding Window"]),
    ("Find All Anagrams in a String", "Sliding Window", "Sliding Window", "Medium", ["Hash Table", "String", "Sliding Window"]),
    ("Maximum Average Subarray I", "Sliding Window", "Sliding Window", "Easy", ["Array", "Sliding Window"]),
    ("Longest Subarray of 1's After Deleting One Element", "Sliding Window", "Sliding Window", "Medium", ["Array", "Dynamic Programming", "Sliding Window"]),
    ("Minimum Operations to Reduce X to Zero", "Sliding Window", "Sliding Window", "Medium", ["Array", "Hash Table", "Binary Search", "Sliding Window", "Prefix Sum"]),
    ("Count Number of Nice Subarrays", "Sliding Window", "Sliding Window", "Medium", ["Array", "Hash Table", "Math", "Sliding Window", "Prefix Sum"]),
    ("Number of Substrings Containing All Three Characters", "Sliding Window", "Sliding Window", "Medium", ["Hash Table", "String", "Sliding Window"]),
    ("Replace the Substring for Balanced String", "Sliding Window", "Sliding Window", "Medium", ["String", "Sliding Window"]),
    ("Max Consecutive Ones III", "Sliding Window", "Sliding Window", "Medium", ["Array", "Binary Search", "Sliding Window", "Prefix Sum"]),
    ("Fruit Into Baskets", "Sliding Window", "Sliding Window", "Medium", ["Array", "Hash Table", "Sliding Window"]),
    ("Longest Nice Subarray", "Sliding Window", "Sliding Window", "Medium", ["Array", "Bit Manipulation", "Sliding Window"]),
    ("Grumpy Bookstore Owner", "Sliding Window", "Sliding Window", "Medium", ["Array", "Sliding Window"]),
    ("Maximum Number of Vowels in a Substring of Given Length", "Sliding Window", "Sliding Window", "Medium", ["String", "Sliding Window"]),
    ("Count Substrings with Only One Distinct Letter", "Sliding Window", "Sliding Window", "Easy", ["String", "Sliding Window"]),
    ("Get Equal Substrings Within Budget", "Sliding Window", "Sliding Window", "Medium", ["String", "Sliding Window"]),

    # --- Binary Search (18) ---
    ("Binary Search", "Binary Search", "Binary Search", "Easy", ["Array", "Binary Search"]),
    ("Search Insert Position", "Binary Search", "Binary Search", "Easy", ["Array", "Binary Search"]),
    ("Find First and Last Position of Element in Sorted Array", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Koko Eating Bananas", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Capacity To Ship Packages Within D Days", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search", "Greedy"]),
    ("Split Array Largest Sum", "Binary Search", "Binary Search", "Hard", ["Array", "Binary Search", "Dynamic Programming", "Greedy"]),
    ("Median of Two Sorted Arrays", "Binary Search", "Binary Search", "Hard", ["Array", "Binary Search", "Divide and Conquer"]),
    ("Guess Number Higher or Lower", "Binary Search", "Binary Search", "Easy", ["Binary Search", "Interactive"]),
    ("Search in Rotated Sorted Array II", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Single Element in a Sorted Array", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Find Right Interval", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search", "Sorting"]),
    ("Minimum Speed to Arrive on Time", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Kth Missing Positive Number", "Binary Search", "Binary Search", "Easy", ["Array", "Binary Search"]),
    ("Sqrt(x)", "Binary Search", "Binary Search", "Easy", ["Math", "Binary Search"]),
    ("Search a 2D Matrix II", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search", "Divide and Conquer", "Matrix"]),
    ("Find Minimum in Rotated Sorted Array II", "Binary Search", "Binary Search", "Hard", ["Array", "Binary Search"]),
    ("Peak Index in a Mountain Array", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search"]),
    ("Minimum Limit of Balls in a Bag", "Binary Search", "Binary Search", "Medium", ["Array", "Binary Search", "Sorting"]),

    # --- Trees (28) ---
    ("Maximum Depth of Binary Tree", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search", "Recursion"]),
    ("Same Tree", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search"]),
    ("Invert Binary Tree", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"]),
    ("Binary Tree Level Order Traversal", "Trees", "BFS", "Medium", ["Tree", "Breadth-First Search", "Binary Tree"]),
    ("Validate Binary Search Tree", "Trees", "DFS", "Medium", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),
    ("Lowest Common Ancestor of a Binary Tree", "Trees", "DFS", "Medium", ["Tree", "Depth-First Search", "Binary Tree"]),
    ("Binary Tree Maximum Path Sum", "Trees", "DFS", "Hard", ["Tree", "Depth-First Search", "Dynamic Programming", "Binary Tree"]),
    ("Serialize and Deserialize Binary Tree", "Trees", "DFS", "Hard", ["Tree", "Depth-First Search", "Breadth-First Search", "String", "Design"]),
    ("Construct Binary Tree from Preorder and Inorder Traversal", "Trees", "DFS", "Medium", ["Array", "Hash Table", "Divide and Conquer", "Tree", "Binary Tree"]),
    ("Flatten Binary Tree to Linked List", "Trees", "DFS", "Medium", ["Linked List", "Stack", "Tree", "Depth-First Search", "Binary Tree"]),
    ("Path Sum", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Binary Tree"]),
    ("Path Sum II", "Trees", "DFS", "Medium", ["Tree", "Depth-First Search", "Backtracking", "Binary Tree"]),
    ("Binary Tree Right Side View", "Trees", "BFS", "Medium", ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"]),
    ("Symmetric Tree", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"]),
    ("Balanced Binary Tree", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Binary Tree"]),
    ("Diameter of Binary Tree", "Trees", "DFS", "Easy", ["Tree", "Depth-First Search", "Binary Tree"]),
    ("Minimum Depth of Binary Tree", "Trees", "BFS", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"]),
    ("Populating Next Right Pointers in Each Node", "Trees", "BFS", "Medium", ["Tree", "Depth-First Search", "Breadth-First Search", "Linked List", "Binary Tree"]),
    ("Count Good Nodes in Binary Tree", "Trees", "DFS", "Medium", ["Tree", "Depth-First Search", "Binary Tree"]),
    ("Maximum Level Sum of a Binary Tree", "Trees", "BFS", "Medium", ["Tree", "Breadth-First Search", "Binary Tree"]),
    ("Find Largest Value in Each Tree Row", "Trees", "BFS", "Medium", ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"]),
    ("Convert Sorted Array to Binary Search Tree", "Trees", "DFS", "Easy", ["Tree", "Binary Search Tree", "Array", "Divide and Conquer", "Binary Tree"]),
    ("Construct Binary Tree from Inorder and Postorder Traversal", "Trees", "DFS", "Medium", ["Array", "Hash Table", "Divide and Conquer", "Tree", "Binary Tree"]),
    ("Binary Tree Zigzag Level Order Traversal", "Trees", "BFS", "Medium", ["Tree", "Breadth-First Search", "Binary Tree"]),
    ("Delete Node in a BST", "Trees", "BST", "Medium", ["Tree", "Binary Search Tree", "Binary Tree"]),
    ("Binary Tree Preorder Traversal", "Trees", "DFS", "Easy", ["Stack", "Tree", "Depth-First Search", "Binary Tree"]),
    ("Binary Tree Postorder Traversal", "Trees", "DFS", "Easy", ["Stack", "Tree", "Depth-First Search", "Binary Tree"]),
    ("Binary Tree Inorder Traversal", "Trees", "DFS", "Easy", ["Stack", "Tree", "Depth-First Search", "Binary Tree"]),
    ("Average of Levels in Binary Tree", "Trees", "BFS", "Easy", ["Tree", "Breadth-First Search", "Binary Tree"]),

    # --- BST (10) ---
    ("Search in a Binary Search Tree", "BST", "BST", "Easy", ["Tree", "Binary Search Tree", "Binary Tree"]),
    ("Insert into a Binary Search Tree", "BST", "BST", "Medium", ["Tree", "Binary Search Tree", "Binary Tree"]),
    ("Kth Smallest Element in a BST", "BST", "DFS", "Medium", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),
    ("Two Sum IV - Input is a BST", "BST", "BST", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Search Tree", "Hash Table", "Binary Tree"]),
    ("Minimum Absolute Difference in BST", "BST", "DFS", "Easy", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),
    ("Closest Binary Search Tree Value", "BST", "BST", "Easy", ["Tree", "Binary Search Tree", "Binary Tree", "Binary Search"]),
    ("Inorder Successor in BST", "BST", "BST", "Medium", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),
    ("Convert BST to Greater Tree", "BST", "DFS", "Medium", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),
    ("Recover Binary Search Tree", "BST", "DFS", "Medium", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),
    ("Range Sum of BST", "BST", "DFS", "Easy", ["Tree", "Depth-First Search", "Binary Search Tree", "Binary Tree"]),

    # --- Graphs (18) ---
    ("Number of Islands", "Graphs", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Clone Graph", "Graphs", "DFS", "Medium", ["Hash Table", "Depth-First Search", "Breadth-First Search", "Graph"]),
    ("Course Schedule", "Graphs", "Topological Sort", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"]),
    ("Course Schedule II", "Graphs", "Topological Sort", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"]),
    ("Pacific Atlantic Water Flow", "Graphs", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Matrix"]),
    ("Graph Valid Tree", "Graphs", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Number of Connected Components in an Undirected Graph", "Graphs", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Cheapest Flights Within K Stops", "Graphs", "Shortest Path", "Medium", ["Dynamic Programming", "Heap", "Graph", "Shortest Path"]),
    ("Network Delay Time", "Graphs", "Shortest Path", "Medium", ["Heap", "Graph", "Shortest Path"]),
    ("Redundant Connection", "Graphs", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Is Graph Bipartite?", "Graphs", "BFS", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Keys and Rooms", "Graphs", "DFS", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph"]),
    ("Possible Bipartition", "Graphs", "BFS", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Evaluate Division", "Graphs", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Graph", "Shortest Path"]),
    ("The Maze", "Graphs", "DFS", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph", "Matrix"]),
    ("Number of Provinces", "Graphs", "DFS", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph", "Matrix"]),
    ("Find if Path Exists in Graph", "Graphs", "BFS", "Easy", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Minimum Number of Vertices to Reach All Nodes", "Graphs", "Graphs", "Medium", ["Graph"]),
    ("Maximum Depth of N-ary Tree", "Graphs", "DFS", "Easy", ["Tree", "Depth-First Search", "Breadth-First Search"]),

    # --- DFS (22) ---
    ("Surrounded Regions", "DFS", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Word Search", "DFS", "DFS", "Medium", ["Array", "Backtracking", "Matrix", "Depth-First Search"]),
    ("Word Search II", "DFS", "Trie", "Hard", ["Array", "String", "Backtracking", "Trie", "Matrix", "Depth-First Search"]),
    ("Combinations", "DFS", "Backtracking", "Medium", ["Backtracking"]),
    ("Permutations", "DFS", "Backtracking", "Medium", ["Array", "Backtracking"]),
    ("Subsets", "DFS", "Backtracking", "Medium", ["Array", "Backtracking", "Bit Manipulation"]),
    ("Combination Sum II", "DFS", "Backtracking", "Medium", ["Array", "Backtracking"]),
    ("All Paths From Source to Target", "DFS", "DFS", "Medium", ["Backtracking", "Depth-First Search", "Graph"]),
    ("Max Area of Island", "DFS", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Making A Large Island", "DFS", "Union Find", "Hard", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Reconstruct Itinerary", "DFS", "DFS", "Hard", ["Depth-First Search", "Graph"]),
    ("Cracking the Safe", "DFS", "DFS", "Hard", ["Depth-First Search", "String", "Backtracking", "Graph"]),
    ("Matchsticks to Square", "DFS", "Backtracking", "Medium", ["Array", "Dynamic Programming", "Backtracking", "Bit Manipulation"]),
    ("Number of Enclaves", "DFS", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Matrix"]),
    ("Accounts Merge", "DFS", "Union Find", "Medium", ["Array", "String", "Depth-First Search", "Breadth-First Search", "Union Find"]),
    ("Critical Connections in a Network", "DFS", "DFS", "Hard", ["Depth-First Search", "Graph", "Biconnected Component"]),
    ("Minimize Malware Spread", "DFS", "DFS", "Hard", ["Array", "Depth-First Search", "Matrix", "Union Find"]),
    ("Splitting a String Into Descending Consecutive Values", "DFS", "DFS", "Medium", ["String", "Backtracking", "Depth-First Search"]),
    ("N-ary Tree Preorder Traversal", "DFS", "DFS", "Easy", ["Stack", "Tree", "Depth-First Search"]),
    ("N-ary Tree Postorder Traversal", "DFS", "DFS", "Easy", ["Stack", "Tree", "Depth-First Search"]),
    ("Time Needed to Inform All Employees", "DFS", "DFS", "Medium", ["Tree", "Depth-First Search", "Breadth-First Search"]),
    ("Find Eventual Safe States", "DFS", "Topological Sort", "Medium", ["Depth-First Search", "Graph", "Topological Sort", "Array"]),

    # --- BFS (14) ---
    ("Rotting Oranges", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Shortest Path in Binary Matrix", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Open the Lock", "BFS", "BFS", "Medium", ["Breadth-First Search", "Array", "Hash Table", "String"]),
    ("Word Ladder", "BFS", "BFS", "Hard", ["Hash Table", "String", "Breadth-First Search"]),
    ("Walls and Gates", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("01 Matrix", "BFS", "BFS", "Medium", ["Array", "Dynamic Programming", "Breadth-First Search", "Matrix"]),
    ("As Far from Land as Possible", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix", "Dynamic Programming"]),
    ("Nearest Exit from Entrance in Maze", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Minimum Genetic Mutation", "BFS", "BFS", "Medium", ["Hash Table", "String", "Breadth-First Search"]),
    ("Snakes and Ladders", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Ladder Length", "BFS", "BFS", "Medium", ["Hash Table", "String", "Breadth-First Search"]),
    ("Shortest Path to Get Food", "BFS", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Couples Holding Hands", "BFS", "Union Find", "Hard", ["Depth-First Search", "Union Find", "Graph"]),
    ("Minimum Jumps to Reach Home", "BFS", "BFS", "Medium", ["Array", "Hash Table", "Breadth-First Search"]),

    # --- Backtracking (18) ---
    ("N-Queens", "Backtracking", "Backtracking", "Hard", ["Array", "Backtracking"]),
    ("N-Queens II", "Backtracking", "Backtracking", "Hard", ["Backtracking"]),
    ("Sudoku Solver", "Backtracking", "Backtracking", "Hard", ["Array", "Backtracking", "Matrix"]),
    ("Generate Parentheses", "Backtracking", "Backtracking", "Medium", ["String", "Dynamic Programming", "Backtracking"]),
    ("Letter Combinations of a Phone Number", "Backtracking", "Backtracking", "Medium", ["Hash Table", "String", "Backtracking"]),
    ("Subsets II", "Backtracking", "Backtracking", "Medium", ["Array", "Backtracking", "Bit Manipulation"]),
    ("Permutations II", "Backtracking", "Backtracking", "Medium", ["Array", "Hash Table", "Backtracking"]),
    ("Combination Sum III", "Backtracking", "Backtracking", "Medium", ["Array", "Backtracking"]),
    ("Partition to K Equal Sum Subsets", "Backtracking", "Backtracking", "Medium", ["Array", "Backtracking", "Dynamic Programming", "Bit Manipulation"]),
    ("Palindrome Partitioning", "Backtracking", "Backtracking", "Medium", ["String", "Dynamic Programming", "Backtracking"]),
    ("Restore IP Addresses", "Backtracking", "Backtracking", "Medium", ["String", "Backtracking"]),
    ("Word Break II", "Backtracking", "Backtracking", "Hard", ["Array", "Hash Table", "String", "Dynamic Programming", "Backtracking", "Trie", "Memoization"]),
    ("Unique Paths III", "Backtracking", "Backtracking", "Hard", ["Array", "Backtracking", "Bit Manipulation", "Matrix"]),
    ("Flip Game II", "Backtracking", "Backtracking", "Medium", ["Math", "Backtracking", "Memoization", "Game Theory"]),
    ("Beautiful Arrangement", "Backtracking", "Backtracking", "Medium", ["Array", "Backtracking", "Bit Manipulation", "Dynamic Programming"]),

    # --- Recursion (10) ---
    ("Swap Nodes in Pairs", "Recursion", "Linked List", "Medium", ["Linked List", "Recursion"]),
    ("Pow(x, n)", "Recursion", "Binary Search", "Medium", ["Math", "Binary Search", "Recursion"]),
    ("Merge Two Sorted Lists", "Recursion", "Linked List", "Easy", ["Linked List", "Recursion"]),
    ("Reverse Linked List", "Recursion", "Linked List", "Easy", ["Linked List", "Recursion"]),
    ("Linked List Cycle", "Recursion", "Two Pointers", "Easy", ["Linked List", "Two Pointers"]),
    ("Palindrome Linked List", "Recursion", "Linked List", "Easy", ["Linked List", "Two Pointers", "Stack", "Recursion"]),
    ("Merge k Sorted Lists", "Recursion", "Heap", "Hard", ["Linked List", "Divide and Conquer", "Heap", "Merge Sort"]),
    ("Sort List", "Recursion", "Linked List", "Medium", ["Linked List", "Two Pointers", "Divide and Conquer", "Sorting", "Merge Sort"]),
    ("Reorder List", "Recursion", "Linked List", "Medium", ["Linked List", "Two Pointers", "Stack", "Recursion"]),
    ("Fibonacci Number", "Recursion", "Dynamic Programming", "Easy", ["Math", "Dynamic Programming", "Memoization", "Recursion"]),

    # --- Greedy (18) ---
    ("Assign Cookies", "Greedy", "Greedy", "Easy", ["Array", "Sorting", "Greedy"]),
    ("Non-overlapping Intervals", "Greedy", "Intervals", "Medium", ["Array", "Dynamic Programming", "Sorting", "Greedy"]),
    ("Minimum Number of Arrows to Burst Balloons", "Greedy", "Intervals", "Medium", ["Array", "Sorting", "Greedy"]),
    ("Task Scheduler", "Greedy", "Greedy", "Medium", ["Array", "Hash Table", "Sorting", "Greedy", "Heap", "Counting"]),
    ("Candy", "Greedy", "Greedy", "Hard", ["Array", "Greedy"]),
    ("Gas Station", "Greedy", "Greedy", "Medium", ["Array", "Greedy"]),
    ("Broken Calculator", "Greedy", "Greedy", "Medium", ["Math", "Greedy"]),
    ("Maximum Units on a Truck", "Greedy", "Greedy", "Easy", ["Array", "Sorting", "Greedy"]),
    ("Smallest Range II", "Greedy", "Greedy", "Medium", ["Array", "Math", "Sorting", "Greedy"]),
    ("Minimum Deletions to Make Character Frequencies Unique", "Greedy", "Greedy", "Medium", ["String", "Hash Table", "Greedy", "Counting", "Sorting"]),
    ("Minimum Domino Rotations For Equal Row", "Greedy", "Greedy", "Medium", ["Array", "Greedy"]),
    ("Lemonade Change", "Greedy", "Greedy", "Easy", ["Array", "Greedy"]),
    ("Minimum Cost of Buying Candies With Discount", "Greedy", "Greedy", "Easy", ["Array", "Sorting", "Greedy"]),
    ("Largest Perimeter Triangle", "Greedy", "Greedy", "Easy", ["Array", "Math", "Sorting", "Greedy"]),
    ("Maximum Performance of a Team", "Greedy", "Greedy", "Hard", ["Array", "Sorting", "Heap", "Greedy"]),
    ("Minimum Number of Refueling Stops", "Greedy", "Heap", "Hard", ["Dynamic Programming", "Heap", "Greedy"]),
    ("Reducing Dishes", "Greedy", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming", "Greedy", "Sorting"]),
    ("Wiggle Subsequence", "Greedy", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Greedy"]),

    # --- Heap (14) ---
    ("Kth Largest Element in an Array", "Heap", "Heap", "Medium", ["Array", "Divide and Conquer", "Sorting", "Heap", "Quickselect"]),
    ("Find Median from Data Stream", "Heap", "Heap", "Hard", ["Two Pointers", "Design", "Sorting", "Heap", "Data Stream"]),
    ("K Closest Points to Origin", "Heap", "Heap", "Medium", ["Array", "Math", "Sorting", "Heap", "Divide and Conquer", "Geometry"]),
    ("Reorganize String", "Heap", "Heap", "Medium", ["Hash Table", "String", "Greedy", "Sorting", "Heap", "Counting"]),
    ("Last Stone Weight", "Heap", "Heap", "Easy", ["Array", "Heap"]),
    ("Ugly Number II", "Heap", "Dynamic Programming", "Medium", ["Hash Table", "Math", "Dynamic Programming", "Heap"]),
    ("Kth Largest Element in a Stream", "Heap", "Heap", "Easy", ["Tree", "Binary Search Tree", "Binary Tree", "Heap", "Design", "Data Stream"]),
    ("Find K Pairs with Smallest Sums", "Heap", "Heap", "Medium", ["Array", "Heap"]),
    ("Meeting Rooms III", "Heap", "Heap", "Hard", ["Array", "Sorting", "Heap", "Counting", "Ordered Set"]),
    ("Total Cost to Hire K Workers", "Heap", "Heap", "Medium", ["Array", "Two Pointers", "Heap", "Sorting"]),
    ("Find the Kth Largest Integer in the Array", "Heap", "Heap", "Medium", ["String", "Heap", "Divide and Conquer", "Quickselect", "Sorting"]),
    ("Single-Threaded CPU", "Heap", "Heap", "Medium", ["Array", "Sorting", "Heap"]),
    ("The K Weakest Rows in a Matrix", "Heap", "Heap", "Easy", ["Array", "Sorting", "Heap", "Matrix"]),
    ("Minimum Obstacle Removal at Corner", "Heap", "Shortest Path", "Hard", ["Array", "Breadth-First Search", "Heap", "Graph", "Matrix", "Shortest Path"]),

    # --- Stack (16) ---
    ("Min Stack", "Stack", "Stack", "Medium", ["Stack", "Design"]),
    ("Evaluate Reverse Polish Notation", "Stack", "Stack", "Medium", ["Array", "Math", "Stack"]),
    ("Daily Temperatures", "Stack", "Monotonic Stack", "Medium", ["Array", "Stack", "Monotonic Stack"]),
    ("Next Greater Element I", "Stack", "Monotonic Stack", "Easy", ["Array", "Hash Table", "Stack", "Monotonic Stack"]),
    ("Largest Rectangle in Histogram", "Stack", "Monotonic Stack", "Hard", ["Array", "Stack", "Monotonic Stack"]),
    ("Basic Calculator", "Stack", "Stack", "Hard", ["String", "Stack", "Math"]),
    ("Basic Calculator II", "Stack", "Stack", "Medium", ["String", "Stack", "Math"]),
    ("Remove Duplicate Letters", "Stack", "Monotonic Stack", "Medium", ["String", "Stack", "Monotonic Stack", "Greedy"]),
    ("Online Stock Span", "Stack", "Monotonic Stack", "Medium", ["Stack", "Design", "Monotonic Stack", "Data Stream"]),
    ("Sum of Subarray Minimums", "Stack", "Monotonic Stack", "Medium", ["Array", "Dynamic Programming", "Stack", "Monotonic Stack"]),
    ("Number of Visible People in a Queue", "Stack", "Monotonic Stack", "Hard", ["Array", "Stack", "Monotonic Stack"]),
    ("Asteroid Collision", "Stack", "Stack", "Medium", ["Array", "Stack", "Simulation"]),
    ("Score of Parentheses", "Stack", "Stack", "Medium", ["String", "Stack"]),
    ("Next Greater Element II", "Stack", "Monotonic Stack", "Medium", ["Array", "Stack", "Monotonic Stack"]),
    ("Remove K Digits", "Stack", "Monotonic Stack", "Medium", ["String", "Stack", "Greedy", "Monotonic Stack"]),
    ("Simplify Path", "Stack", "Stack", "Medium", ["String", "Stack"]),

    # --- Queue (10) ---
    ("Implement Queue using Stacks", "Queue", "Stack", "Easy", ["Stack", "Design", "Queue"]),
    ("Design Circular Queue", "Queue", "Queue", "Medium", ["Array", "Linked List", "Design", "Queue"]),
    ("Number of Recent Calls", "Queue", "Queue", "Easy", ["Design", "Queue", "Data Stream"]),
    ("Dota2 Senate", "Queue", "Queue", "Medium", ["String", "Queue", "Greedy"]),
    ("Reveal Cards In Increasing Order", "Queue", "Queue", "Medium", ["Array", "Queue", "Sorting", "Simulation"]),
    ("Design Circular Deque", "Queue", "Queue", "Medium", ["Array", "Linked List", "Design", "Queue"]),
    ("Time Needed to Buy Tickets", "Queue", "Queue", "Easy", ["Array", "Queue", "Simulation"]),
    ("Shortest Subarray with Sum at Least K", "Queue", "Monotonic Stack", "Hard", ["Array", "Queue", "Sliding Window", "Monotonic Queue", "Prefix Sum"]),

    # --- Trie (12) ---
    ("Implement Trie (Prefix Tree)", "Trie", "Trie", "Medium", ["String", "Hash Table", "Design", "Trie"]),
    ("Design Add and Search Words Data Structure", "Trie", "Trie", "Medium", ["String", "Depth-First Search", "Design", "Trie"]),
    ("Longest Word in Dictionary", "Trie", "Trie", "Medium", ["Array", "String", "Trie", "Sorting"]),
    ("Replace Words", "Trie", "Trie", "Medium", ["Array", "Hash Table", "String", "Trie"]),
    ("Map Sum Pairs", "Trie", "Trie", "Medium", ["Hash Table", "String", "Trie", "Design"]),
    ("Search Suggestions System", "Trie", "Trie", "Medium", ["Array", "String", "Trie", "Sorting", "Binary Search"]),
    ("Concatenated Words", "Trie", "Trie", "Hard", ["Array", "String", "Dynamic Programming", "Trie", "Memoization"]),
    ("Word Break", "Trie", "Dynamic Programming", "Medium", ["Array", "Hash Table", "String", "Dynamic Programming", "Trie", "Memoization"]),
    ("Word Break II", "Trie", "Backtracking", "Hard", ["Array", "Hash Table", "String", "Dynamic Programming", "Backtracking", "Trie", "Memoization"]),
    ("Subtree of Another Tree", "Trie", "DFS", "Easy", ["Tree", "Depth-First Search", "String Matching", "Binary Tree", "Hash Function"]),
    ("Add and Search Word", "Trie", "Trie", "Medium", ["String", "Depth-First Search", "Design", "Trie"]),
    ("Prefix and Suffix Search", "Trie", "Trie", "Hard", ["String", "Trie", "Design"]),

    # --- Segment Tree (6) ---
    ("Range Sum Query - Mutable", "Segment Tree", "Segment Tree", "Medium", ["Array", "Design", "Binary Indexed Tree", "Segment Tree"]),
    ("Range Sum Query 2D - Immutable", "Segment Tree", "Prefix Sum", "Medium", ["Array", "Matrix", "Prefix Sum", "Design"]),
    ("Count of Range Sum", "Segment Tree", "Segment Tree", "Hard", ["Array", "Binary Search", "Divide and Conquer", "Binary Indexed Tree", "Segment Tree", "Merge Sort"]),
    ("My Calendar I", "Segment Tree", "Segment Tree", "Medium", ["Array", "Binary Search", "Design", "Segment Tree", "Ordered Set"]),
    ("Range Module", "Segment Tree", "Segment Tree", "Hard", ["Design", "Segment Tree", "Ordered Set", "Binary Indexed Tree"]),
    ("Create Sorted Array through Instructions", "Segment Tree", "Fenwick Tree", "Hard", ["Array", "Binary Search", "Binary Indexed Tree", "Segment Tree", "Ordered Set", "Merge Sort"]),

    # --- Fenwick Tree (5) ---
    ("Count of Smaller Numbers After Self", "Fenwick Tree", "Fenwick Tree", "Hard", ["Array", "Binary Search", "Divide and Conquer", "Binary Indexed Tree", "Segment Tree", "Merge Sort", "Ordered Set"]),
    ("Reverse Pairs", "Fenwick Tree", "Fenwick Tree", "Hard", ["Array", "Binary Search", "Divide and Conquer", "Binary Indexed Tree", "Segment Tree", "Merge Sort", "Ordered Set"]),
    ("Longest Increasing Subsequence", "Fenwick Tree", "Dynamic Programming", "Medium", ["Array", "Binary Search", "Dynamic Programming"]),
    ("Query Kth Smallest Trimmed Number", "Fenwick Tree", "Sorting", "Hard", ["Array", "String", "Sorting", "Heap"]),
    ("Falling Squares", "Fenwick Tree", "Segment Tree", "Hard", ["Array", "Ordered Set", "Segment Tree"]),

    # --- Bit Manipulation (14) ---
    ("Number of 1 Bits", "Bit Manipulation", "Bit Manipulation", "Easy", ["Divide and Conquer", "Bit Manipulation"]),
    ("Counting Bits", "Bit Manipulation", "Dynamic Programming", "Easy", ["Dynamic Programming", "Bit Manipulation"]),
    ("Reverse Bits", "Bit Manipulation", "Bit Manipulation", "Easy", ["Divide and Conquer", "Bit Manipulation"]),
    ("Missing Number", "Bit Manipulation", "Bit Manipulation", "Easy", ["Array", "Hash Table", "Math", "Binary Search", "Bit Manipulation", "Sorting"]),
    ("Power of Two", "Bit Manipulation", "Bit Manipulation", "Easy", ["Math", "Bit Manipulation"]),
    ("Power of Four", "Bit Manipulation", "Bit Manipulation", "Easy", ["Math", "Bit Manipulation"]),
    ("Hamming Distance", "Bit Manipulation", "Bit Manipulation", "Easy", ["Bit Manipulation"]),
    ("Total Hamming Distance", "Bit Manipulation", "Bit Manipulation", "Medium", ["Bit Manipulation"]),
    ("Single Number II", "Bit Manipulation", "Bit Manipulation", "Medium", ["Array", "Bit Manipulation"]),
    ("Single Number III", "Bit Manipulation", "Bit Manipulation", "Medium", ["Bit Manipulation"]),
    ("Bitwise AND of Numbers Range", "Bit Manipulation", "Bit Manipulation", "Medium", ["Bit Manipulation"]),
    ("Maximum Product of Word Lengths", "Bit Manipulation", "Bit Manipulation", "Medium", ["Array", "String", "Bit Manipulation"]),
    ("Gray Code", "Bit Manipulation", "Backtracking", "Medium", ["Backtracking", "Math", "Bit Manipulation"]),

    # --- Dynamic Programming (48) ---
    ("Climbing Stairs", "Dynamic Programming", "Dynamic Programming", "Easy", ["Math", "Dynamic Programming", "Memoization"]),
    ("Coin Change", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Breadth-First Search"]),
    ("House Robber", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("House Robber II", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("House Robber III", "Dynamic Programming", "DFS", "Medium", ["Tree", "Depth-First Search", "Dynamic Programming", "Binary Tree"]),
    ("Decode Ways", "Dynamic Programming", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Unique Paths", "Dynamic Programming", "Dynamic Programming", "Medium", ["Math", "Dynamic Programming", "Combinatorics"]),
    ("Unique Paths II", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Matrix"]),
    ("Minimum Path Sum", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Matrix"]),
    ("Edit Distance", "Dynamic Programming", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Longest Common Subsequence", "Dynamic Programming", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Regular Expression Matching", "Dynamic Programming", "Dynamic Programming", "Hard", ["String", "Dynamic Programming", "Recursion"]),
    ("Wildcard Matching", "Dynamic Programming", "Dynamic Programming", "Hard", ["String", "Dynamic Programming", "Greedy", "Recursion"]),
    ("Partition Equal Subset Sum", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("Target Sum", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Backtracking"]),
    ("Perfect Squares", "Dynamic Programming", "Dynamic Programming", "Medium", ["Math", "Dynamic Programming", "Breadth-First Search"]),
    ("Triangle", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("Minimum Cost Climbing Stairs", "Dynamic Programming", "Dynamic Programming", "Easy", ["Array", "Dynamic Programming"]),
    ("N-th Tribonacci Number", "Dynamic Programming", "Dynamic Programming", "Easy", ["Math", "Dynamic Programming", "Memoization"]),
    ("Number of Longest Increasing Subsequence", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Binary Search", "Segment Tree"]),
    ("Russian Doll Envelopes", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Binary Search", "Dynamic Programming", "Sorting"]),
    ("Largest Divisible Subset", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Math", "Sorting"]),
    ("Interleaving String", "Dynamic Programming", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Distinct Subsequences", "Dynamic Programming", "Dynamic Programming", "Hard", ["String", "Dynamic Programming"]),
    ("Minimum ASCII Delete Sum for Two Strings", "Dynamic Programming", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Ones and Zeroes", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "String", "Dynamic Programming"]),
    ("Partition Array for Maximum Sum", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("Longest Palindromic Subsequence", "Dynamic Programming", "Dynamic Programming", "Medium", ["String", "Dynamic Programming"]),
    ("Palindrome Partitioning II", "Dynamic Programming", "Dynamic Programming", "Hard", ["String", "Dynamic Programming"]),
    ("Burst Balloons", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming"]),
    ("Best Time to Buy and Sell Stock with Cooldown", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("Best Time to Buy and Sell Stock II", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming", "Greedy"]),
    ("Best Time to Buy and Sell Stock III", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming"]),
    ("Best Time to Buy and Sell Stock IV", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming"]),
    ("Coin Change II", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("Maximal Rectangle", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Stack", "Dynamic Programming", "Matrix"]),
    ("Cherry Pickup", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming", "Matrix"]),
    ("Dungeon Game", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming", "Matrix"]),
    ("Out of Boundary Paths", "Dynamic Programming", "Dynamic Programming", "Medium", ["Dynamic Programming"]),
    ("Knight Probability in Chessboard", "Dynamic Programming", "Dynamic Programming", "Medium", ["Dynamic Programming"]),
    ("Strange Printer", "Dynamic Programming", "Dynamic Programming", "Hard", ["String", "Dynamic Programming"]),
    ("Remove Boxes", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming", "Memoization"]),
    ("Longest Increasing Path in a Matrix", "Dynamic Programming", "DFS", "Hard", ["Array", "Depth-First Search", "Dynamic Programming", "Matrix"]),
    ("Stone Game", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Math", "Dynamic Programming", "Game Theory"]),
    ("Paint House", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Dynamic Programming"]),
    ("Paint House II", "Dynamic Programming", "Dynamic Programming", "Hard", ["Array", "Dynamic Programming"]),
    ("Word Break", "Dynamic Programming", "Dynamic Programming", "Medium", ["Array", "Hash Table", "String", "Dynamic Programming", "Trie", "Memoization"]),
    ("Minimum Swaps to Make Strings Equal", "Dynamic Programming", "Greedy", "Medium", ["String", "Greedy", "Math"]),
    ("Egg Drop With 2 Eggs and N Floors", "Dynamic Programming", "Dynamic Programming", "Medium", ["Math", "Dynamic Programming"]),
    ("Count Vowels Permutation", "Dynamic Programming", "Dynamic Programming", "Hard", ["Dynamic Programming", "Math"]),

    # --- Math (22) ---
    ("Reverse Integer", "Math", "Math", "Medium", ["Math"]),
    ("Palindrome Number", "Math", "Math", "Easy", ["Math"]),
    ("Excel Sheet Column Title", "Math", "Math", "Easy", ["Math", "String"]),
    ("Excel Sheet Column Number", "Math", "Math", "Easy", ["Math", "String"]),
    ("Ugly Number", "Math", "Math", "Easy", ["Math"]),
    ("Count Primes", "Math", "Math", "Medium", ["Array", "Math", "Enumeration", "Number Theory"]),
    ("Fraction to Recurring Decimal", "Math", "Math", "Medium", ["Hash Table", "Math", "String"]),
    ("Detect Squares", "Math", "Math", "Medium", ["Array", "Hash Table", "Design", "Math", "Counting"]),
    ("Super Pow", "Math", "Math", "Medium", ["Math"]),
    ("Self Dividing Numbers", "Math", "Math", "Easy", ["Math"]),
    ("Robot Bounded In Circle", "Math", "Math", "Medium", ["Math", "Geometry"]),
    ("Construct the Rectangle", "Math", "Math", "Easy", ["Math"]),
    ("Reach a Number", "Math", "Math", "Medium", ["Math", "Binary Search"]),
    ("Consecutive Numbers Sum", "Math", "Math", "Medium", ["Math"]),
    ("Smallest Integer Divisible by K", "Math", "Math", "Medium", ["Hash Table", "Math"]),
    ("Rotate String", "Math", "Math", "Easy", ["String", "Math"]),
    ("Lucky Numbers in a Matrix", "Math", "Matrix", "Easy", ["Array", "Matrix"]),
    ("Integer Break", "Math", "Dynamic Programming", "Medium", ["Math", "Dynamic Programming"]),
    ("Arranging Coins", "Math", "Math", "Easy", ["Math", "Binary Search"]),
    ("Rectangle Area", "Math", "Geometry", "Easy", ["Math", "Geometry"]),
    ("Complex Number Multiplication", "Math", "Math", "Medium", ["Math", "String"]),
    ("Spiral Matrix III", "Math", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),

    # --- Geometry (6) ---
    ("Max Points on a Line", "Geometry", "Geometry", "Hard", ["Array", "Hash Table", "Math", "Geometry"]),
    ("Convex Polygon", "Geometry", "Geometry", "Medium", ["Math", "Geometry"]),
    ("Valid Boomerang", "Geometry", "Geometry", "Easy", ["Math", "Geometry"]),
    ("Rectangle Overlap", "Geometry", "Geometry", "Easy", ["Math", "Geometry"]),
    ("Minimum Area Rectangle", "Geometry", "Geometry", "Medium", ["Array", "Hash Table", "Math", "Geometry", "Sorting"]),
    ("Projection Area of 3D Shapes", "Geometry", "Geometry", "Easy", ["Array", "Math", "Geometry"]),

    # --- Linked List (22) ---
    ("Add Two Numbers", "Linked List", "Linked List", "Medium", ["Linked List", "Math", "Recursion"]),
    ("Add Two Numbers II", "Linked List", "Linked List", "Medium", ["Linked List", "Math", "Stack"]),
    ("Rotate List", "Linked List", "Linked List", "Medium", ["Linked List", "Two Pointers"]),
    ("Odd Even Linked List", "Linked List", "Linked List", "Medium", ["Linked List"]),
    ("Partition List", "Linked List", "Linked List", "Medium", ["Linked List", "Two Pointers"]),
    ("Copy List with Random Pointer", "Linked List", "Linked List", "Medium", ["Hash Table", "Linked List"]),
    ("Flatten a Multilevel Doubly Linked List", "Linked List", "Linked List", "Medium", ["Linked List", "Depth-First Search", "Doubly-Linked List"]),
    ("LRU Cache", "Linked List", "Design", "Medium", ["Hash Table", "Linked List", "Design", "Doubly-Linked List"]),
    ("Design Linked List", "Linked List", "Design", "Medium", ["Design", "Linked List"]),
    ("Middle of the Linked List", "Linked List", "Two Pointers", "Easy", ["Linked List", "Two Pointers"]),
    ("Delete Node in a Linked List", "Linked List", "Linked List", "Medium", ["Linked List"]),
    ("Linked List Cycle II", "Linked List", "Two Pointers", "Medium", ["Linked List", "Two Pointers"]),
    ("Intersection of Two Linked Lists", "Linked List", "Two Pointers", "Easy", ["Hash Table", "Linked List", "Two Pointers"]),
    ("Remove Linked List Elements", "Linked List", "Linked List", "Easy", ["Linked List", "Recursion"]),
    ("Reverse Linked List II", "Linked List", "Linked List", "Medium", ["Linked List"]),
    ("Remove Duplicates from Sorted List", "Linked List", "Linked List", "Easy", ["Linked List"]),
    ("Remove Duplicates from Sorted List II", "Linked List", "Linked List", "Medium", ["Linked List", "Two Pointers"]),
    ("Reverse Nodes in k-Group", "Linked List", "Linked List", "Hard", ["Linked List", "Recursion"]),
    ("Sort List", "Linked List", "Linked List", "Medium", ["Linked List", "Two Pointers", "Divide and Conquer", "Sorting", "Merge Sort"]),
    ("Swap Nodes in Pairs", "Linked List", "Linked List", "Medium", ["Linked List", "Recursion"]),
    ("Remove Nth Node From End of List", "Linked List", "Two Pointers", "Medium", ["Linked List", "Two Pointers"]),
    ("Merge k Sorted Lists", "Linked List", "Heap", "Hard", ["Linked List", "Divide and Conquer", "Heap", "Merge Sort"]),

    # --- Intervals (14) ---
    ("Merge Intervals", "Intervals", "Intervals", "Medium", ["Array", "Sorting"]),
    ("Insert Interval", "Intervals", "Intervals", "Medium", ["Array"]),
    ("Non-overlapping Intervals", "Intervals", "Intervals", "Medium", ["Array", "Dynamic Programming", "Sorting", "Greedy"]),
    ("Minimum Number of Arrows to Burst Balloons", "Intervals", "Intervals", "Medium", ["Array", "Sorting", "Greedy"]),
    ("Meeting Rooms", "Intervals", "Intervals", "Easy", ["Array", "Sorting"]),
    ("Meeting Rooms II", "Intervals", "Intervals", "Medium", ["Array", "Sorting", "Heap", "Prefix Sum"]),
    ("Interval List Intersections", "Intervals", "Intervals", "Medium", ["Array", "Two Pointers", "Sorting"]),
    ("Employee Free Time", "Intervals", "Intervals", "Hard", ["Array", "Sorting", "Heap", "Queue"]),
    ("Remove Interval", "Intervals", "Intervals", "Medium", ["Array", "Sorting"]),
    ("My Calendar I", "Intervals", "Segment Tree", "Medium", ["Array", "Binary Search", "Design", "Segment Tree", "Ordered Set"]),
    ("My Calendar II", "Intervals", "Segment Tree", "Medium", ["Array", "Segment Tree", "Design"]),
    ("My Calendar III", "Intervals", "Segment Tree", "Hard", ["Array", "Segment Tree", "Ordered Set", "Design"]),
    ("Data Stream as Disjoint Intervals", "Intervals", "Intervals", "Hard", ["Binary Search", "Ordered Set", "Design"]),
    ("Minimum Number of Taps to Open to Water a Garden", "Intervals", "Greedy", "Hard", ["Array", "Dynamic Programming", "Greedy"]),

    # --- Matrix (18) ---
    ("Game of Life", "Matrix", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),
    ("Diagonal Traverse", "Matrix", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),
    ("Reshape the Matrix", "Matrix", "Matrix", "Easy", ["Array", "Matrix", "Simulation"]),
    ("Toeplitz Matrix", "Matrix", "Matrix", "Easy", ["Array", "Matrix"]),
    ("Search a 2D Matrix II", "Matrix", "Binary Search", "Medium", ["Array", "Binary Search", "Divide and Conquer", "Matrix"]),
    ("Spiral Matrix II", "Matrix", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),
    ("Kth Smallest Element in a Sorted Matrix", "Matrix", "Binary Search", "Medium", ["Array", "Binary Search", "Matrix", "Heap", "Divide and Conquer"]),
    ("Set Matrix Zeroes", "Matrix", "Matrix", "Medium", ["Array", "Hash Table", "Matrix"]),
    ("Rotate Image", "Matrix", "Matrix", "Medium", ["Array", "Matrix", "Math"]),
    ("Spiral Matrix", "Matrix", "Matrix", "Medium", ["Array", "Matrix", "Simulation"]),
    ("Valid Sudoku", "Matrix", "Hashing", "Medium", ["Array", "Hash Table", "Matrix"]),
    ("01 Matrix", "Matrix", "BFS", "Medium", ["Array", "Dynamic Programming", "Breadth-First Search", "Matrix"]),
    ("Rotting Oranges", "Matrix", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Shortest Path in Binary Matrix", "Matrix", "BFS", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Pacific Atlantic Water Flow", "Matrix", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Matrix"]),
    ("Surrounded Regions", "Matrix", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Max Area of Island", "Matrix", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Number of Islands", "Matrix", "DFS", "Medium", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),

    # --- Monotonic Stack (10) ---
    ("Daily Temperatures", "Monotonic Stack", "Monotonic Stack", "Medium", ["Array", "Stack", "Monotonic Stack"]),
    ("Next Greater Element I", "Monotonic Stack", "Monotonic Stack", "Easy", ["Array", "Hash Table", "Stack", "Monotonic Stack"]),
    ("Next Greater Element II", "Monotonic Stack", "Monotonic Stack", "Medium", ["Array", "Stack", "Monotonic Stack"]),
    ("Next Greater Element III", "Monotonic Stack", "Math", "Medium", ["Math", "Two Pointers", "String"]),
    ("Largest Rectangle in Histogram", "Monotonic Stack", "Monotonic Stack", "Hard", ["Array", "Stack", "Monotonic Stack"]),
    ("Trapping Rain Water", "Monotonic Stack", "Monotonic Stack", "Hard", ["Array", "Two Pointers", "Stack", "Dynamic Programming"]),
    ("Remove Duplicate Letters", "Monotonic Stack", "Monotonic Stack", "Medium", ["String", "Stack", "Monotonic Stack", "Greedy"]),
    ("Online Stock Span", "Monotonic Stack", "Monotonic Stack", "Medium", ["Stack", "Design", "Monotonic Stack", "Data Stream"]),
    ("Sum of Subarray Minimums", "Monotonic Stack", "Monotonic Stack", "Medium", ["Array", "Dynamic Programming", "Stack", "Monotonic Stack"]),
    ("Number of Visible People in a Queue", "Monotonic Stack", "Monotonic Stack", "Hard", ["Array", "Stack", "Monotonic Stack"]),

    # --- Union Find (12) ---
    ("Number of Connected Components in an Undirected Graph", "Union Find", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Graph Valid Tree", "Union Find", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Redundant Connection", "Union Find", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph"]),
    ("Longest Consecutive Sequence", "Union Find", "Union Find", "Medium", ["Array", "Hash Table", "Union Find"]),
    ("Accounts Merge", "Union Find", "Union Find", "Medium", ["Array", "String", "Depth-First Search", "Breadth-First Search", "Union Find"]),
    ("Making A Large Island", "Union Find", "Union Find", "Hard", ["Array", "Depth-First Search", "Breadth-First Search", "Union Find", "Matrix"]),
    ("Most Stones Removed with Same Row or Column", "Union Find", "Union Find", "Medium", ["Array", "Backtracking", "Bit Manipulation", "Dynamic Programming", "Graph", "Union Find"]),
    ("Optimal Account Balancing", "Union Find", "Union Find", "Hard", ["Array", "Backtracking", "Bit Manipulation", "Dynamic Programming", "Graph", "Union Find"]),
    ("Sentence Similarity II", "Union Find", "Union Find", "Medium", ["Depth-First Search", "Union Find", "Graph", "Hash Table"]),
    ("Satisfiability of Equality Equations", "Union Find", "Union Find", "Medium", ["Union Find", "Graph", "String"]),
    ("Longest Happy Prefix", "Union Find", "String", "Hard", ["String", "Rolling Hash", "String Matching", "Hash Function"]),
    ("Regions Cut By Slashes", "Union Find", "Union Find", "Medium", ["Depth-First Search", "Breadth-First Search", "Union Find", "Graph", "Matrix"]),

    # --- Topological Sort (12) ---
    ("Course Schedule", "Topological Sort", "Topological Sort", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"]),
    ("Course Schedule II", "Topological Sort", "Topological Sort", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph", "Topological Sort"]),
    ("Alien Dictionary", "Topological Sort", "Topological Sort", "Hard", ["Array", "String", "Topological Sort", "Graph"]),
    ("Sequence Reconstruction", "Topological Sort", "Topological Sort", "Medium", ["Graph", "Topological Sort"]),
    ("Course Schedule III", "Topological Sort", "Greedy", "Hard", ["Array", "Greedy", "Sorting", "Heap"]),
    ("Parallel Courses", "Topological Sort", "Topological Sort", "Medium", ["Graph", "Topological Sort"]),
    ("Parallel Courses II", "Topological Sort", "Topological Sort", "Hard", ["Dynamic Programming", "Graph", "Topological Sort", "Bit Manipulation"]),
    ("Minimum Height Trees", "Topological Sort", "BFS", "Medium", ["Graph", "Topological Sort", "Breadth-First Search"]),
    ("Sort Items by Groups Respecting Dependencies", "Topological Sort", "Topological Sort", "Hard", ["Graph", "Topological Sort"]),
    ("Find Eventual Safe States", "Topological Sort", "Topological Sort", "Medium", ["Depth-First Search", "Graph", "Topological Sort", "Array"]),
    ("Largest Color Value in a Directed Graph", "Topological Sort", "Topological Sort", "Hard", ["Hash Table", "Dynamic Programming", "Graph", "Topological Sort", "Counting"]),
    ("Orderly Queue", "Topological Sort", "Math", "Hard", ["Math", "String", "Sorting"]),

    # --- Shortest Path (12) ---
    ("Network Delay Time", "Shortest Path", "Shortest Path", "Medium", ["Heap", "Graph", "Shortest Path"]),
    ("Cheapest Flights Within K Stops", "Shortest Path", "Shortest Path", "Medium", ["Dynamic Programming", "Heap", "Graph", "Shortest Path"]),
    ("Word Ladder", "Shortest Path", "Shortest Path", "Hard", ["Hash Table", "String", "Breadth-First Search"]),
    ("Shortest Path in Binary Matrix", "Shortest Path", "Shortest Path", "Medium", ["Array", "Breadth-First Search", "Matrix"]),
    ("Path With Minimum Effort", "Shortest Path", "Shortest Path", "Medium", ["Array", "Binary Search", "Depth-First Search", "Breadth-First Search", "Union Find", "Heap", "Matrix"]),
    ("The Maze II", "Shortest Path", "Shortest Path", "Medium", ["Depth-First Search", "Breadth-First Search", "Graph", "Heap", "Shortest Path"]),
    ("Swim in Rising Water", "Shortest Path", "Shortest Path", "Hard", ["Array", "Binary Search", "Depth-First Search", "Breadth-First Search", "Union Find", "Heap", "Matrix"]),
    ("Shortest Path Visiting All Nodes", "Shortest Path", "Shortest Path", "Hard", ["Dynamic Programming", "Bit Manipulation", "Breadth-First Search", "Graph", "Bitmask"]),
    ("Find the City With the Smallest Number of Neighbors at a Threshold Distance", "Shortest Path", "Shortest Path", "Medium", ["Dynamic Programming", "Graph", "Shortest Path"]),
    ("Minimum Cost to Make at Least One Valid Path in a Grid", "Shortest Path", "Shortest Path", "Medium", ["Array", "Breadth-First Search", "Graph", "Heap", "Shortest Path"]),
    ("Second Minimum Time to Reach Destination", "Shortest Path", "Shortest Path", "Medium", ["Breadth-First Search", "Graph", "Dynamic Programming", "Shortest Path"]),
    ("Minimum Obstacle Removal at Corner", "Shortest Path", "Shortest Path", "Hard", ["Array", "Breadth-First Search", "Heap", "Graph", "Matrix", "Shortest Path"]),
]


def build_question_records() -> List[Dict[str, Any]]:
    seen_titles: Set[str] = set()
    records = []
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=730)
    for title, topic, pattern, difficulty, tags in QUESTIONS_RAW:
        if title in seen_titles:
            continue
        seen_titles.add(title)
        slug = slugify_title(title)
        records.append({
            "title": title,
            "platform": "LeetCode",
            "topic": topic,
            "pattern": pattern,
            "difficulty": difficulty,
            "tags": tags,
            "url": f"https://leetcode.com/problems/{slug}/",
            "created_at": start + datetime.timedelta(
                seconds=random.randint(0, int((now - start).total_seconds()))
            ),
        })
    return records


def generate_users(n: int) -> List[Dict[str, Any]]:
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=730)
    users = []
    used_emails: Set[str] = set()
    for i in range(n):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        base_email = f"{first.lower()}.{last.lower()}"
        email = f"{base_email}@{random.choice(EMAIL_DOMAINS)}"
        counter = 1
        while email in used_emails:
            email = f"{base_email}{counter}@{random.choice(EMAIL_DOMAINS)}"
            counter += 1
        used_emails.add(email)
        users.append({
            "name": f"{first} {last}",
            "email": email,
            "created_at": start + datetime.timedelta(
                seconds=random.randint(0, int((now - start).total_seconds()))
            ),
        })
    return users


def generate_solves(
    user_ids: List[int],
    question_ids: List[int],
    question_difficulty: Dict[int, str],
    n: int,
) -> List[Dict[str, Any]]:
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(days=700)

    user_solve_counts: Dict[int, int] = {}
    solves: List[Dict[str, Any]] = []

    for i in range(n):
        user_id = random.choices(
            user_ids,
            weights=[1.0 / (1 + user_solve_counts.get(uid, 0) * 0.01) for uid in user_ids],
            k=1,
        )[0]
        question_id = random.choice(question_ids)
        difficulty = question_difficulty[question_id]

        user_solve_counts[user_id] = user_solve_counts.get(user_id, 0) + 1
        total_solves = user_solve_counts[user_id]

        user_start = start + datetime.timedelta(days=random.randint(0, 600))
        solve_dt = user_start + datetime.timedelta(
            days=random.randint(0, min(total_solves * 2, 180)),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        if solve_dt > now:
            solve_dt = now - datetime.timedelta(minutes=random.randint(0, 1440))

        if difficulty == "Easy":
            time_taken = max(1, random.gauss(8, 4))
            wrong_attempts = random.choices([0, 0, 0, 1, 1, 2, 3], k=1)[0]
            hints_used = random.choices([0, 0, 0, 0, 1, 1], k=1)[0]
        elif difficulty == "Medium":
            time_taken = max(3, random.gauss(25, 12))
            wrong_attempts = random.choices([0, 1, 1, 2, 2, 3, 4, 5], k=1)[0]
            hints_used = random.choices([0, 0, 1, 1, 2, 2, 3], k=1)[0]
        else:
            time_taken = max(10, random.gauss(55, 25))
            wrong_attempts = random.choices([1, 2, 3, 3, 4, 5, 6, 8, 10], k=1)[0]
            hints_used = random.choices([0, 1, 2, 2, 3, 3, 4, 5], k=1)[0]

        time_taken = round(time_taken, 1)

        confidence_base = 0.4 + min(total_solves * 0.015, 0.4)
        if difficulty == "Easy":
            confidence_base += 0.1
        elif difficulty == "Hard":
            confidence_base -= 0.1
        confidence = min(1.0, max(0.05, confidence_base + random.gauss(0, 0.12)))
        confidence = round(confidence, 3)

        solves.append({
            "user_id": user_id,
            "question_id": question_id,
            "solved_at": solve_dt,
            "time_taken_minutes": time_taken,
            "wrong_attempts": wrong_attempts,
            "hints_used": hints_used,
            "confidence_score": confidence,
        })
    return solves


def generate_revisions(
    solves: List[Dict[str, Any]],
    question_difficulty: Dict[int, str],
    n: int,
) -> List[Dict[str, Any]]:
    if not solves:
        return []
    solves_sorted = sorted(solves, key=lambda s: s["solved_at"])
    now = datetime.datetime.utcnow()
    selected = random.sample(solves_sorted, min(n, len(solves_sorted)))
    revisions: List[Dict[str, Any]] = []
    for solve in selected:
        days_after = random.randint(1, 90)
        rev_dt = solve["solved_at"] + datetime.timedelta(days=days_after)
        if rev_dt > now:
            rev_dt = now - datetime.timedelta(minutes=random.randint(0, 1440))

        days_since_solve = (rev_dt - solve["solved_at"]).days
        base_quality = max(0.1, 0.9 - days_since_solve * 0.008)
        confidence = solve["confidence_score"]
        base_quality += (confidence - 0.5) * 0.2
        difficulty = question_difficulty.get(solve["question_id"], "Medium")
        if difficulty == "Hard":
            base_quality -= 0.08
        elif difficulty == "Easy":
            base_quality += 0.05
        quality = min(1.0, max(0.0, base_quality + random.gauss(0, 0.1)))
        quality = round(quality, 3)

        revisions.append({
            "user_id": solve["user_id"],
            "question_id": solve["question_id"],
            "revised_at": rev_dt,
            "revision_quality": quality,
        })
    return revisions


def generate_recommendations(
    user_ids: List[int],
    question_ids: List[int],
    question_difficulty: Dict[int, str],
    revision_map: Dict[Tuple[int, int], float],
    solve_confidence_map: Dict[Tuple[int, int], float],
    n: int,
) -> List[Dict[str, Any]]:
    now = datetime.datetime.utcnow()
    recommendations: List[Dict[str, Any]] = []
    attempts = 0
    max_attempts = n * 5

    while len(recommendations) < n and attempts < max_attempts:
        attempts += 1
        user_id = random.choice(user_ids)
        question_id = random.choice(question_ids)

        key = (user_id, question_id)

        rev_quality = revision_map.get(key, None)
        confidence = solve_confidence_map.get(key, None)
        difficulty = question_difficulty.get(question_id, "Medium")

        if rev_quality is not None:
            forget_prob = max(0.0, min(1.0, 1.0 - rev_quality + random.gauss(0, 0.08)))
            rec_score = max(0.0, min(1.0, rev_quality * 0.6 + random.gauss(0.3, 0.1)))
        elif confidence is not None:
            forget_prob = max(0.0, min(1.0, 1.0 - confidence * 0.8 + random.gauss(0, 0.1)))
            rec_score = max(0.0, min(1.0, (1.0 - confidence) * 0.7 + random.gauss(0.2, 0.1)))
        else:
            forget_prob = max(0.0, min(1.0, 0.5 + random.gauss(0, 0.15)))
            rec_score = max(0.0, min(1.0, 0.5 + random.gauss(0, 0.15)))

        if difficulty == "Hard":
            forget_prob = min(1.0, forget_prob + 0.08)
            rec_score = max(0.0, rec_score - 0.05)
        elif difficulty == "Easy":
            forget_prob = max(0.0, forget_prob - 0.05)
            rec_score = min(1.0, rec_score + 0.05)

        forget_prob = round(max(0.0, min(1.0, forget_prob)), 3)
        rec_score = round(max(0.0, min(1.0, rec_score)), 3)

        gen_dt = now - datetime.timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        recommendations.append({
            "user_id": user_id,
            "question_id": question_id,
            "recommendation_score": rec_score,
            "forget_probability": forget_prob,
            "generated_at": gen_dt,
        })
    return recommendations


def detect_tags_type(db) -> bool:
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.bind)
        columns = inspector.get_columns(Question.__tablename__)
        for col in columns:
            if col["name"] == "tags":
                col_type = str(col["type"]).upper()
                if "ARRAY" in col_type:
                    return True
                else:
                    return False
    except Exception:
        pass
    return False


def bulk_insert(session, model, records: List[Dict[str, Any]], batch_size: int = BATCH_SIZE):
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        session.bulk_insert_mappings(model, batch)
    session.commit()


def main():
    db = SessionLocal()
    try:
        is_array = detect_tags_type(db)

        print("Seeding users...")
        user_records = generate_users(200)
        bulk_insert(db, User, user_records)
        user_ids = [row[0] for row in db.query(User.id).all()]
        num_users = len(user_ids)
        del user_records
        db.expire_all()

        print("Seeding questions...")
        question_records = build_question_records()
        if not is_array:
            for rec in question_records:
                if isinstance(rec["tags"], list):
                    rec["tags"] = ", ".join(rec["tags"])
        bulk_insert(db, Question, question_records)
        question_rows = db.query(Question.id, Question.difficulty).all()
        question_ids = [row[0] for row in question_rows]
        question_difficulty = {row[0]: row[1] for row in question_rows}
        num_questions = len(question_ids)
        del question_records
        del question_rows
        db.expire_all()

        print("Seeding solves...")
        solve_records = generate_solves(user_ids, question_ids, question_difficulty, 12000)
        bulk_insert(db, Solve, solve_records)
        num_solves = len(solve_records)
        db.expire_all()

        print("Seeding revisions...")
        revision_records = generate_revisions(solve_records, question_difficulty, 7000)
        bulk_insert(db, Revision, revision_records)
        num_revisions = len(revision_records)

        print("Seeding recommendations...")
        revision_rows = db.query(
            Revision.user_id,
            Revision.question_id,
            Revision.revision_quality,
        ).all()
        revision_map: Dict[Tuple[int, int], float] = {
            (row[0], row[1]): row[2] for row in revision_rows
        }
        del revision_rows
        del revision_records

        solve_confidence_map: Dict[Tuple[int, int], float] = {
            (s["user_id"], s["question_id"]): s["confidence_score"]
            for s in solve_records
        }

        recommendation_records = generate_recommendations(
            user_ids, question_ids, question_difficulty, revision_map, solve_confidence_map, 7000
        )
        bulk_insert(db, Recommendation, recommendation_records)
        num_recommendations = len(recommendation_records)

        del solve_records
        del recommendation_records
        del solve_confidence_map
        del revision_map
        db.expire_all()

        print()
        print(f"Number of users inserted: {num_users}")
        print(f"Number of questions inserted: {num_questions}")
        print(f"Number of solves inserted: {num_solves}")
        print(f"Number of revisions inserted: {num_revisions}")
        print(f"Number of recommendations inserted: {num_recommendations}")
        print("Database seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"\n!!! ERROR during seeding: {e}")
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()