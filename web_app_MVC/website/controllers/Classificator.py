from tensorflow import keras
import tensorflow as tf
import cv2

class Classificator:
    
    # costruttore rnn
    def __init__(self, model_rnn = "D:\\tesi\\notebook\model_RNN"):
        
        self.model = tf.keras.models.load_model(model_rnn)
        self.classificazione=' '
        
    #TO DO decidere se riscrivere la funzione
    #def predict(params):
        #self.model.predict(params)
        
    
    def prob_viz(self,res,actions,input_frame):
        output_frame =input_frame
        self.classificazione=''
        for num, pro in enumerate(res):
            cv2.rectangle(output_frame,(0,60+num*40), 
                        (int(pro*100), 90+num*40),(255,0,255), -1)
            cv2.putText(output_frame, actions[num], (0,85+num*40), 
                        cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2, cv2.LINE_AA)
            prob = int(pro*100)
            action= actions[num]
            self.classificazione = str(action) + str(prob) +'\n'+self.classificazione
        return output_frame
    
    def get_prob_viz(self,res,actions):
        for num, pro in enumerate(res):
        
            prob = int(pro*100)
            action= actions[num]
            stringa = str(action) + str(prob) +'\n'+stringa
            
        return stringa
    
    def get_stringa(self):
        return self.classificazione

