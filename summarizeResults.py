import os
import sys
import json
import csv
import numpy as np

# Summarize results from models. Outputs data to final_results.csv.

if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print ("Format: " + sys.argv[0] + ' [Path to Models Folder (i.e. models/YMJA)]')
        exit(0)
    else:
        model = sys.argv[1]

    prev_model = ""

    with open("final_results.csv", 'w') as output_file:
        output_file.write("model,val_acc_mean,val_acc_std,val_recall_mean,val_recall_std,val_precision_mean,val_precision_std,val_f1_mean,val_f1_std\n")

        for subdir, dirs, files in os.walk(sys.argv[1]):
            for file in files:
                if file == "summary.csv" and "fold_" in subdir:
                    if prev_model != subdir.split('/')[2]:


                        if prev_model != "":
                            val_acc_mean_avg = round(np.array(val_acc_mean).astype(np.float).mean() * 100, 2)
                            val_acc_std_avg = round(np.array(val_acc_std).astype(np.float).mean() * 100, 2)
                            val_recall_mean_avg = round(np.array(val_recall_mean).mean() * 100, 2)
                            val_recall_std_avg = round(np.array(val_recall_std).mean() * 100, 2)
                            val_prec_mean_avg = round(np.array(val_precision_mean).mean() * 100, 2)
                            val_prec_std_avg = round(np.array(val_precision_std).mean() * 100, 2)
                            val_f1_mean_avg = round(np.array(val_f1_mean).mean() * 100, 2)
                            val_f1_std_avg = round(np.array(val_f1_std).mean()*100, 2)
                            print("Val Acc: " + str(val_acc_mean_avg)+ "% +/- "+ str(val_acc_std_avg) + "%")
                            print("Val Recall: " + str(val_recall_mean_avg) + "% +/- "+ str(val_recall_std_avg) + "%")
                            print("Val Precision: " + str(val_prec_mean_avg) + "% +/- "+ str(val_prec_std_avg) + "%")
                            print ("Val F1: " + str(val_f1_mean_avg) + "% +/- " + str(val_f1_std_avg) + "%")
                            output_file.write(prev_model + "," + str(val_acc_mean_avg) + "," + str(val_acc_std_avg) + "," +str(val_recall_mean_avg) + "," + str(val_recall_std_avg) + "," +str(val_prec_mean_avg) + "," + str(val_prec_std_avg) + "," +str(val_f1_mean_avg) + "," + str(val_f1_std_avg) + "\n")


                        val_acc_mean = []
                        val_acc_std = []
                        val_recall_mean = []
                        val_recall_std = []
                        val_precision_mean = []
                        val_precision_std = []
                        val_f1_mean = []
                        val_f1_std = []


                        print("")
                        print ("Model: " + subdir.split('/')[2])
                        prev_model = subdir.split('/')[2]

                    with open(os.path.join(subdir, file)) as summary:
                        reader = csv.reader(summary, delimiter=',')
                        val_acc = []
                        val_recall = []
                        val_precision = []
                        val_f1 = []
                        for idx, row in enumerate(reader):
                            if (idx == 0):
                                val_acc_ind = row.index("val_acc")
                                val_recall_ind = row.index("val_recall_m")
                                val_precision_ind = row.index("val_precision_m")
                                val_f1_ind = row.index("val_f1_m")
                            else:
                                val_acc.append(row[val_acc_ind])
                                val_recall.append(row[val_recall_ind])
                                val_precision.append(row[val_precision_ind])
                                val_f1.append(row[val_f1_ind])

                        val_acc_mean.append(np.array(val_acc).astype(np.float).mean())
                        val_acc_std.append(np.array(val_acc).astype(np.float).std())
                        val_recall_mean.append(np.array(val_recall).astype(np.float).mean())
                        val_recall_std.append(np.array(val_recall).astype(np.float).std())
                        val_precision_mean.append(np.array(val_precision).astype(np.float).mean())
                        val_precision_std.append(np.array(val_precision).astype(np.float).std())
                        val_f1_mean.append(np.array(val_f1).astype(np.float).mean())
                        val_f1_std.append(np.array(val_f1).astype(np.float).std())
        
        val_acc_mean_avg = round(np.array(val_acc_mean).astype(np.float).mean() * 100, 2)
        val_acc_std_avg = round(np.array(val_acc_std).astype(np.float).mean() * 100, 2)
        val_recall_mean_avg = round(np.array(val_recall_mean).mean() * 100, 2)
        val_recall_std_avg = round(np.array(val_recall_std).mean() * 100, 2)
        val_prec_mean_avg = round(np.array(val_precision_mean).mean() * 100, 2)
        val_prec_std_avg = round(np.array(val_precision_std).mean() * 100, 2)
        val_f1_mean_avg = round(np.array(val_f1_mean).mean() * 100, 2)
        val_f1_std_avg = round(np.array(val_f1_std).mean()*100, 2)
        print("Val Acc: " + str(val_acc_mean_avg)+ "% +/- "+ str(val_acc_std_avg) + "%")
        print("Val Recall: " + str(val_recall_mean_avg) + "% +/- "+ str(val_recall_std_avg) + "%")
        print("Val Precision: " + str(val_prec_mean_avg) + "% +/- "+ str(val_prec_std_avg) + "%")
        print ("Val F1: " + str(val_f1_mean_avg) + "% +/- " + str(val_f1_std_avg) + "%")
        output_file.write(prev_model + "," + str(val_acc_mean_avg) + "," + str(val_acc_std_avg) + "," +str(val_recall_mean_avg) + "," + str(val_recall_std_avg) + "," +str(val_prec_mean_avg) + "," + str(val_prec_std_avg) + "," +str(val_f1_mean_avg) + "," + str(val_f1_std_avg))




            
