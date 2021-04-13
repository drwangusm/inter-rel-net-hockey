import os
import sys
import json

NUM_FRAMES = 64
FILTERED_POSES_DIR = "FilteredPoses/"
OUTPUT_DIR = "FinalFormatJson/"

if __name__ == "__main__":

    if(len(sys.argv) < 2 or (sys.argv[1] != "IRN" and sys.argv[1] != "Potion")):
        print("Must select format for dataset: ./" + sys.argv[0] + " [IRN | Potion]")
        exit(1)
    else:
        model = sys.argv[1]

    for subdir, dirs, files in os.walk(FILTERED_POSES_DIR):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(subdir, file)) as json_file:
                    frameData = json.load(json_file)

                    selectedFrames = []
                    print(file, len(frameData))
                    for i in range(NUM_FRAMES):
                        selectedFrame = (frameData[int(i/NUM_FRAMES * len(frameData))]) # Select even distribution of frames (might have some duplicates if under NUM_FRAMES)
                        
                        selectedFrames.append(selectedFrame)

                    if(model == "IRN"):
                        OUTPUT_DIR = "YMJA/"

                    penalty_class = subdir.split("/")[1]
                    output_directory = OUTPUT_DIR + penalty_class + "/"

                    # Create directories and output files
                    os.makedirs(os.path.dirname(output_directory), exist_ok=True)

                    with open(output_directory + file, 'w') as out_json_file:
                        json.dump(selectedFrames, out_json_file, indent=4)

        
