from ursina import *
from mesh_terrain import *

drowned = FrameAnimation3d('minecraft-drowned\drowned_', fps=2, collider='mesh')
drowned.texture = 'drowned.png'
drowned.position = Vec3(10,0,50)
DROWNEDcounter=0
already_drowned=False
from mob_system import *
def DROWNED(player,perlin):
    global DROWNEDcounter,already_drowned
    if already_drowned==False:
        ENTi=Entity(position=drowned.position)
        ENTi.lookAt(player)
        ENTi.rotation_y-=180
        drowned.rotation_y=ENTi.rotation_y
        try:
                if build[f"{drowned.x},{drowned.z}"]=="e" and vd[zombie.x,zombie.y,zombie.z]==None:
                    pass
                else:
                    if drowned.x>player.x:
                        drowned.x-=0.1
                    if drowned.x<player.x:
                        drowned.x+=0.1
                    if drowned.z>player.z:
                        drowned.z-=0.1
                    if drowned.z<player.z:
                        drowned.z+=0.1
                    drowned.y=perlin.getHeight(drowned.x,drowned.z)
        except:
                if drowned.x > player.x:
                    drowned.x -= 0.1
                if drowned.x < player.x:
                    drowned.x += 0.1
                if drowned.z > player.z:
                    drowned.z -= 0.1
                if drowned.z < player.z:
                    drowned.z += 0.1
                drowned.y = perlin.getHeight(drowned.x, drowned.z)
        if distance(player,drowned)<=3:
            drowned.x-=1
            DROWNEDcounter+=1

        if DROWNEDcounter>=30:
            if DROWNEDcounter==30:
                tex.text="NONONONO! I died cause of this mad drowned!"
                drowned.y=7000
                already_drowned=True