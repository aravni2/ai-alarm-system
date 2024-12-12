import face_recognition
import os
import sys
import cv2
import numpy as np
# https://www.youtube.com/watch?v=535acCxjHCI


class Video():
    def __init__(self) -> None:
        self.known_faces_dir = "known_faces"
        self.unknown_faces_dir = "unknown_faces"
        self.tolerance = .6
        self.frame_thickness = 3
        self.font_thickness = 2
        self.model = "cnn" #hog
        self.process_this_frame = True
        self.known_faces = []
        self.known_names = []
        self.face_locations = []
        self.face_encodings= []
        self.face_names = []
        self.matches = []

        self.video_capture = cv2.VideoCapture(0)

    def load_faces(self):
        """Load faces from "known_faces" folder
        """
        for name in os.listdir(self.known_faces_dir):
            for filename in os.listdir(f"{self.known_faces_dir}/{name}"):
                print(filename)
                image = face_recognition.load_image_file(f"{self.known_faces_dir}/{name}/{filename}")
                encoding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(encoding)
                self.known_names.append(name)

    def check_faces(self):
        """Compare video frame to faces in known faces folder to see if matching,
            This also frames out and labels the face with the persons name based on the folder itself
            Will label "uknown" if face doesn't appear
        """
            # Grab a single frame of video
        ret, frame = self.video_capture.read()

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                self.matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in self.matches:
                    first_match_index = self.matches.index(True)
                    name = self.known_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                # face_distances = face_recognition.face_distance(known_faces, face_encoding)
                # best_match_index = np.argmin(face_distances)
                # if matches[best_match_index]:
                #     name = known_names[best_match_index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom+35), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom +29), font, 1.0, (255, 255, 255), 1)
            print(name)

        # Display the resulting image
        cv2.imshow('Video', frame)

        return self.matches, frame
    


    # # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break





# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)


# known_faces_dir = "known_faces"
# unknown_faces_dir = "unknown_faces"
# tolerance = .6
# frame_thickness = 3
# font_thickness = 2
# model = "cnn" #hog
# process_this_frame = True

# print('loading known faces')
# known_faces = []
# known_names = []


# for name in os.listdir(known_faces_dir):
#     for filename in os.listdir(f"{known_faces_dir}/{name}"):
#         print(filename)
#         image = face_recognition.load_image_file(f"{known_faces_dir}/{name}/{filename}")
#         encoding = face_recognition.face_encodings(image)[0]
#         known_faces.append(encoding)
#         known_names.append(name)

# print('process uknown')
# for filename in os.listdir(unknown_faces_dir):
#     print(filename)
#     image = face_recognition.load_image_file(f"{unknown_faces_dir}/{filename}")
#     encodings = face_recognition.face_encodings(image)[0]
#     image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

if __name__== '__main__':

    vid = Video()

    vid.load_faces()

    while True:

        vid.check_faces()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # # Grab a single frame of video
    # ret, frame = video_capture.read()

    # # Only process every other frame of video to save time
    # if process_this_frame:
    #     # Resize frame of video to 1/4 size for faster face recognition processing
    #     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    #     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    #     rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
    #     # Find all the faces and face encodings in the current frame of video
    #     face_locations = face_recognition.face_locations(rgb_small_frame)
    #     face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    #     face_names = []
    #     for face_encoding in face_encodings:
    #         # See if the face is a match for the known face(s)
    #         matches = face_recognition.compare_faces(known_faces, face_encoding)
    #         name = "Unknown"

    #         # # If a match was found in known_face_encodings, just use the first one.
    #         if True in matches:
    #             first_match_index = matches.index(True)
    #             name = known_names[first_match_index]

    #         # Or instead, use the known face with the smallest distance to the new face
    #         # face_distances = face_recognition.face_distance(known_faces, face_encoding)
    #         # best_match_index = np.argmin(face_distances)
    #         # if matches[best_match_index]:
    #         #     name = known_names[best_match_index]

    #         face_names.append(name)

    # process_this_frame = not process_this_frame


    # # Display the results
    # for (top, right, bottom, left), name in zip(face_locations, face_names):
    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    #     top *= 4
    #     right *= 4
    #     bottom *= 4
    #     left *= 4

    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, bottom), (right, bottom+35), (0, 0, 255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(frame, name, (left + 6, bottom +29), font, 1.0, (255, 255, 255), 1)
    #     print(name)

    # # Display the resulting image
    # cv2.imshow('Video', frame)

    # # Hit 'q' on the keyboard to quit!
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release handle to the webcam
    vid.video_capture.release()
    cv2.destroyAllWindows()
    