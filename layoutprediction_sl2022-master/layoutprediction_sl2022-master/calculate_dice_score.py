import cv2
import numpy as np
import os
import json
import glob
'''
!!!Script and functions to calculate the dice value of two pictures
The dice score is a percentage value comparing two same sized pictures. Compares every pixel with the corresponding pixel of the other picture and check if the pixel is colored or not
Saves the results in a .json-file.
Original calculation was taken from 
https://stackoverflow.com/questions/49759710/calculating-dice-co-efficient-between-two-random-images-of-same-size

'''

def calculate_dice_score(img_name, img_name2):
    '''!!!Calculating the dice score with every pixel
    @param img_name: file path to first image file
    @param img_name2: file path to second image file
    '''
    #load images
    img = cv2.imread(img_name)
    img2 = cv2.imread(img_name2)

    #formate images
    img = np.asarray(img).astype(bool)
    img2 = np.asarray(img2).astype(bool)

    #calculate score
    if img.shape != img2.shape:
        raise ValueError("Shape mismatch: img and img2 must have the same shape to compare them.")
    else:
        lenIntersection=0
        number_of_colored_pixels = 0
            
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if ( np.array_equal(img[i][j],img2[i][j]) ):
                    lenIntersection+=1
             
        lenimg=img.shape[0]*img.shape[1]
        lenimg2=img2.shape[0]*img2.shape[1]  
        value = (2. * lenIntersection  / (lenimg + lenimg2))
        print(value)
    return value 

def calculate_dice_score_adjusted(img_name, img_name2):
    '''!!!Calculating the dice score with every colorized pixel
    @param img_name: file path to first image file
    @param img_name2: file path to second image file
    '''
    #load images
    img = cv2.imread(img_name)
    img2 = cv2.imread(img_name2)

    #formate images
    img = np.asarray(img).astype(bool)
    img2 = np.asarray(img2).astype(bool)

    #calculate score
    if img.shape != img2.shape:
        raise ValueError("Shape mismatch: img and img2 must have the same shape to compare them.")
    else:
        lenIntersection=0
        number_of_colored_pixels = 0
            
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if(True in img[i][j]  or  True in img2[i][j]):
                    number_of_colored_pixels += 1
                    if ( np.array_equal(img[i][j],img2[i][j])):        
                        lenIntersection+=1
        value = (2. * lenIntersection  / (number_of_colored_pixels))
        print(value)
    return value 


if __name__ == '__main__':

    #initialize lists
    results = []
    results_adjusted = []

    #finding the ground truth dark pictures
    path_string = os.getcwd() + '\example\eval-original-layout\*dark.png'
    print(path_string)
    dark_pictures = glob.glob(path_string)

    #iterating the dark pictures and calculating the Dice similarity coefizient
    for iter, file in enumerate(dark_pictures): 
        results.append(calculate_dice_score(f'./example/eval-original-layout/{iter}_ground_truth_dark.png' , f'results/{iter}_lines_dark.png'))
        results_adjusted.append(calculate_dice_score_adjusted(f'./example/eval-original-layout/{iter}_ground_truth_dark.png' , f'results/{iter}_lines_dark.png'))

    #calculating the average to have get a better value
    average = np.sum(results)/iter
    average_adjusted = np.sum(results_adjusted)/iter

    #saving the inforamtion into a json file to have it accesable
    with open("dice_scores.json", "w") as outfile:
        json.dump(results, outfile)
        json.dump(average, outfile)

    with open("dice_scores_adjusted.json", "w") as outfile:
        json.dump(results_adjusted, outfile)
        json.dump(average_adjusted, outfile)