from ursina import *
# Instantiate ursina here, so that textures can be
# loaded without issue in other modules :)
app = Ursina()

from ursina.prefabs.first_person_controller import FirstPersonController
from mesh_terrain import MeshTerrain
from flake import SnowFall
import random as ra
from bump_system import *
from save_load_system import saveMap, loadMap
from inventory_system import *
import mining_system as MS
"""
NB - RED workspace is private PREP.
NB - BLUE is TUTORIAL code!
Adventures
1) 'Snap' behaviour for items. DONE :D
2) Number keys select building block type. DONE :)
3) Make an inventory panel.

Notes for vid 16
i) Correcting colour - DONE (except for stain bug - see vi)
ii) Saving blockType correctly - DONE
ii+) from 't' to not None and not 'g' (in bump_system, building, etc.) - DONE
ii+) record blockType in td only at end of genBlock() - DONE
iii) Map-name const at start of save_load_system - DONE
iv) fixPos() at instantiation of hotspots - DONE!

Tut 17 notes
i) inventory panel creation; toggle behaviour, static method - DONE
ii) Investigate colour staining bug - DONE
ii+) Solve colour staining - DONE :D
ii) ? - Earthquakes :o - DONE :D

Tut 18 notes
i) mined block particles - pick-up for inventory - DONE
ii) trees? Rocks?! (VID 20?)
iii) Note on ursina update and fix! 4.1.1 - DONE

Tut 19 adventure plans!
0) eye-level correction - DONE
0.1) more efficient highlight call - DONE
0.2) empty-subject hands, then no build - DONE
i) colour bug for e.g. ruby collectible - DONE - UNDONE?!
ii) picking up behaviour  - DONE
iii) sounds for picking up item - DONE
iv) text for stacking info on inventory DONE
iv+) stacking behaviour on inventory DONE
v) destroy collectibles if lifespan expires - DONE

Tut 20
i) ui aspect ratio bug DONE
ii) collectible colour bug DONE
iii) inventory items stay put when clicked DONE
iv) saw a panda -- DONE
v) created simple stack system DONE 

Tut 21
i) BUG item text remaining when it shouldn't - DONE
i.i) BUG items of different kinds overlapping... DONE
i.ii) Item stack text update upon collection. - DONE
iii) TREES :) - DONE

Tut 22
i) deplete stack number when building :) - DONE

Tut 23 * TREE SPECIAL *
0.i) refactor rara (random module clash) - DONE
ii) Trees minable - DONE
ii.i) Tree texture(s) - DONE -> grass transparency :) 'BUG'
ii.ii) Tree perlin distribution - DONE
iii) FOV to 63 - DONE (corrected for dash effect)
iv) location co-ords as Text on screen DONE 

Tut 24
i) audio - pickups as member property
ii) Rocks -> replace random stone placements
iii) tree placement wiggle
iv) prevent tree crown clash

**To Do List**
) audio as member property of collectible class
) Refactor the current-blockType (building) mechanism.
) Write an 'empty' function to empty a hotspot.
) Giant rocky outcrops?!
) Text background (e.g. for location text)
) Ui hotspot spacing (refactor)
) Bump system - sticking to trees, and climbing them...
) minimap?
) BUG glitching through terrain bc trees
"""
window.color = color.azure#color.rgb(0,200,225)
# indra = Sky()
# indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
subject.height=1.62 # Minecraft eye-level?
subject.camera_pivot.y=subject.height
subject.frog=False # For jumping...
subject.runSpeed=12
subject.walkSpeed=4
subject.blockType=None # Current building mineral.
camera.dash=10 # Rate at which fov changes when running.
camera.fov=origFOV=63
#seaMask=Entity(model="quad",scale=8,parent=camera.ui)
# *** - see inventory_system.py
# window.fullscreen=False
entityColors={}
terrain = MeshTerrain(subject,camera)
snowfall = SnowFall(subject)
# How do you at atmospheric fog?
# scene.fog_color=indra.color
generatingTerrain=True
villy=FrameAnimation3d("villy_",fps=1,texture="assets/minecraft-villager/villy")
villy.add_script(SmoothFollow(subject,offset=(0,0,1.5),speed=0.1))
sheepy=FrameAnimation3d("sheep_",fps=1,x=100,z=200,texture="assets/minecraft-sheep/sheep")
sheepy.add_script(SmoothFollow(subject,offset=(0,0,5),speed=0.1))
# Generate our terrain 'chunks'.
for i in range(4):
    terrain.genTerrain()
# For loading in a large terrain at start.
# loadMap(subject,terrain)
grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)

