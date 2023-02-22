def correct_angles_tree(threshold, angles_vid, angles_u):
    correct_angles=0
    for i in range(len(angles_vid)):
        diff=abs(angles_vid[i][1] - angles_u[i][1])
        if diff > threshold:
            if i == 0 or i == 4:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Unendo le mani cerca di fomare un angolo retto con il gomito")
                correct_angles+=1
            elif i == 2 or i == 5:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Non tenere i gomiti esternamente ma lasciali vicino al corpo")
                correct_angles+=1
            elif i == 3 or i == 6:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Mantieni le gambe largezza spalle piegandone una")
                correct_angles+=1
            elif i == 4 or i == 7:
                print("Angolo {} sbagliato di: {} gradi".format(angles_vid[i][0], diff))
                print("Distendi meglio una gamba e cerca di portare il piede in prossimità del ginochhio")
                correct_angles+=1
        if correct_angles==0 :
            print("posizione corretta")   