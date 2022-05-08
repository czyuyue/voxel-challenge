from scene import Scene; import taichi as ti; from taichi.math import *; ti.init(arch=ti.gpu)
ti.init(random_seed=236587456)
scene = Scene(voxel_edges=0, exposure=1); scene.set_floor(-64.0, (1.0, 1.0, 1.0))
scene.set_directional_light((1, 1, 1), 0.1, (1, 1, 1)); scene.set_background_color((0.3, 0.4, 0.6))
darkbrown=vec3(0.95686,0.64314,0.37647)*0.666
navajowhite=vec3(0.5451,0.47451,0.36863)
chocolate=vec3(0.82353,0.41176,0.11765)*0.5
@ti.func
def rvec3():
    return vec3(ti.random(),ti.random(),ti.random())
@ti.func
def create_tree(x,y,height,base_color,rad):
    for h in ti.ndrange((-64,height)):
        col=vec3(0.82745,0.82745,0.82745)
        if ti.random()<0.4:
            col=vec3(0.0,0.0,0.0)
        for i,j in ti.ndrange((x,x+rad),(y,y+rad)):
            if ti.random()<0.2:
                col=vec3(0.82745,0.82745,0.82745)
            if (not all(col==vec3(0.0,0.0,0.0))) and ti.random()<0.3:
                tmp=ti.random(); col=col-vec3(tmp,tmp,tmp)*0.2
            scene.set_voxel(vec3(i, h, j), 1, col)
    tmp=-60+(height+60)/3.2; num_ball=0
    while tmp<height-5:
        tmp+=ti.random()*4;len=1+(0.75*(60+height)-tmp)**0.50;
        dir=rvec3()-0.5;dir[1]=abs(dir[1])/3.0;dir=dir/dir.norm()
        for i in range(len):
            pos=vec3(x,tmp,y)+dir*i*3+(rvec3()-0.5)*3;scene.set_voxel(pos, 2, vec3(1.0,1.0,0))
            for num in range(10):
                ps=pos+(rvec3()-0.2)*len; scene.set_voxel(vec3(ps[0],ps[1],ps[2]), 2, vec3(1.0,1.0,0))
    for h,i,j in ti.ndrange((-60,64),(-60,60),(-60,60)):
        if i<x or i>=x+rad or j<y or j>=y+rad:
            flag=0
            for dx,dy,dz in ti.ndrange((-3,4),(-3,4),(-3,min(4,64-h))):
                mat,color=scene.get_voxel(vec3(i+dx,h+dz,j+dy))
                flag=(1 if ((vec3(dx,dy,dz)).norm()<2.5 and mat==2) else flag)
            if flag:
                col=base_color+(rvec3()-vec3(0.5))*0.3
                if ti.random()<0.1:
                    scene.set_voxel(vec3(i, h, j), 1, col)
    for h,i,j in ti.ndrange((-64,64),(-64,64),(-64,64)):
        mat,color=scene.get_voxel(vec3(i,h,j))
        scene.set_voxel(vec3(i, h, j), (0 if mat==2 else mat),color)
@ti.func
def drawleg(pos,op):
    scene.set_voxel(vec3(pos[0], -59, pos[1]), 1, vec3(0.41176,0.41176,0.41176)*0.22)
    for i in range(3):
        scene.set_voxel(vec3(pos[0], -58+i, pos[1]), 1, navajowhite)
    for i in range(7):
        for j in ti.ndrange(((i>1),min(i+1,4))):
            scene.set_voxel(vec3(pos[0]-j*op, -55+i, pos[1]), 1, chocolate*(ti.random()*0.2+0.9))