pX = subject.x
pZ = subject.z
DIST=10
zombiecounterI=0
DROWNEDcounterI=0
def input(key):
    global generatingTerrain,already_drowned,already_dead,DIST,zombiecounterI,DROWNEDcounterI
    terrain.input(key)
    if key=='g':
        generatingTerrain = not generatingTerrain

    if key=='space': subject.frog=True
    if key=='m': saveMap(subject.position,terrain.td)
    if key=='l': loadMap(subject,terrain)
    #if key=='z':subject.position=zombie.position
    if key=='b':
        arrow=Entity(model="cube",scale=(0.2,1,0),texture="bow_arrow2.png",rotation_x=-90,rotation_y=45)
        arrow.position = subject.forward * DIST
        arrow.position+=(subject.x,0,subject.z)
        arrow.y=round(terrain.perlin.getHeight(arrow.x,arrow.z))+1.5
        if distance_xz(grey,arrow)<=1 and abs(grey.y-arrow.y)<=3.5:
            ip1()
        if already_dead==False:
            if distance_xz(zombie,arrow)<=2 and abs(zombie.y-arrow.y)<=3.5:
                tex.text="Fuck you, you nasty wixya!"
                zombiecounterI+=1
            if zombiecounterI>=3:
                zombie.y=7000
            already_dead=True
        if already_drowned == False:
                if distance_xz(drowned, arrow) <= 2 and abs(drowned.y - arrow.y) <= 3.5:
                    tex.text = "Fuck you, you nasty wixya!!"
                    DROWNEDcounterI += 1
                if DROWNEDcounterI >= 3:
                    drowned.y = 7000
                already_drowned=True
        if (distance_xz(sheepy, arrow) <= 2 and abs(sheepy.y - arrow.y) <= 3.5):
            Collectible("wool",(bte.position[0],bte.position[1]+1,bte.position[2]),"texture_atlas_3.png",subject)
            sheepy.x=100
            sheepy.z=200
            #Audio("someoneReallyCompletelyStupid.mp3")
    if key=="k hold":
        subject.y+=2
    if key=="y hold":
        subject.y-=2
    if key=="z":
        subject.y=terrain.perlin.getHeight(subject.x,subject.z)+5
    if key=="n":
        sheepy.x = 100
        sheepy.z = 200
        subject.x=sheepy.x
        subject.z=sheepy.z
        Collectible("wool", (bte.position[0], bte.position[1] + 1, bte.position[2]), "texture_atlas_3.png", subject)
    inv_input(key,subject,mouse)

count=0
earthcounter=0
earthquake_ON=False
already_closed=True
def update():
        global count, pX, pZ, already_closed, seaMask, earthcounter, creepy, origFOV,generatingTerrain  # ,DIST
        # Highlight terrain block for mining/building...
        terrain.update()
        # Handle mob ai.
        mob_movement(grey, subject.position, terrain.td,terrain,subjectUiPos=subject.camera_pivot.position)
        mob_movement_panda(greyPanda,subject.position,terrain.td)
        ZOMBIE(subject,terrain.perlin)
        DROWNED(subject,terrain.perlin)
        # creeper(grey)
        count += 1
        if count >= 1:

            count = 1
            # Generate terrain at current swirl position.
            if generatingTerrain:
                terrain.genTerrain()
                # for i in range(1):
                # terrain.genTerrain()
        # Change subset position based on subject position.
        if abs(subject.x - pX) > 1 or abs(subject.z - pZ) > 1:
            pX = subject.x
            pZ = subject.z
            terrain.swirlEngine.reset(pX, pZ)
            # Sound :)
            if subject.y > 4:
                if snow_audio.playing == False:
                    snow_audio.pitch = ra.random() + 0.25
                    snow_audio.play()
            elif grass_audio.playing == False:
                grass_audio.pitch = ra.random() + 0.7
                grass_audio.play()
            if floor(subject.y)<=-21:
                if grass_audio.playing==True:
                    grass_audio.stop()


        # *******
        #  Earthquake experiment!
        if earthquake_ON:
            earth_amp = 0.1
            earth_freq = 0.5
            earthcounter += earth_freq
            for h in terrain.subsets:
                h.y = (math.sin(terrain.subsets.index(h) +
                                earthcounter) * earth_amp)  # *time.dt
        # *******

        # Walk on solid terrain, and check wall collisions.
        bumpWall(subject,terrain)
        # Running and dash effect.
        if held_keys['shift'] and held_keys['w']:
            subject.speed = subject.runSpeed
            if camera.fov < 100:
                camera.fov += camera.dash * time.dt
        else:
            subject.speed = subject.walkSpeed
            if camera.fov > origFOV:
                camera.fov -= camera.dash * 4 * time.dt
                if camera.fov < origFOV: camera.fov = origFOV

        if terrain.perlin.getHeight(round(subject.x),round(subject.z))<=-22 and floor(subject.y)<=-21: #and not boat.visible:# and (round(boat.x),floor(boat.y),round(boat.z))!=(round(boat.x),round(boat.y),round(boat.z)):
            if subject.camera_pivot.y>0.2:
                subject.camera_pivot.y-=0.1
            tex.text="Achievement made: In the sea!"
            seaMask.color=Color(0, 0.501960784, 1, 0.66)
            generatingTerrain=True
        #if terrain.perlin.getHeight(round(subject.x), round(subject.z)) <= -22 and floor(subject.y) <= -21 and boat.visible:
        #    subject.camera_pivot.y=-subject.y-21+subject.height


        else:
            seaMask.color=color.clear
            subject.camera_pivot.y=subject.height
        villy.y=terrain.perlin.getHeight(villy.x,villy.z)+0.74
        sheepy.y = terrain.perlin.getHeight(sheepy.x, sheepy.z) + 0.74
from mob_system import *
from panda_system import *
from drunken_system import *
from drowned_system import *
app.run()
