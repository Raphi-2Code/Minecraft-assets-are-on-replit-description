from ursina import *

greyPanda = FrameAnimation3d('panda_walk_',fps=1)
greyPanda.texture='panda_texture'
greyPanda.position = Vec3(0,100,10)
greyPanda.turnSpeed = 1
greyPanda.speed = 0.1

def mob_movement_panda(mob, subPos, _td):
    if mob.y<=-26:
        mob.y=100
        mob.x=subPos[0]+2
        mob.z=subPos[2]+2
    # First, turn towards target...
    # BUG wiggle walk when aligned with subject?
    tempOR = mob.rotation_y
    mob.lookAt(subPos)
    mob.rotation = Vec3(0,mob.rotation.y+180,0)
    mob.rotation_y = lerp(tempOR,mob.rotation_y,mob.turnSpeed*time.dt)

    # Now move mob towards target...
    # How close can they approach?
    intimacyDist = 3
    # How far away from target?
    dist = subPos-mob.position
    # Magnitude of distance from target examined...
    if dist.length() > intimacyDist:
        # Approach target...
        mob.position -= mob.forward * mob.speed * time.dt
        mob.resume() # Animation.
        mob.is_playing=True
    else:
        mob.pause() # Animation.
        mob.is_playing=False

    terrain_walk_panda(mob, _td)

def terrain_walk_panda(mob, _td):
    blockFound=False
    position_before=mob.position
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