@ti.func
def create_deer(x,y):
    leg1=vec2(x,y); leg2=vec2(x,y-4)
    leg3=vec2(x-13,y);leg4=vec2(x-13,y-4);drawleg(leg1,1);drawleg(leg2,1);drawleg(leg3,-1);drawleg(leg4,-1)
    for i,j,h in ti.ndrange((x-12,x+3),(y-3,y),(-52,-47)):
        if h+52>1:
            scene.set_voxel(vec3(i,h,j)+vec3(0,(i>=x-1)*(i-x+1),0), 1, chocolate*0.77*(ti.random()*0.2+0.9))
        else :
            scene.set_voxel(vec3(i,h,j)+vec3(0,(i>=x-1)*(i-x+1),0), 1, navajowhite*1.33*(ti.random()*0.2+0.9))
    for i,j,h in ti.ndrange((x+1,x+4),(y-3,y),(-47,-41)):
        if (i==x+3 or (i==x+2 and h==-47)) and h<-44:
            scene.set_voxel(vec3(i,h,j), 1, navajowhite*1.33*(ti.random()*0.2+0.9))
        else:
            scene.set_voxel(vec3(i,h,j), 1, chocolate*0.77*(ti.random()*0.2+0.9))
    scene.set_voxel(vec3(x+3,-43,y-3), 1, vec3(0.0,0.0,0.0)); scene.set_voxel(vec3(x+3,-43,y-1), 1, vec3(0.0,0.0,0.0))
    scene.set_voxel(vec3(x+4,-42,y-2), 1, chocolate*0.77); scene.set_voxel(vec3(x+4,-43,y-2), 1, chocolate*0.77)
    scene.set_voxel(vec3(x+4,-44,y-2), 1, chocolate*0.77); scene.set_voxel(vec3(x+5,-43,y-2), 1, navajowhite*1.33)
    scene.set_voxel(vec3(x+5,-44,y-2), 1, navajowhite*1.33); scene.set_voxel(vec3(x+6,-43,y-2), 1, darkbrown*0.2)
    scene.set_voxel(vec3(x+6,-44,y-2), 1, darkbrown*0.2); scene.set_voxel(vec3(x+1,-42,y), 1, chocolate*0.77)
    scene.set_voxel(vec3(x+2,-42,y), 1, chocolate*0.77); scene.set_voxel(vec3(x+1,-42,y-4), 1, chocolate*0.77)
    scene.set_voxel(vec3(x+2,-42,y-4), 1, chocolate*0.77); scene.set_voxel(vec3(x-13,-48,y-2), 1, navajowhite)
    for i in range(3):
        scene.set_voxel(vec3(x+1,-41,y-3)+vec3(0,i,0), 1, navajowhite*0.8)
        scene.set_voxel(vec3(x+1,-41,y-1)+vec3(0,i,0), 1, navajowhite*0.8)
@ti.kernel
def init():
    n=60; turn=vec2(ti.random()*10-5,ti.random()*10-5)
    O1=vec2(-60.0,turn[1]); O2=vec2(60.0,turn[1]);
    rad1=(O1-vec2(-60.0,-60.0)).norm(); rad2=(O2-vec2(60.0,60.0)).norm()
    for i, j in ti.ndrange((-n,n), (-n,n)):
        pos=vec2(i,j); d1=(pos-O1).norm(); d2=(pos-O2).norm()
        if abs(d1-rad1)<6.5 and j<=turn[1]+2 or abs(d2-rad2)<6.5 and j>=turn[1]-2:
            scene.set_voxel(vec3(i, -60, j), 1, darkbrown+0.1*(rvec3()-0.5))
        elif (abs(d1-rad1)<7.5 and j<=turn[1]+2 or abs(d2-rad2)<7.5 and j>=turn[1]-2) and ti.random()<0.75:
            scene.set_voxel(vec3(i, -60, j), 1, darkbrown*0.80+0.1*(rvec3()-0.5))
        else :
            scene.set_voxel(vec3(i, -60, j), 1, vec3(0.13333,0.5451,0.13333)+0.15*(rvec3()-0.5))
            if i>-55 and i<55 and j>-55 and j<55:
                if ti.random()<0.005:
                    height=int(2+ti.random()*2.5)
                    for h in ti.ndrange((-60,-60+height+1)):
                        scene.set_voxel(vec3(i, h, j), 1, vec3(0.0, 0.39216, 0.0)+0.1*(rvec3()-0.5))
        for h in range(-64,-60):
            scene.set_voxel(vec3(i,h,j),1,darkbrown+0.2*(rvec3()-0.5))
    create_tree(30,-25,30,vec3(0.85,0.647,0.125)+(rvec3()-0.5)*0.001,3); create_tree(-20,-15,55,vec3(1.0,0.843,0.0),4)
    create_tree(-30,27,10,vec3(0.72157,0.52549,0.04314)+(rvec3()-0.5)*0.1,3); create_deer(50,44)
init()
scene.finish()
