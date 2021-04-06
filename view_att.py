import csv
import sys

AVG_BASED_ON_ACTUAL = True # Either base average on actual results or predicted results

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: " + sys.argv[0] + " [attention.csv file]")
        exit(0)
   
    att_vec_avg = {}
    samples_count = {}

    with open(sys.argv[1]) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for idx, row in enumerate(reader):
            if idx != 0:  # Skip header
                actual = row.pop(0)
                predicted = row.pop(0)
                
                if AVG_BASED_ON_ACTUAL:
                    index = actual
                else:
                    index = predicted
                
                if index in att_vec_avg:  #Means also in sample count
                    samples_count[index] += 1
                    print(row)
                    att_vec_avg[index] = [(float(x) + float(y)) for (x,y) in zip(att_vec_avg[index], row)] # Sum element wise in list
                    
                else:
                    att_vec_avg[index] = row
                    samples_count[index] = 1
        
        for index in samples_count:
            att_vec_avg[index] = [float(x) / samples_count[index] for x in att_vec_avg[index]]  # Compute average
            print ("Penalty Class:", index)
            print ("Attention Vector:", att_vec_avg[index])            
        

                

