import numpy as np
import cv2
import json
from matplotlib import pyplot as plt

def detect(filename, debug):

    img1 = cv2.imread('template_scaled.jpg',0)          # queryImage
    img2 = cv2.imread(filename,0) # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    #for i,(m,n) in enumerate(matches):
    #    if m.distance < 0.7*n.distance:
    #        matchesMask[i]=[1,0]

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good)>10:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

        #print(src_pts);
        #print([ kp1[m.queryIdx].pt for m in good ]);

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

        #print(M[0:2])

        Minv = np.linalg.inv(M)

        #print(Minv)

        #h,w = img1.shape
        #pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        #dst = cv2.perspectiveTransform(pts,M)

        #img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
        #img1Aff = cv2.warpAffine(img1, M[0:2], (640, 853))
        img2Aff = cv2.warpAffine(img2, Minv[0:2], (500,217))
        #print(img1Aff)
        #img2np = np.array(img2)
        #img1Affnp = np.array(img2Aff)
        #test = np.where(img1Affnp != 0)
        #print(test)

        img1 = cv2.blur(img1,(49,49))

        pts2 = []
        for i in range(len(img1)):
            for j in range(len(img1[i])):
                if img1[i][j] < 140 or img2Aff[i][j] > 100 or j <50 or j>450:
                    img2Aff[i][j] = 255
                else:
                    img2Aff[i][j] = 0
                    pts2.append([j,i])
        #plt.imshow(img1, 'gray'),plt.show()
        print(pts2)
        pts2 = np.float32(pts2).reshape(-1,1,2)
        #pts2 = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        print(pts2)
        dst2 = cv2.perspectiveTransform(pts2,M)

        #print(dst2)

        json_out = []
        for t in dst2:
            print(t)
            y = int(t[0][0])
            x = int(t[0][1])
            if x<len(img2) and y<len(img2[0]) and x>=0 and y>=0:
                img2[x][y] = 255
                json_out.append([x,y])
        #plt.imshow(img1Aff, 'gray'), plt.show()
        #print(json.dumps(json_out))
        #plt.imshow(img2, 'gray'), plt.show()
        return json_out;
        exit()

    else:
        print("Not enough matches are found")
        matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

    plt.imshow(img3, 'gray'),plt.show()

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

    #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

    #plt.imshow(img3,),plt.show()

    return [];