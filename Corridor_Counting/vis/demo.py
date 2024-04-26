import cv2
import json

if __name__ == '__main__':
    data = json.load(open('visual_info.json', 'r'))
    
    u_id = data['u_id']
    u_id_label = f"ID: {u_id}"
    
    text = []

    for cam, info in data['data'].items():
        print(f"writing video {cam}")
        cam_id = int(cam[-3:])
        start_frame = int(info['start_frame'])
        mov_id = int(info['movement'])
        mov_frame = int(info['frame_assigned'])
        boxes = info['bounding_boxes']
        

        # Input video reader
        raw_video = cv2.VideoCapture(f'../../AICITY2022_Track1_TAG/datasets/Dataset_A/validation/S05/{cam}/vdo.avi')

        # Set up output video writer
        fps = 10
        width = int(raw_video.get(3))
        height = int(raw_video.get(4))
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(f'{cam}_annotated.mp4', codec, fps, (width, height))


        i = 0
        box_color = (0, 0, 255) # red
        matched = False
        while raw_video.isOpened():
            ret, frame = raw_video.read()
            if not ret:
                break
            
            # Skip ahead to the frame when the vehicle appears
            if i < start_frame:
                i += 1
                out_video.write(frame)
                continue
            
            # Once vehicle disappears from view, skip to end of video
            if len(boxes) <= i - start_frame:
                i += 1
                out_video.write(frame)
                continue
            
            # Change colors when movement is assigned
            if i == mov_frame:
                box_color = (255, 0, 0) # blue
                text.append(f"Cam {cam_id}: MOV {mov_id}")
                matched = True

            # Draw bounding box
            box = boxes[i - start_frame]
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            
            # Write info near box
            
            # id on top left corner
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            text_color = (255, 255, 255) # white
            bg_color = (0, 0, 255) # red
            
            text_size, _ = cv2.getTextSize(u_id_label, font, font_scale, 2)
            
            pos = (x1, y1)
            box_tl = (pos[0] - 2, pos[1] - text_size[1] - 2)
            box_br = (pos[0] + text_size[0] + 2, y1) 
            
            cv2.rectangle(frame, box_tl, box_br, bg_color, -1)
            cv2.putText(frame, u_id_label, pos, font, font_scale, text_color, 2)
            
            # cam, movements on bottom left corner
            text_color = (0, 0, 255) # red
            pos = (x1, y2 - 1)
            for j, line in enumerate(text):
                if (j == len(text) - 1) and matched:
                    text_color = (255, 0, 0) # blue
                    
                text_size, _ = cv2.getTextSize(line, font, font_scale, 2)
                pos = (pos[0], pos[1] + text_size[1] + 5)
                cv2.putText(frame, line, pos, font, font_scale, text_color, 2)
            
            out_video.write(frame)

            i += 1

        raw_video.release()
        out_video.release()

    cv2.destroyAllWindows()

