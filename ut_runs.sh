#!/bin/bash

##UT joint, no lstm, no fusion
python3 src/run_protocol.py final_joint_rel_ave_s1 configs/UT/set_1/final/final_joint_rel_ave.cfg UT-1 -n 5
python3 src/run_protocol.py final_joint_rel_ave_s2 configs/UT/set_2/final/final_joint_rel_ave.cfg UT-2 -n 5
python3 src/run_protocol.py final_joint_rel_att_s1 configs/UT/set_1/final/final_joint_rel_att.cfg UT-1 -n 5
python3 src/run_protocol.py final_joint_rel_att_s2 configs/UT/set_2/final/final_joint_rel_att.cfg UT-2 -n 5
python3 src/run_protocol.py final_joint_no_rel_ave_s1 configs/UT/set_1/final/final_joint_no_rel_ave.cfg UT-1 -n 5
python3 src/run_protocol.py final_joint_no_rel_ave_s2 configs/UT/set_2/final/final_joint_no_rel_ave.cfg UT-2 -n 5
python3 src/run_protocol.py final_joint_no_rel_att_s1 configs/UT/set_1/final/final_joint_no_rel_att.cfg UT-1 -n 5
python3 src/run_protocol.py final_joint_no_rel_att_s2 configs/UT/set_2/final/final_joint_no_rel_att.cfg UT-2 -n 5

##UT temp, no lstm, no fusion
python3 src/run_protocol.py final_temp_rel_ave_s1 configs/UT/set_1/final/final_temp_rel_ave.cfg UT-1 -n 5
python3 src/run_protocol.py final_temp_rel_ave_s2 configs/UT/set_2/final/final_temp_rel_ave.cfg UT-2 -n 5
python3 src/run_protocol.py final_temp_rel_att_s1 configs/UT/set_1/final/final_temp_rel_att.cfg UT-1 -n 5
python3 src/run_protocol.py final_temp_rel_att_s2 configs/UT/set_2/final/final_temp_rel_att.cfg UT-2 -n 5
python3 src/run_protocol.py final_temp_no_rel_ave_s1 configs/UT/set_1/final/final_temp_no_rel_ave.cfg UT-1 -n 5
python3 src/run_protocol.py final_temp_no_rel_ave_s2 configs/UT/set_2/final/final_temp_no_rel_ave.cfg UT-2 -n 5
python3 src/run_protocol.py final_temp_no_rel_att_s1 configs/UT/set_1/final/final_temp_no_rel_att.cfg UT-1 -n 5
python3 src/run_protocol.py final_temp_no_rel_att_s2 configs/UT/set_2/final/final_temp_no_rel_att.cfg UT-2 -n 5

#UT joint, lstm, no fusion
python3 src/run_protocol.py final_joint_rel_ave_lstm_s1 configs/UT/set_1/final/lstm/final_joint_rel_ave_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_joint_rel_ave_lstm_s2 configs/UT/set_2/final/lstm/final_joint_rel_ave_lstm.cfg UT-2 -n 5 -t
python3 src/run_protocol.py final_joint_rel_att_lstm_s1 configs/UT/set_1/final/lstm/final_joint_rel_att_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_joint_rel_att_lstm_s2 configs/UT/set_2/final/lstm/final_joint_rel_att_lstm.cfg UT-2 -n 5 -t
python3 src/run_protocol.py final_joint_no_rel_ave_lstm_s1 configs/UT/set_1/final/lstm/final_joint_no_rel_ave_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_joint_no_rel_ave_lstm_s2 configs/UT/set_2/final/lstm/final_joint_no_rel_ave_lstm.cfg UT-2 -n 5 -t
python3 src/run_protocol.py final_joint_no_rel_att_lstm_s1 configs/UT/set_1/final/lstm/final_joint_no_rel_att_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_joint_no_rel_att_lstm_s2 configs/UT/set_2/final/lstm/final_joint_no_rel_att_lstm.cfg UT-2 -n 5 -t

