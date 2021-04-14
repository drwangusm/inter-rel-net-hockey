import cv2
import json
import os.path

GAMES_MP4_PATH = "/usr/local/data02/dpdataset/hockey_mp4/"
CLIPS_PATH = "/usr/local/data02/dpdataset/DP17_PostProcessing/YMJA/"
JSON_PATH = "/usr/local/data02/dpdataset/DP17_PostProcessing/json/2021-03-20-penalties.json"
MINUS_OFFSET = 1        # clip start time = json start time - MINUS_OFFSET
PLUS_OFFSET = 2         # clip end time = json end time + PLUS_OFFSET

def create_folder(folder_name:str):
    path = os.path.join(CLIPS_PATH, folder_name)
    if not os.path.isdir(path):
        print(f'Creating folder: {path}')
        os.makedirs(path)

classes = ["Cross_Checking", "Hi_sticking", "Holding", "Hooking", "Interference",
"No_penalty", "Roughing", "Slashing", "Tripping"]

for class_ in classes:
    create_folder(class_)

TrippingIDs = []
HookingIDs = []
SlashingIDs = []
RoughingIDs = []
InterferenceIDs = []
HoldingIDs = []
Cross_CheckingIDs = []
Hi_stickingIDs = []
No_penaltyIDs = []



with open(JSON_PATH) as json_file:
	dataset = json.load(json_file)

for pen in dataset["penalties"]:
    if pen["label"] == "Tripping":
        TrippingIDs.append(pen["ID"])
    elif pen["label"] == "Hooking":
        HookingIDs.append(pen["ID"])
    elif pen["label"] == "Slashing":
        SlashingIDs.append(pen["ID"])
    elif pen["label"] == "Roughing":
        RoughingIDs.append(pen["ID"])
    elif pen["label"] == "Interference":
        InterferenceIDs.append(pen["ID"])
    elif pen["label"] == "Holding":
        HoldingIDs.append(pen["ID"])
    elif pen["label"] == "Cross-checking":
        Cross_CheckingIDs.append(pen["ID"])
    elif pen["label"] == "Hi sticking":
        Hi_stickingIDs.append(pen["ID"])
    elif pen["label"] == "No penalty":
        No_penaltyIDs.append(pen["ID"])

print("#Tripping",len(TrippingIDs))
print("#Hooking",len(HookingIDs))
print("#Slashing",len(SlashingIDs))
print("#Roughing",len(RoughingIDs))
print("#Interference",len(InterferenceIDs))
print("#Holding",len(HoldingIDs))
print("#Cross_Checking",len(Cross_CheckingIDs))
print("#Hi_sticking",len(Hi_stickingIDs))
print("#No_penalty",len(No_penaltyIDs))


for pen in dataset["penalties"]:
    if(os.path.isfile(GAMES_MP4_PATH + pen["gamename"] + ".mp4")):
        clip_ID = pen['ID']
        start_time = pen['start']
        end_time = pen['end']

        start_time_processed = int(start_time.split(':')[0])*3600+int(start_time.split(':')[1])*60+int(start_time.split(':')[2]) - MINUS_OFFSET
        end_time_processed = int(end_time.split(':')[0])*3600+int(end_time.split(':')[1])*60+int(end_time.split(':')[2]) + PLUS_OFFSET        
        #Load Video
        cap = cv2.VideoCapture(GAMES_MP4_PATH + pen["gamename"] + ".mp4")
        
        #Get FrameRate and size
        fps = cap.get(cv2.CAP_PROP_FPS)
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
        
        #Get start and end Frames number
        startFrame = int(start_time_processed * fps)
        endFrame = int(end_time_processed * fps)
        
        #Create output
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        if pen["label"] == "Cross-checking":
            pen_class = "Cross_Checking"
        elif pen["label"] == "Hi sticking":
            pen_class = "Hi_sticking"
        elif pen["label"] == "No penalty":
            pen_class = "No_penalty"
        else:
            pen_class = pen["label"]

        out = cv2.VideoWriter(CLIPS_PATH+pen_class+'/_'+pen["gamename"]+str(clip_ID)+".mp4",fourcc, fps, (width,height))
        
        #set frame 
        cap.set(cv2.CAP_PROP_POS_FRAMES,startFrame)
        
        #Copy over frame from cap to out
        for _ in range(endFrame - startFrame):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        
        print("%d %d %d"%(clip_ID,start_time_processed,end_time_processed))
        
        #Release videos
        cap.release()
        out.release()

cv2.destroyAllWindows()