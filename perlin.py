from perlin_module import PerlinNoise
import random
class Perlin:
    def __init__(this):
        try:this.seed=int(open("seed.txt","r").read())
        except:
            text=open("seed.txt","x")
            this.seed = int(str(random.random()).lstrip("0."))  # ord("o")+ord("q")
            text.write(this.seed)
            print(this.seed)
            text.close()

        this.octaves = 8
        this.freq = 256
        this.amp = 18    

        this.pNoise_continental = PerlinNoise( seed=this.seed,
                                    octaves=1)

        this.pNoise_details = PerlinNoise(  seed=this.seed,
                                    octaves=this.octaves)
        

    def getHeight(this,x,z):
        from math import sin
        y = 0
        y = this.pNoise_continental([x/512,z/512])*128
        y += this.pNoise_details([x/this.freq,z/this.freq])*this.amp
        
        # Apply some predictable surface variation.
        sAmp=0.33
        y+=sin(z)*sAmp
        y+=sin(x*0.5)*sAmp
        #if y<=-23:
        #    y=-23
        return y