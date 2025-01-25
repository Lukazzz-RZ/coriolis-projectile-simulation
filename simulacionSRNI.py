
import numpy as np
import matplotlib.pyplot as plt

r0 = np.array([0,0,1.5+6.4*10**6]) # x,y,z
v0 = np.array([0,50,50])  #vx,vy,vz
w = np.array([0,np.cos(np.pi/3),np.sin(np.pi/3)])
w = w*0.00007272205
g = 9.81
roz = 0.15
roz_esp = roz

def prodVect(v1,v2):

    if not len(v1) == len(v2):
        print("Los vectores no tienen la misma dimension" )
        exit()
    else:
        w = np.zeros(len(v1)) 
        for i in range(len(v1)):

            w[i] =  (v1[(i+1)%3]*v2[(i+2)%3] - v1[(i+2)%3]*v2[(i+1)%3]) 
            
        return np.array(w)
    
def AceleracionCoriolis(v,w):
    return prodVect(2*v,w)

def AceleracionCentripeta(r,w):
    return prodVect(prodVect(w,r),w)
    

dt = 0.1
t = [0]
r = [r0]
v = [v0]

distancia = 0
while r[-1][2] > 6.4*10**6:
    a_i = np.array([0,0,-g]) -roz*v[-1] + AceleracionCoriolis(v[-1],w) + AceleracionCentripeta(r[-1],w)
    v.append(v[-1]+a_i*dt)
    r.append(r[-1]+v[-1]*dt)
    t.append(t[-1]+dt)
    r_efec1 = r[-1]-[0,0,6.4*10**6]
    r_efec2 = r[-1]-[0,0,6.4*10**6]
    distancia = distancia + np.sqrt(np.dot(r_efec1-r_efec2,r_efec1-r_efec2))
    
r_esp = [r0]
v_esp = [v0]
for i in range(len(t)):
    v_esp.append(v_esp[-1]+(np.array([0,0,-g])-roz_esp*v_esp[-1])*dt)
    r_esp.append(r_esp[-1]+v_esp[-1]*dt+0.5*(np.array([0,0,-g])-roz_esp*v_esp[-1])*dt**2)

print("distancia recorrida: " + str(distancia))
x=[]
y=[]
z=[]
x_esp=[]
y_esp=[]
z_esp=[]
for i in range(len(t)):
    x.append(r[i][0])
    y.append(r[i][1])
    z.append(r[i][2]-6.4*10**6)
    x_esp.append(r_esp[i][0])
    y_esp.append(r_esp[i][1])
    z_esp.append(r_esp[i][2]-6.4*10**6)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c='r')
ax.scatter(x_esp, y_esp, z_esp, c='b')
plt.show()



                              
                            ########              
                          ######  ####            
                          ######  ############    
                          ##################      
                            ########              
                            ######                
                            ######                
                            ######                
                            ########              
                          ############            
                        ##############            
                      ##################          
          ##############################                
        ################################          
        ################################          
          ############################            
                ####################              
                    ####                          
                    ########                     
                      #####