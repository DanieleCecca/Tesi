sequences=[]
group_sequences=[]
group=[]
labels=[]
j=0
for file in actions:
        file_path = os.path.join(DATA_PATH, file)
        
        key_dir_list = []
        for f in os.listdir(file_path):
            name, ext = os.path.splitext(f)
            if not ext == '.mp4':
                key_dir_list.append(f)
                

        i=0
        for keypoint_dir in key_dir_list:
            window = []
            for frame_num in range(1, info_videos[j][1][i][1]):
                group=[x for x in range(len(key_dir_list))]
                frame_path = np.load(os.path.join(file_path,keypoint_dir,"{}.npy".format(frame_num)))
                window.append(frame_path)
                if frame_num%45==0:    
                    sequences.append(window)
                    group_sequences.append(group[i])
                    labels.append(label_map[file])
                    window=[]                             
                    
            i+=1
        j+=1