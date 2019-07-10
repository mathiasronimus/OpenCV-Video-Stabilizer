import numpy as np
import cv2
import sys

# The maximum amount an image may be translated in either direction or axis
MAXIMUM_TRANSLATION = 20

# Parse the command-line arguments
argc = len(sys.argv)
if argc is not 3:
    print('Incorrect arguments. Use python <name of this script> <path to input video> <path to output video>')
    quit()

inputFile = sys.argv[1]
saveFile = sys.argv[2]

# Load video
vidIn = cv2.VideoCapture(inputFile)

# Get video dimensions
origVidWidth = int(vidIn.get(cv2.CAP_PROP_FRAME_WIDTH))
origVidHeight = int(vidIn.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Output file
fourCC = cv2.VideoWriter_fourcc(*"mp4v")
vidOut = cv2.VideoWriter(saveFile, fourCC, vidIn.get(cv2.CAP_PROP_FPS), (origVidWidth - MAXIMUM_TRANSLATION * 2, origVidHeight - MAXIMUM_TRANSLATION * 2))

# Process the video frame by frame
oldFrame = None
olderFrame = None
while (vidIn.isOpened()):
    ret, frame = vidIn.read()
    if frame is None:
        break

    # Frames need information from the adjacent frames to be
    # processed, so we need to wait until we have three frames.
    if oldFrame is not None and olderFrame is not None:
        # Process the middle frame (oldFrame)

        # Convert frames to grayscale for correlation
        olderFrameGray = cv2.cvtColor(olderFrame, cv2.COLOR_BGR2GRAY)
        oldFrameGray = cv2.cvtColor(oldFrame, cv2.COLOR_BGR2GRAY)
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Then convert to float 32 format
        olderFrameGray = np.float32(olderFrameGray)
        oldFrameGray = np.float32(oldFrameGray)
        frameGray = np.float32(frameGray)

        # Find the correlation for each image transition
        oldCorr = cv2.phaseCorrelate(olderFrameGray, oldFrameGray)[0]
        currCorr = cv2.phaseCorrelate(oldFrameGray, frameGray)[0]

        # The shift for the middle frame will be the average of both
        shiftX = (currCorr[0] - oldCorr[0]) / 2
        shiftY = (currCorr[1] - oldCorr[1]) / 2

        # Don't shift more than MAXIMUM_TRANSLATION
        shiftX = min(shiftX, MAXIMUM_TRANSLATION)
        shiftY = min(shiftY, MAXIMUM_TRANSLATION)

        # Create translation matrix and get translated image
        translateMatrix = np.float32(   [[1, 0, shiftX],
                                         [0, 1, shiftY]])
        processedFrame = cv2.warpAffine(oldFrame, translateMatrix, (origVidWidth, origVidHeight))

        # Crop the frame to remove black bars introduced by translation
        processedFrame = processedFrame[MAXIMUM_TRANSLATION:origVidHeight - MAXIMUM_TRANSLATION, MAXIMUM_TRANSLATION:origVidWidth - MAXIMUM_TRANSLATION]
        vidOut.write(processedFrame)
    # ENDIF

    # Done processing, move frames along
    olderFrame = oldFrame
    oldFrame = frame

# Clean up resources
vidIn.release()
