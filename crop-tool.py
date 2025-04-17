import cv2

def mouse_callback(action, x, y, flags, userdata):
    global mousePressed, startX, startY
    if action == cv2.EVENT_LBUTTONDOWN:
        mousePressed, startX, startY = True, x, y
        image_for_frame[:] = image_with_text
    elif action == cv2.EVENT_MOUSEMOVE:
        if mousePressed:
            temp_image = image_with_text.copy()
            cv2.rectangle(temp_image, (startX, startY), (x,y), (0,255,0), 1)
            image_for_frame[:] = temp_image
        else:
            return
    elif action == cv2.EVENT_LBUTTONUP:
        mousePressed = False
        minX = min(startX, x)
        minY = min(startY, y)
        maxX = max(startX, x)
        maxY = max(startY, y)
        if (maxX - minX >= minCropX and maxY - minY >= minCropY):
            cropped_image = base_image[minY:maxY, minX:maxX]
            cv2.imwrite("face.jpg", cropped_image)
            temp_image = image_with_text.copy()
            cv2.rectangle(temp_image, (startX, startY), (x, y), (0, 255, 0), 2)
            cv2.putText(temp_image, "image saved",
                        (minX+10, maxY+20 if imageHeight-maxY>20 else maxY-20),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.8, color=(0, 255, 0))
            image_for_frame[:] = temp_image
            cv2.waitKey(200)
    else:
        return
    cv2.imshow("sample window", image_for_frame)

mousePressed, startX, startY, minCropX, minCropY = False, -1, -1, 10, 10
base_image = cv2.imread('sample.png',cv2.IMREAD_UNCHANGED)
_, imageHeight, _ = base_image.shape
image_with_text = base_image.copy()
cv2.putText(image_with_text, "choose any corner and drag",
                (20,imageHeight-20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.8, color=(255,255,255))
cv2.namedWindow("sample window")
cv2.imshow("sample window", image_with_text)
image_for_frame = image_with_text.copy()
cv2.setMouseCallback("sample window", mouse_callback)

while True:
    k = cv2.waitKey(20)
    if k == 27:
        break

cv2.destroyAllWindows()