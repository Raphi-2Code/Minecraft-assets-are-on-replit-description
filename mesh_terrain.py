from perlin import Perlin
from ursina import *
# from random import random as rara
# random module comes with inventory_system as ra
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import *
from config import six_cube_dirs, minerals, mins
from tree_system import *
from inventory_system import *
build={}
ruinportals=[]
bl=[]
beds=[]
BOATED=False
experimental=True
seaMask=Entity(model="quad",scale=8,parent=camera.ui)
def mountdismount():
    global BOATED
    BOATED=True
boat=Entity(model="assets/minecraft-boat/source/boat.obj",color=color.white,texture="assets/minecraft-boat/textures/oak.png",collider=None,on_click=mountdismount)
boat.visible=False
BE=False
BEDDY=False
has_boat=0
bXXX=False
def craftAndClose():
    global BE,has_boat
    BOAT.enabled=False
    BOAT.visible=False
    Close.enabled=False
    Close.visible=False
    ee.enabled=False
    ee.visible=False
    boat.visible=True
    boat.collider="box"
    boat.position=Vec3(eval("("+wai.text.lstrip("Position: ")+")"))
    BE=True
    has_boat+=1
BOAT=Button(text="Boat",scale=0.1,y=0.2,on_click=craftAndClose)
BOAT.visible=False
def bedAndClose():
    global BEDDY
    BED.visible=False
    BED.enabled=False
    BOAT.enabled=False
    BOAT.visible=False
    Close.enabled=False
    Close.visible=False
    ee.enabled=False
    ee.visible=False
    BEDDY=True
BED=Button(text="Bed",scale=0.1,y=0.4,on_click=bedAndClose)
BED.visible=False
def Close():
    global BE
    BOAT.enabled=False
    BOAT.visible=False
    BED.enabled=False
    BED.visible=False
    Close.enabled=False
    Close.visible=False
    ee.enabled=False
    ee.visible=False

Close=Button(text="Close",scale=0.1,y=0.3,on_click=Close)
Close.visible=False
def vle():
    BOAT.enabled=True
    BOAT.visible=True
    BED.enabled=True
    BED.visible=True
    Close.enabled=True
    Close.visible=True
    ee.enabled=False
    ee.visible=False
ee=Button(text="Craft",scale=0.1,y=0.2,on_click=vle)
ee.enabled=False
ee.visible=False
def openMenu():
    ee.enabled=True
    ee.visible=True
    BOAT.enabled=False
    BOAT.visible=False
    BED.enabled=False
    BED.visible=False
    Close.enabled=False
    Close.visible=False
