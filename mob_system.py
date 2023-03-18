from ursina import *
from mining_system import *
from mesh_terrain import*
text='                                                                                                                                                  '
i=0
creepy=True
ctplayer=False
tex=Text(background=True,y=-0.45,x=-0.49,text=text)
def ip1():
    global i,creepy
    text = "Ouch! That hurts! Are you completely stupid?!"
    tex.text = text
    i+=1
    if i==3:
        grey.collider=None
        grey.color=color.clear
        creepy=False
        Audio("someoneReallyCompletelyStupid.mp3")
grey = FrameAnimation3d('source\creeperaaa_',fps=2,scale=0.1,collider="mesh",)
grey.color=color.white
def creepingp():
    grey.color=color.gray if grey.color==color.white else color.white
def ctpl():
    global ctplayer
    ctplayer=True
def ctf():
    global ctplayer
    ctplayer=False
# ***
grey.texture='textures\creeper'
grey.position = Vec3(0,-20,10)
grey.turnSpeed = 2
grey.speed = 12
def mob_movement(mob, subPos, _td,terrain,subjectUiPos):
    if creepy==True:
            # First, turn towards target...
            # BUG wiggle walk when aligned with subject?
            tempOR = mob.rotation_y
            mob.lookAt(subPos)
            mob.rotation = Vec3(0, mob.rotation.y + 180, 0)
            mob.rotation_y = lerp(tempOR, mob.rotation_y, mob.turnSpeed * time.dt)

            # Now move mob towards target...
            # How close can they approach?
            intimacyDist = 3
            # How far away from target?
            dist = subPos - mob.position
            # Magnitude of distance from target examined...
            if dist.length() > intimacyDist:
                # Approach target...
                mob.position -= mob.forward * mob.speed * time.dt
                mob.resume()  # Animation.
                mob.is_playing = True
            else:
                mob.pause()  # Animation.
                mob.is_playing = False
            terrain_walk(mob,subPos,_td,terrain,subjectUiPos)
creepingP=False
already_dead=False
creepedcounter=0
def terrain_walk(mob, subPos, _td,terrain,subjectUiPos):
    global text,creepedcounter,already_dead,creepingcounter,tex,creepingP
    #mob.y+=1.5
    # Check mob hasn't fallen off the planet ;)
    position_before=mob.position
    if mob.y < -100:
        mob.y = 100

    blockFound=False
    step = 4
    height = 1
    x = floor(mob.x+0.5)
    z = floor(mob.z+0.5)
    y = floor(mob.y+0.5)
    for i in range(-step,step):
        whatT1=_td.get((x,y+i,z))
        if whatT1!=None and whatT1!='g':
            whatT2=_td.get((x,y+i+1,z))
            if whatT2!=None and whatT2!='g':
                target = y+i+height+1
                blockFound=True
                break
            target = y+i+height
            blockFound=True
            break
    if blockFound==True:
        yBefore=mob.y
        def beee():
            try:
                if build[f"{round(mob.x)},{round(mob.z)}"] == "e" or build[f"{round(mob.x)-1},{round(mob.z)}"] == "e" or build[f"{round(mob.x)},{round(mob.z)-1}"] == "e"or build[f"{round(mob.x)-1},{round(mob.z)-1}"] == "e"or build[f"{round(mob.x)+1},{round(mob.z)}"] == "e"or build[f"{round(mob.x)},{round(mob.z)+1}"] == "e"or build[f"{round(mob.x)+1},{round(mob.z)+1}"] == "e":
                    return True
                else:
                    return False
            except:
                return False
        yNow = mob.y = lerp(mob.y, target, 6 * time.dt) if not abs(lerp(mob.y, target, 6 * time.dt)-mob.y)>6 and not beee() else position_before
    else:
        # Gravity fall :<
        mob.y -= 9.8 * time.dt
    if distance(subPos,mob.position)<5 and already_dead==False:
        creepingp()
        creepingP=True
        creepedcounter+=0.1
        if creepedcounter>=5:# and already_dead==False:
            grey.color=color.clear
            grey.collider=None
            tex.text = f"You died! Creeper killed you on camera coordinates: {subjectUiPos}."
            w1=Entity(position=grey.position)
            e1=creeper_explosion(td=_td,vd=terrain.vd,subsets=terrain.subsets,_texture=terrain.textureAtlas,_sub=grey)
            e2 = creeper_explosion(td=_td, vd=terrain.vd, subsets=terrain.subsets, _texture=terrain.textureAtlas,
                                  _sub=w1)
            if (e1 != None and e1[2]!='wood' and
                e1[2]!='foliage' and e1[2]!='oak_planks' and e1[2]!='obsidian' and e1[2]!='netherrack' and e1[2]!='obsidian' and e1[2]!='gold'):
                terrain.genWalls(e1[0],e1[1])
                terrain.subsets[e1[1]].model.generate()
            if (e2 != None and e2[2]!='wood' and
                e2[2]!='foliage' and e2[2]!='oak_planks' and e2[2]!='obsidian' and e2[2]!='netherrack' and e2[2]!='obsidian' and e2[2]!='gold'):
                terrain.genWalls(e2[0],e2[1])
                terrain.subsets[e2[1]].model.generate()
            already_dead=True
#creepyCreeper = Entity(model="assets/minecraft-creeper/source/creeper",
#                       texture="assets/minecraft-creeper/textures/creeper", scale=0.1)

def creeper(mob):
    #creepyCreeper.x=mob.x
    #creepyCreeper.z=mob.z
    #creepyCreeper.y=mob.y+2.5
    return None