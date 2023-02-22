def extract_all_keypoints(directory_path,actions):
     for file in actions:
        
        file_path = os.path.join(directory_path, file)

        video_list = []
        for f in os.listdir(file_path):
            name, ext = os.path.splitext(f)
            if ext == '.mp4':
                video_list.append(f)
    
        for video in video_list:
            
            video_path = os.path.join(file_path,video) 
            cap = cv2.VideoCapture(video_path)
            
            #Ottengo il numero di frames totali
            video_frames_count= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        
            video_height, video_width = [768, 1366]# sostituire con funzione
            crop_region = init_crop_region(video_height, video_width)
            
            i=1
       
            for frame_counter in range(video_frames_count):
                try:                
                    #leggo il frame               
                    ret,frame = cap.read()
                    
                    #se non viene letto esco
                    if not ret:
                        break
                    
                    image = frame.copy()
                    cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                    keypoints_with_scores = run_inference(
                    movenet, image, crop_region,
                    crop_size=[256, 256])# sostituire con variabile

                    crop_region = determine_crop_region(
                    keypoints_with_scores, video_height, video_width)
                    
                    keypoints = extract_keypoints(keypoints_with_scores)
                
                    npy_path = os.path.join(file_path,video +"_landmarks",str(i))
                    np.save(npy_path, keypoints)                                        
                    i+=1
                    print(i)
                    print(npy_path)
                except:
                    pass

            cap.release()
            cv2.destroyAllWindows()