craftingTables=[]
class MeshTerrain:
    def __init__(this,_sub,_cam):
        
        this.subject = _sub
        this.camera = _cam
        # *** - for ursina update fix
        this.block = load_model('block.obj',use_deepcopy=True)
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)

        this.subsets = []
        this.numSubsets = 1024
        
        # Must be even number! See genTerrain()
        this.subWidth = 6 
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.currentSubset = 0

        # Our terrain dictionary :D
        this.td = {}

        # Our vertex dictionary -- for mining.
        this.vd = {}

        this.perlin = Perlin()

        # Instantiate our subset Entities.
        this.setup_subsets()

    def plantTree(this,_x,_y,_z):
        global bl
        if not _y<=-18 and (not f"{round(_x)},{round(_z)}" in ruinportals):
            ent=TreeSystem.genTree(_x,_z)
            if ent==0: return
            # TrunkyWunky.
            treeH=int(3*ent)
            for i in range(treeH):
                if not f"{_x},{_y+i},{_z}" in bl:
                    this.genBlock(_x,_y+i,_z,
                        blockType='wood',layingTerrain=False)
                    bl.append(f"{_x},{_y+i},{_z}")
            # Crown.
            for t in range(-2,3):
                for tt in range(4):
                    for ttt in range(-2,3):
                        if not f"{_x+t},{_y+treeH+tt-1},{_z+ttt}" in bl:
                            this.genBlock(_x+t,_y+treeH+tt-1,_z+ttt,
                            blockType='foliage')
                            bl.append(f"{_x+t},{_y+treeH+tt-1},{_z+ttt}")

    def setup_subsets(this):
        for i in range(0,this.numSubsets):
            e = Entity( model=Mesh(),
                        texture=this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)

    def do_mining(this):
        # Pass in block and textureAtlas for dropping
        # collectible. See mining_system mine().
            epi = mine( this.td,this.vd,this.subsets,
                        this.textureAtlas,this.subject,this.perlin)
            if (epi != None and epi[2]!='wood' and
                epi[2]!='foliage' and epi[2]!='oak_planks' and epi[2]!='obsidian' and epi[2]!='netherrack' and epi[2]!='obsidian' and epi[2]!='gold'):
                this.genWalls(epi[0],epi[1])
                this.subsets[epi[1]].model.generate()
            if epi=="crafting_table":
                craftingTables.remove(f"{epi[0][0]},{epi[0][1]},{epi[0][2]}")

    # Highlight looked-at block :)
    def update(this):
        highlight(  this.subject.position,
                    this.subject.height,
                    this.camera,this.td)
        # Blister-mining!
        if bte.visible==True and mouse.locked==True:
            if held_keys['shift'] and held_keys['left mouse']:
                this.do_mining()
            # for key, value in held_keys.items():
            #     if key=='left mouse' and value==1:
            #         this.do_mining()

    def input(this,key):
        global build
        if key=='left mouse up' and bte.visible==True and mouse.locked==True and f"{bte.x},{bte.y},{bte.z}" not in craftingTables:
            this.do_mining()
            try:beds.remove(f"{bte.x},{bte.y},{bte.z}")
            except:pass
        # Building :)
        # First, return and don't build if empty handed.
        if this.subject.blockType is None: return
        if key=='right mouse up' and bte.visible==True and mouse.locked==True:
            bsite = checkBuild( bte.position,this.td,
                                this.camera.forward,
                                this.subject.position+Vec3(0,this.subject.height,0))
            #GG
            if bsite!=None: #and not (f"{bsite.x},{bsite.y-1},{bsite.z}" in craftingTables):
                build[f"{bsite.x},{bsite.z}"]="e"
                this.genBlock(floor(bsite.x),floor(bsite.y),floor(bsite.z),subset=0,blockType=this.subject.blockType)
                if this.subject.blockType == "crafting_table":
                    craftingTables.append(f"{bte.x},{bte.y},{bte.z}")
                    print("APPENDING!")
                if this.subject.blockType=="bed":
                    beds.append(f"{bte.x},{bte.y},{bte.z}")
                gapShell(this.td,bsite)
                this.subsets[0].model.generate()
                # *** Deplete a block from the stack ;)
                for h in hotspots:
                    # Is this hotspot highlighted?
                    if h.color==color.black:
                        # Decrease stack number by 1.
                        h.stack -= 1
                        if h.stack > 0:
                            h.item.update_stack_text()
                            break
                        # If we use up all blocks,
                        # empty out this hotspot.
                        elif h.stack <= 0:
                            if h.stack < 0:
                                h.stack=0
                            h.occupied=False
                            destroy(h.item)
                            h.t.text=""
                            # No blocks to build with!
                            this.subject.blockType=None
            if f"{bte.x},{bte.y},{bte.z}" in craftingTables:
                inv_input("e",this.subject,mouse)
                openMenu()
                bsite=None
    
    # I.e. after mining, to create illusion of depth.
    def genWalls(this,epi,subset):
        
        if epi==None: return
        # Refactor this -- place in mining_system 
        # except for cal to genBlock?
        
        for i in range(0,6):
            np = epi + six_cube_dirs[i]
            if this.td.get( (floor(np.x),
                            floor(np.y),
                            floor(np.z)))==None:
                if not (floor(np.x),floor(np.y),floor(np.z))==(floor(np.x),floor(this.perlin.getHeight(floor(np.x),floor(np.z))-1),floor(np.z)):
                    this.genBlock(floor(np.x),floor(np.y),floor(np.z),subset,gap=False,blockType='stone')
                else:
                    this.genBlock(floor(np.x), floor(np.y), floor(np.z), subset, gap=False, blockType='soil')

    def genBlock(this,x,y,z,subset=-1,gap=True,blockType='grass',layingTerrain=False):
        global bl
        if subset==-1: subset=this.currentSubset
        # Extend or add to the vertices of our model.
        model = this.subsets[subset].model

        model.vertices.extend([ Vec3(x,y,z) + v for v in 
                                this.block.vertices])

        if layingTerrain:
            if round(x+z)**2==round(sqrt(abs(y-z-x))) and z%4==0:
                exec(open("villagerSystem.txt","r").read())
            if ra.random() > 0.86:
                blockType='grassflower'
                if ra.random()>0.999 and not f"{x},{y},{z}" in bl:
                    blockType='obsidian'
                    ruinportals.append(f"{x},{z}")
                    this.genBlock(x,y+1,z,subset=-1,gap=True,blockType='netherrack',layingTerrain=False)
                    this.genBlock(x+1, round(this.perlin.getHeight(x+1,z))+1, z, subset=-1, gap=True, blockType='netherrack', layingTerrain=False)
                    this.genBlock(x+1, round(this.perlin.getHeight(x+1,z+1))+1, z+1, subset=-1, gap=True, blockType='netherrack', layingTerrain=False)
                    this.genBlock(x + 2, round(this.perlin.getHeight(x + 2, z + 1)) + 1, z + 1, subset=-1, gap=True,
                                  blockType='netherrack', layingTerrain=False)
                    this.genBlock(x, y + 2, z+1, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 2, z + 2, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 2, z, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 3, z+3, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 4, z + 3, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 5, z + 2, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 5, z + 1, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 3, z, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 4, z, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y + 6, z + 3, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y+5, z, subset=-1, gap=True,
                                  blockType='obsidian', layingTerrain=False)
                    this.genBlock(x, y+6, z, subset=-1, gap=True,
                                  blockType='gold', layingTerrain=False)
                    #this.genBlock(x, y + 6, z + 9, subset=-1, gap=True,
                    #              blockType='lava', layingTerrain=False)

            if y<=-19:
                blockType='sand'
            if y<=-23:
                blockType='water'
                Entity(model="plane",position=(x,-21,z),texture="water",color=Color(0, 0.501960784, 1, 0.66),collider=None)
            # If high enough, cap with snow blocks :D
            if y > 2:
                blockType='snow' if ra.random()<0.86 else 'ice'

        # Does the dictionary entry for this blockType
        # hold colour information? If so, use it :)
        if len(minerals[blockType])>2:
            # Decide random tint for colour of block :)
            c = 0
            # Grab the Vec4 colour data :)
            ce=minerals[blockType][2]
            # Adjust each colour channel separately to
            # ensure that hard-coded RGB combination is maintained.
            #if blockType!="water":
            model.colors.extend(    (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)*
                                    this.numVertices)
            #else:
            #    model.colors.extend((Vec4(ce[0] - c,  5, 5 , ce[3]),) *
            #                        this.numVertices)
        else:
            # Decide random tint for colour of block :)
            c = 0
            model.colors.extend(    (Vec4(1-c,1-c,1-c,1),)*
                                    this.numVertices)

        # This is the texture atlas co-ord for grass :)
        uu=minerals[blockType][0]
        uv=minerals[blockType][1]

        model.uvs.extend([Vec2(uu,uv) + u for u in this.block.uvs])

        # Record terrain in dictionary :)
        this.td[(floor(x),floor(y),floor(z))] = blockType
        # Also, record gap above this position to
        # correct for spawning walls after mining.
        if gap==True:
            key=((floor(x),floor(y+1),floor(z)))
            if this.td.get(key)==None:
                this.td[key]='g'

        # Record subset index and first vertex of this block.
        vob = (subset, len(model.vertices)-this.numVertices-1)
        this.vd[(floor(x),
                floor(y),
                floor(z))] = vob

    def genTerrain(this):
        global BOATED,BE,BEDDY,has_boat,bXXX,BED
        #hier weitermachen
        if BEDDY==True:
                BEDDY = False
                for hhhhh in range(len(hotspots)):
                        try:
                            if hotspots[hhhhh].item.blockType == "oak_planks":
                                print("Flow!")
                                hotspots[hhhhh].stack = floor(int(hotspots[hhhhh].stack) / 3)
                                hotspots[hhhhh].t.text = hotspots[hhhhh].stack
                                hotspots[hhhhh].item.update_stack_text()
                                bXXX=True

                                if hotspots[hhhhh].stack < 0:
                                    hotspots[hhhhh].stack = ceil(int(hotspots[hhhhh].stack) * 3)
                                    hotspots[hhhhh].t.text = hotspots[hhhhh].stack
                                    hotspots[hhhhh].item.update_stack_text()
                                    bXXX=False
                                for ghg in range(len(hotspots)):
                                    try:
                                        if hotspots[ghg].item.blockType == "wool" and bXXX==True:
                                            print("edde")
                                            hotspots[ghg].stack = floor(int(hotspots[ghg].stack) / 3)
                                            hotspots[ghg].t.text = hotspots[ghg].stack
                                            hotspots[ghg].item.update_stack_text()

                                            if hotspots[ghg].stack < 0:
                                                hotspots[ghg].stack = floor(int(hotspots[ghg].stack) * 3)
                                                hotspots[ghg].t.text = hotspots[ghg].stack
                                                hotspots[ghg].item.update_stack_text()
                                            else:
                                                Collectible("bed", (bte.position[0], bte.position[1] + 1, bte.position[2]), "texture_atlas_3.png", this.subject)
                                    except:pass
                        except:
                            pass
                else:
                    BED.visible=False
        #hier hört auf
        if BE==True and has_boat<2:
            BE=False
            if this.subject.blockType=="oak_planks":
                boat.visible=True
                for hhhh in range(len(hotspots)):
                    try:
                        if hotspots[hhhh].item.blockType=="oak_planks":
                            hotspots[hhhh].stack = int(hotspots[hhhh].stack)-5
                            hotspots[hhhh].t.text = hotspots[hhhh].stack
                            hotspots[hhhh].item.update_stack_text()

                            if hotspots[hhhh].stack < 0:
                                hotspots[hhhh].stack = int(hotspots[hhhh].stack) + 5
                                hotspots[hhhh].t.text = hotspots[hhhh].stack
                                hotspots[hhhh].item.update_stack_text()
                                boat.visible = False
                                has_boat = False
                                BE=True
                    except:pass
            else:boat.visible=False
        if has_boat>2:
            print("Teleporting boat to you...")
        if BOATED==True:
            boat.position=this.subject.position
            if this.perlin.getHeight(round(this.subject.x),round(this.subject.z))<=-22 and floor(this.subject.y)<=-21:
                seaMask.disable()
                this.subject.camera_pivot.y = - this.subject.y - 21 + this.subject.height
                this.subject.y = this.subject.y+this.subject.camera_pivot.y-this.subject.height
        else:
            if this.perlin.getHeight(round(this.subject.x), round(this.subject.z)) <= -22 and floor(
                    this.subject.y) <= -21:
                seaMask.enable()
        if held_keys["f"]:
            BOATED=False
        for ixixix in range(len(beds)):
            if distance(this.subject,eval("Vec3("+str(ixixix)+")")) and this.subject.enabled:
                if held_keys["p"]:
                    print("Sleeping!")
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)

        d = int(this.subWidth*0.5)

        for k in range(-d,d):
            for j in range(-d,d):

                y = floor(this.perlin.getHeight(x+k,z+j))
                if this.td.get( (floor(x+k),
                                floor(y),
                                floor(z+j)))==None:
                    this.genBlock(x+k,y,z+j,blockType='grass',layingTerrain=True)
                    # Plant a tree?
                    this.plantTree(x+k,y+1,z+j)

        this.subsets[this.currentSubset].model.generate()
        # Current subset hack ;)
        if this.currentSubset<this.numSubsets-1:
            this.currentSubset+=1
        else: this.currentSubset=0
        this.swirlEngine.move()
        if experimental==True:
            this.genCave(x=x,y=y,z=z)
    def genCave(this,x,y,z):
        if x - y + z == x + y - z:
            for xE in range(int(x)-10,int(x)):
                for yE in range(int(y)-10,int(y)):
                    for zE in range(int(y)-10,int(y)):
                            epili = Cave(td=this.td, vd=this.vd, subsets=this.subsets, _texture=this.textureAtlas,
                                                  _sub=Entity(position=(xE,yE,zE)))
                            if (epili != None and epili[2]!='wood' and
                                epili[2]!='foliage' and epili[2]!='oak_planks' and epili[2]!='obsidian' and epili[2]!='netherrack' and epili[2]!='obsidian' and epili[2]!='gold'):
                                this.genWalls(epili[0],epili[1])
                                this.subsets[epili[1]].model.generate()