#!/bin/bash

##NTU-V1 joint, no lstm, no fusion
python3 src/run_protocol.py final_joint_rel_ave_v1 configs/NTU-V1/final/final_joint_rel_ave.cfg NTU -n 5 -v 2
python3 src/run_protocol.py final_joint_rel_att_v1 configs/NTU-V1/final/final_joint_rel_att.cfg NTU -n 5 -v 2
python3 src/run_protocol.py final_joint_no_rel_ave_v1 configs/NTU-V1/final/final_joint_no_rel_ave.cfg NTU -n 5 -v 2
python3 src/run_protocol.py final_joint_no_rel_att_v1 configs/NTU-V1/final/final_joint_no_rel_att.cfg NTU -n 5 -v 2

##NTU-V1 temp, no lstm, no fusion
python3 src/run_protocol.py final_temp_rel_ave_v1 configs/NTU-V1/final/final_temp_rel_ave.cfg NTU -n 5 -v 2
python3 src/run_protocol.py final_temp_rel_att_v1 configs/NTU-V1/final/final_temp_rel_att.cfg NTU -n 5 -v 2
python3 src/run_protocol.py final_temp_no_rel_ave_v1 configs/NTU-V1/final/final_temp_no_rel_ave.cfg NTU -n 5 -v 2
python3 src/run_protocol.py final_temp_no_rel_att_v1 configs/NTU-V1/final/final_temp_no_rel_att.cfg NTU -n 5 -v 2

##NTU-V1 joint, lstm no fusion
python3 src/run_protocol.py final_joint_rel_ave_lstm_v1 configs/NTU-V1/final/lstm/final_joint_rel_ave_lstm.cfg NTU -n 5 -t -v 2
python3 src/run_protocol.py final_joint_rel_att_lstm_v1 configs/NTU-V1/final/lstm/final_joint_rel_att_lstm.cfg NTU -n 5 -t -v 2
python3 src/run_protocol.py final_joint_no_rel_ave_lstm_v1 configs/NTU-V1/final/lstm/final_joint_no_rel_ave_lstm.cfg NTU -n 5 -t -v 2
python3 src/run_protocol.py final_joint_no_rel_att_lstm_v1 configs/NTU-V1/final/lstm/final_joint_no_rel_att_lstm.cfg NTU -n 5 -t -v 2

##NTU-V1 temp, lstm no fusion
python3 src/run_protocol.py final_temp_rel_ave_lstm_v1 configs/NTU-V1/final/lstm/final_temp_rel_ave_lstm.cfg NTU -n 5 -t -v 2
python3 src/run_protocol.py final_temp_rel_att_lstm_v1 configs/NTU-V1/final/lstm/final_temp_rel_att_lstm.cfg NTU -n 5 -t -v 2
python3 src/run_protocol.py final_temp_no_rel_ave_lstm_v1 configs/NTU-V1/final/lstm/final_temp_no_rel_ave_lstm.cfg NTU -n 5 -t -v 2
python3 src/run_protocol.py final_temp_no_rel_att_lstm_v1 configs/NTU-V1/final/lstm/final_temp_no_rel_att_lstm.cfg NTU -n 5 -t -v 2

#NTU-V1 no lstm, fusion
python3 src/run_protocol.py IRN_final_rel_ave_before_v1 configs/NTU-V1/final/IRN_final_rel_ave_before.cfg NTU -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_rel_att_before_v1 configs/NTU-V1/final/IRN_final_rel_att_before.cfg NTU -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_ave_before_v1 configs/NTU-V1/final/IRN_final_no_rel_ave_before.cfg NTU -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_att_before_v1 configs/NTU-V1/final/IRN_final_no_rel_att_before.cfg NTU -F middle -n 5 -v 2

python3 src/run_protocol.py IRN_final_rel_ave_after_v1 configs/NTU-V1/final/IRN_final_rel_ave_after.cfg NTU -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_rel_att_after_v1 configs/NTU-V1/final/IRN_final_rel_att_after.cfg NTU -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_ave_after_v1 configs/NTU-V1/final/IRN_final_no_rel_ave_after.cfg NTU -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_att_after_v1 configs/NTU-V1/final/IRN_final_no_rel_att_after.cfg NTU -F middle -n 5 -v 2

#NTU-V1 lstm fusion
python3 src/run_protocol.py IRN_final_rel_ave_before_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_rel_ave_before_lstm.cfg NTU -t -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_rel_att_before_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_rel_att_before_lstm.cfg NTU -t -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_ave_before_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_no_rel_ave_before_lstm.cfg NTU -t -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_att_before_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_no_rel_att_before_lstm.cfg NTU -t -F middle -n 5 -v 2

python3 src/run_protocol.py IRN_final_rel_ave_after_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_rel_ave_after_lstm.cfg NTU -t -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_rel_att_after_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_rel_att_after_lstm.cfg NTU -t -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_ave_after_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_no_rel_ave_after_lstm.cfg NTU -t -F middle -n 5 -v 2
python3 src/run_protocol.py IRN_final_no_rel_att_after_lstm_v1 configs/NTU-V1/final/lstm/IRN_final_no_rel_att_after_lstm.cfg NTU -t -F middle -n 5 -v 2