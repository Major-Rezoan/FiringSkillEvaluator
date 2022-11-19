import sqlite3
import cv2

def Long_Hor_Err(img, text_SL):
    cv2.putText(img, 'Reasons:' , (820,text_SL), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Left hand moving horizontally for poor holding.', (820,text_SL+30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA) 
    cv2.putText(img, '(2) Lateral error in alignment of back sight U and front sight tip.', (820,text_SL+55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, 'Solutions:' , (820,text_SL+90), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Firming the grip of left/Right hand (for left/right hand firers).', (820,text_SL+115), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(2) Align the frontsight tip and backsight U properly', (820,text_SL+140), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    return img

def Long_Vert_Err(img, text_SL):
    cv2.putText(img, 'Reasons:' , (820,text_SL), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Wrong breathing control, (barrel moves with rise and fall of chest).', (820,text_SL+30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA) 
    cv2.putText(img, '(2) Vertical error in alignment of back sight U and front sight tip.', (820,text_SL+55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, 'Solutions:' , (820,text_SL+90), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Control breathing, Follow the marksmanship principal.', (820,text_SL+115), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(2) Align the frontsight tip and backsight U properly.', (820,text_SL+140), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    return img

def Bi_Focal_Err(img, text_SL):
    cv2.putText(img, 'Reasons:' , (820,text_SL), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Bullet hits below the point of aim once giving much stress on point', (820,text_SL+30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA) 
    cv2.putText(img, 'of aim and vice versa while stressed on tip.', (820,text_SL+55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, '(2) Not understanding the trigger pull.', (820,text_SL+80), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, 'Solutions:' , (820,text_SL+115), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Aiming by focusing on the target, not on frontsight tip/backsight U.', (820,text_SL+140), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(2) Following trigger pull mechanism', (820,text_SL+165), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    return img

def Scat_Gp_Err(img, text_SL):
    cv2.putText(img, 'Reasons:' , (820,text_SL), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) All factors of correct hold are not ensured.', (820,text_SL+30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA) 
    cv2.putText(img, '(2) Frequent movement of elbows and body while firing', (820,text_SL+55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, 'Solutions:' , (820,text_SL+90), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Ensuring correct hold and position.', (820,text_SL+115), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(2) Keeping hands firm and body position fixed during firing.', (820,text_SL+140), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    return img

def Impat_Shot_Err(img, text_SL):
    cv2.putText(img, 'Reasons:' , (820,text_SL), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Weakness to hold weapon patiently till the last.', (820,text_SL+30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA) 
    cv2.putText(img, '(2) Firing shots at a long interval', (820,text_SL+55), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 105, 250), 1, cv2.LINE_AA)
    cv2.putText(img, 'Solutions:' , (820,text_SL+90), cv2.FONT_HERSHEY_DUPLEX, 0.65, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(1) Keep patience till the end of firing.', (820,text_SL+115), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    cv2.putText(img, '(2) Finish the shots within optimum time.', (820,text_SL+140), cv2.FONT_HERSHEY_DUPLEX, 0.6, (35, 250, 105), 1, cv2.LINE_AA)
    return img

def put_corrections(img, error_name, text_SL):
    if (error_name == "Long Vertical Error"):        
        Long_Vert_Err(img, text_SL)
    elif (error_name == "Bi-focal Error"):        
        Bi_Focal_Err(img, text_SL)
    elif (error_name == "Long Horizontal Error"):        
        Long_Hor_Err(img, text_SL)
    elif (error_name == "Impatient Shot"):        
        Impat_Shot_Err(img, text_SL)
    elif (error_name == "Scattered Group"):        
        Scat_Gp_Err(img, text_SL)
