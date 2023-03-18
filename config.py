"""
Our configurations file, where we set up default values
as well as handy lists and dictionaries for efficiency.
"""

from ursina import Vec3, Vec4

six_cube_dirs = [   Vec3(0,1,0),
                    Vec3(0,-1,0),
                    Vec3(-1,0,0),
                    Vec3(1,0,0),
                    Vec3(0,0,-1),
                    Vec3(0,0,1)
                ]

minerals =  {   'grass' : (8,7),
                'soil' : (10,7),
                'stone' : (8,5),
                'emerald' : (9,6),
                'ice' : (9,7,Vec4(0,0.4,0.5,0.8)),
                'snow' : (8,6),
                'ruby' : (9,6,Vec4(1,0,0,1)),
                'water_': (9,6,Vec4(0,0.8,0.8,0.8)),
                'water': (10,7),
                'wood': (11,7),
                'foliage': (11,6),
                'obsidian': (9,5),
                'netherrack': (10,6),
                'lava': (10,5),
                'gold': (11,5),
                'crafting_table':(8,4),
                'oak_planks':(9,4),
                'sand':(10,4),
                'bed':(11,4),
                'grassflower':(8,3),
                'wool':(9,3)
            }
# Create iterable list from dictionary keys (not values).
mins = list(minerals.keys())