#UT temp, lstm, no fusion
python3 src/run_protocol.py final_temp_rel_ave_lstm_s1 configs/UT/set_1/final/lstm/final_temp_rel_ave_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_temp_rel_ave_lstm_s2 configs/UT/set_2/final/lstm/final_temp_rel_ave_lstm.cfg UT-2 -n 5 -t
python3 src/run_protocol.py final_temp_rel_att_lstm_s1 configs/UT/set_1/final/lstm/final_temp_rel_att_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_temp_rel_att_lstm_s2 configs/UT/set_2/final/lstm/final_temp_rel_att_lstm.cfg UT-2 -n 5 -t
python3 src/run_protocol.py final_temp_no_rel_ave_lstm_s1 configs/UT/set_1/final/lstm/final_temp_no_rel_ave_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_temp_no_rel_ave_lstm_s2 configs/UT/set_2/final/lstm/final_temp_no_rel_ave_lstm.cfg UT-2 -n 5 -t
python3 src/run_protocol.py final_temp_no_rel_att_lstm_s1 configs/UT/set_1/final/lstm/final_temp_no_rel_att_lstm.cfg UT-1 -n 5 -t
python3 src/run_protocol.py final_temp_no_rel_att_lstm_s2 configs/UT/set_2/final/lstm/final_temp_no_rel_att_lstm.cfg UT-2 -n 5 -t

#UT two_stream
python3 src/run_protocol.py IRN_final_rel_ave_after_s1 configs/UT/set_1/final/IRN_final_rel_ave_after.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_ave_after_s2 configs/UT/set_2/final/IRN_final_rel_ave_after.cfg UT-2 -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_after_s1 configs/UT/set_1/final/IRN_final_rel_att_after.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_after_s2 configs/UT/set_2/final/IRN_final_rel_att_after.cfg UT-2 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_after_s1 configs/UT/set_1/final/IRN_final_no_rel_ave_after.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_after_s2 configs/UT/set_2/final/IRN_final_no_rel_ave_after.cfg UT-2 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_after_s1 configs/UT/set_1/final/IRN_final_no_rel_att_after.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_after_s2 configs/UT/set_2/final/IRN_final_no_rel_att_after.cfg UT-2 -F middle -n 5

python3 src/run_protocol.py IRN_final_rel_ave_before_s1 configs/UT/set_1/final/IRN_final_rel_ave_before.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_ave_before_s2 configs/UT/set_2/final/IRN_final_rel_ave_before.cfg UT-2 -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_before_s1 configs/UT/set_1/final/IRN_final_rel_att_before.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_before_s2 configs/UT/set_2/final/IRN_final_rel_att_before.cfg UT-2 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_before_s1 configs/UT/set_1/final/IRN_final_no_rel_ave_before.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_before_s2 configs/UT/set_2/final/IRN_final_no_rel_ave_before.cfg UT-2 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_before_s1 configs/UT/set_1/final/IRN_final_no_rel_att_before.cfg UT-1 -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_before_s2 configs/UT/set_2/final/IRN_final_no_rel_att_before.cfg UT-2 -F middle -n 5

##UT two_stream
python3 src/run_protocol.py IRN_final_rel_ave_before_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_rel_ave_before_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_ave_before_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_rel_ave_before_lstm.cfg UT-2 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_before_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_rel_att_before_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_before_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_rel_att_before_lstm.cfg UT-2 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_before_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_no_rel_ave_before_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_before_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_no_rel_ave_before_lstm.cfg UT-2 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_before_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_no_rel_att_before_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_before_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_no_rel_att_before_lstm.cfg UT-2 -t -F middle -n 5

python3 src/run_protocol.py IRN_final_rel_ave_after_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_rel_ave_after_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_ave_after_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_rel_ave_after_lstm.cfg UT-2 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_after_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_rel_att_after_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_after_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_rel_att_after_lstm.cfg UT-2 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_after_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_no_rel_ave_after_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_after_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_no_rel_ave_after_lstm.cfg UT-2 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_after_lstm_s1 configs/UT/set_1/final/lstm/IRN_final_no_rel_att_after_lstm.cfg UT-1 -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_after_lstm_s2 configs/UT/set_2/final/lstm/IRN_final_no_rel_att_after_lstm.cfg UT-2 -t -F middle -n 5