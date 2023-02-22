def correct_angles_triangle(threshold, angles_vid, angles_u):
    correct_angles=0
    for i in range(len(angles_vid)):
        diff=abs(angles_vid[i][1] - angles_u[i][1])
        if diff > threshold:
            if i == 0 or i == 4:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Distedi meglio le braccia ")
                correct_angles+=1
            elif i == 2 or i == 5:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Disponi le braccia orizzontalmente e cerca di piegarti maggiormente verso la punta del piede")
                correct_angles+=1
            elif i == 3 or i == 6:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Metti le gambe un po' più larghe rispetto alle spalle")
                correct_angles+=1
            elif i == 4 or i == 7:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Mantieni le gambe distese")
                correct_angles+=1
        if correct_angles==0 :
            print("posizione corretta")   