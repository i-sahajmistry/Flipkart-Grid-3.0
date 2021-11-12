    _, frame = vid.read()

    detectMarker(frame, location, markerSize=4, totalMarker=50, draw=True)

    # corners = [location[47][4], location[46][4], location[47][4], location[48][4]]
    # print(corners)
    pts1 = np.float32([[1139, 22], [543, 20], [1139, 22], [1180, 674]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    frame = cv2.warpPerspective(frame, matrix, (width, height))

    cv2.imshow('frame', frame)
    cv2.waitKey(1)