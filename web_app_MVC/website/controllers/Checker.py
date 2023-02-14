import numpy as np
from website.controllers.utils.constants import *
from sklearn.neighbors import NearestNeighbors
import cv2
import numpy as np


class Checker:
    
    def __init__(self):
        self.dataset_Cobra = np.load("D:\progetto_tesi\dataset_checker\dataset_Cobra.npy")
        self.dataset_Corpse = np.load("D:\progetto_tesi\dataset_checker\dataset_Corpse.npy")
        self.dataset_Lotus = np.load("D:\progetto_tesi\dataset_checker\dataset_Lotus.npy")
        self.dataset_Mountain = np.load("D:\progetto_tesi\dataset_checker\dataset_Mountain.npy")
        self.dataset_Tree = np.load("D:\progetto_tesi\dataset_checker\dataset_Tree.npy")
        self.dataset_Triangle = np.load("D:\progetto_tesi\dataset_checker\dataset_Triangle.npy")
        self.correzione = ''   
    
    def calculate_angle(self,a,b,c):
        #a,b e c sono array e dovrebbero essere composti da punti x,y, e confidence
        a=np.array(a) #first 
        b=np.array(b) #mid
        c=np.array(c) #end

        radians = np.arctan2(c[1]-b[1], c[0]-b[0])- np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = int(np.abs(radians*180.0/np.pi))

        if angle > 180.0:
            angle = 360 - angle
        
        return angle

    def calculate_all_angles(self,keypoints):
        agles_list=[]
        for key in ANGL_DICT:
                first_point=keypoints[ANGL_DICT[key][0]]
                second_point=keypoints[ANGL_DICT[key][1]]
                third_point=keypoints[ANGL_DICT[key][2]]
                angle=self.calculate_angle(first_point,second_point,third_point)
                agles_list.append([key,angle])
        return agles_list
    
    def knn_angoli(self,n_neighbors,samples,keypoint):
        two_dimension_samples=samples.reshape(samples.shape[0], 51)
        
        neigh = NearestNeighbors(n_neighbors=n_neighbors)
        neigh.fit(two_dimension_samples)
        
        two_dimension_keypoint = keypoint.reshape(1, -1)
        index=neigh.kneighbors(two_dimension_keypoint,#keypoint/frame
                            n_neighbors=n_neighbors, return_distance=False)
        #print(index)
        #print(index.shape)
        #print(index[0][0])
        #print(samples[index[0][0]])
        
        if(n_neighbors==1):
            angles_vid=self.calculate_all_angles(samples[index[0][0]])
        else:
            centroide=np.zeros((17,3))
            i=0
            for j in index[0]:

                centroide+=samples[j]
                i+=1
            centroide=centroide/i
            
            angles_vid=self.calculate_all_angles(centroide)
        
        return angles_vid
    
    def correct_angles_cobra(self,threshold, angles_vid, angles_u):
        stringa =''
        correct_angles=0
        for i in range(len(angles_vid)):
            diff=abs(angles_vid[i][1] - angles_u[i][1])
            if diff > threshold:
                if i == 0 or i == 4:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi le braccia")+"<br>"
                    correct_angles+=1
                elif i == 2 or i == 5:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le mani larghezza spalle")+"<br>"
                    correct_angles+=1
                elif i == 3 or i == 6:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le gambe largezza spalle")+"<br>"
                    correct_angles+=1
                elif i == 4 or i == 7:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi le gambe")+"<br>"
                    correct_angles+=1
        if correct_angles==0 :
            stringa=str("posizione corretta")

        return stringa  

    def correct_angles_corpse(self,threshold, angles_vid, angles_u):
        stringa =''
        correct_angles=0       
        for i in range(len(angles_vid)):
            diff=abs(angles_vid[i][1] - angles_u[i][1])
            if diff > threshold:
                if i == 0 or i == 4:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi meglio le braccia")+"<br>"
                    correct_angles+=1
                elif i == 2 or i == 5:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Disponi le braccia lungo i fianchi")+"<br>"
                    correct_angles+=1
                elif i == 3 or i == 6:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le gambe largezza spalle")+"<br>"
                    correct_angles+=1
                elif i == 4 or i == 7:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi meglio le gambe")+"<br>"
                    correct_angles+=1
        if correct_angles==0 :
            stringa=str("posizione corretta")

        return stringa     

    def correct_angles_lotus(self,threshold, angles_vid, angles_u):
        stringa =''
        correct_angles=0 
        for i in range(len(angles_vid)):
            diff=abs(angles_vid[i][1] - angles_u[i][1])
            if diff > threshold:
                if i == 0 or i == 4:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi meglio le braccia")+"<br>"
                    correct_angles+=1
                elif i == 2 or i == 5:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantenendo il busto dritto lascia cadere le braccia")+"<br>"#TO DO scrivere qualcosa di meglio
                    correct_angles+=1
                elif i == 3 or i == 6:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le gambe largezza spalle")+"<br>"
                    correct_angles+=1
                elif i == 4 or i == 7:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Incrocia meglio le gambe")+"<br>"
                    correct_angles+=1
        if correct_angles==0 :
            stringa=str("posizione corretta")

        return stringa  
    
    def correct_angles_mountain(self,threshold, angles_vid, angles_u):
        stringa =''
        correct_angles=0
        for i in range(len(angles_vid)):
            diff=abs(angles_vid[i][1] - angles_u[i][1])
            if diff > threshold:
                if i == 0 or i == 4:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi meglio le braccia")+"<br>"
                    correct_angles+=1
                elif i == 2 or i == 5:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Tira manggiormente le braccia verticalmente")+"<br>"
                    correct_angles+=1
                elif i == 3 or i == 6:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le gambe largezza spalle")+"<br>"
                    correct_angles+=1
                elif i == 4 or i == 7:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi meglio le gambe e sali maggiormente sulle punte dei piedi")+"<br>"
                    correct_angles+=1
        if correct_angles==0 :
            stringa=str("posizione corretta")

        return stringa  

    def correct_angles_tree(self,threshold, angles_vid, angles_u):
        stringa =''
        correct_angles=0
        for i in range(len(angles_vid)):
            diff=abs(angles_vid[i][1] - angles_u[i][1])
            if diff > threshold:
                if i == 0 or i == 4:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Unendo le mani cerca di fomare un angolo retto con il gomito")+"<br>"
                    correct_angles+=1
                elif i == 2 or i == 5:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Non tenere i gomiti esternamente ma lasciali vicino al corpo")+"<br>"
                    correct_angles+=1
                elif i == 3 or i == 6:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le gambe largezza spalle piegandone una")+"<br>"
                    correct_angles+=1
                elif i == 4 or i == 7:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distendi meglio una gamba e cerca di portare il piede in prossimità del ginochhio")+"<br>"
                    correct_angles+=1
        if correct_angles==0 :
            stringa=str("posizione corretta")
                
        return stringa   

                    
    def correct_angles_triangle(self,threshold, angles_vid, angles_u):
        stringa =''
        correct_angles=0
        for i in range(len(angles_vid)):
            diff=abs(angles_vid[i][1] - angles_u[i][1])
            if diff > threshold:
                if i == 0 or i == 4:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Distedi meglio le braccia ")+"<br>"
                    correct_angles+=1
                elif i == 2 or i == 5:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Disponi le braccia orizzontalmente e cerca di piegarti maggiormente verso la punta del piede")+"<br>"#TO DO scrivere qualcosa di meglio
                    correct_angles+=1
                elif i == 3 or i == 6:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Metti le gambe un po' più larghe rispetto alle spalle")+"<br>"
                    correct_angles+=1
                elif i == 4 or i == 7:
                    stringa=str("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))+"<br>"+stringa
                    stringa=stringa + str("Mantieni le gambe distese")+"<br>"
                    correct_angles+=1
        if correct_angles==0 :
            stringa=str("posizione corretta") 
        
        return stringa   

    def correct_angles(self,threshold, angles_vid, angles_u,posa):
        stringa =''
        if posa == 'Cobra':
            stringa = self.correct_angles_cobra(threshold, angles_vid, angles_u)
        elif posa== 'Corpse':
            stringa = self.correct_angles_corpse(threshold, angles_vid, angles_u)        
        elif posa== 'Lotus':
            stringa = self.correct_angles_lotus(threshold, angles_vid, angles_u)
        elif posa== 'Mountain':
            stringa = self.correct_angles_mountain(threshold, angles_vid, angles_u)        
        elif posa== 'Tree':
            stringa = self.correct_angles_tree(threshold, angles_vid, angles_u)        
        elif posa== 'Triangle':
            stringa = self.correct_angles_triangle(threshold, angles_vid, angles_u)
        
        self.correzione = stringa
            
    def draw_angles(self,angles_u,input_frame):
        output_frame =input_frame
        for i in range(len(angles_u)):
            cv2.putText(output_frame, angles_u[i][0]+": "+ str(angles_u[i][1]), (450,85+i*40), 
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1, cv2.LINE_AA)
        return output_frame

    def get_stringa(self):
        return self.correzione