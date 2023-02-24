def calculate_all_angles(keypoints):
    agles_list=[]
    for key in ANGL_DICT:
            first_point=keypoints[ANGL_DICT[key][0]]
            second_point=keypoints[ANGL_DICT[key][1]]
            third_point=keypoints[ANGL_DICT[key][2]]
            angle=calculate_angle(first_point,second_point,third_point)
            agles_list.append([key,angle])
    return agles_list