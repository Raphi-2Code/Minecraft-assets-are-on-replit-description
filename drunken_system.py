from ursina import *
from mesh_terrain import *

zombie = FrameAnimation3d('minecraft-zombie\zombieobject_', fps=2, collider='mesh')
zombie.texture = 'zombie_two.png'
zombie.position = Vec3(200,0,0)
ZOMBIEcounter=0
already_deadz=False
from mob_system import *
def ZOMBIE(player,perlin):
    global ZOMBIEcounter,already_deadz
    if already_deadz==False:
        ENT=Entity(position=zombie.position)
        ENT.lookAt(player)
        ENT.rotation_y-=180
        zombie.rotation_y=ENT.rotation_y
        try:
                if build[f"{zombie.x},{zombie.z}"]=="e" and vd[zombie.x,zombie.y,zombie.z]==None:
                    pass
                else:
                    if zombie.x>player.x:
                        zombie.x-=0.1
                    if zombie.x<player.x:
                        zombie.x+=0.1
                    if zombie.z>player.z:
                        zombie.z-=0.1
                    if zombie.z<player.z:
                        zombie.z+=0.1
                    zombie.y=perlin.getHeight(zombie.x,zombie.z)
        except:
                if zombie.x > player.x:
                    zombie.x -= 0.1
                if zombie.x < player.x:
                    zombie.x += 0.1
                if zombie.z > player.z:
                    zombie.z -= 0.1
                if zombie.z < player.z:
                    zombie.z += 0.1
                zombie.y = perlin.getHeight(zombie.x, zombie.z)
        if distance(player,zombie)<=3:
            zombie.x-=1
            ZOMBIEcounter+=1

        if ZOMBIEcounter>=30:
            if ZOMBIEcounter==30:
                tex.text="NONONONO! I died cause of this mad zombie!"
                zombie.y=7000
                already_deadz=True