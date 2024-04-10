#!/bin/bash

##SBU joint, no lstm, no fusion
# python3 src/run_protocol.py final_joint_rel_ave configs/SBU/final/final_joint_rel_ave.cfg SBU -n 5
# python3 src/run_protocol.py final_joint_rel_att configs/SBU/final/final_joint_rel_att.cfg SBU -n 5
# python3 src/run_protocol.py final_joint_no_rel_ave configs/SBU/final/final_joint_no_rel_ave.cfg SBU -n 5
# python3 src/run_protocol.py final_joint_no_rel_att configs/SBU/final/final_joint_no_rel_att.cfg SBU -n 5

##SBU temp, no lstm, no fusion
# python3 src/run_protocol.py final_temp_rel_ave configs/SBU/final/final_temp_rel_ave.cfg SBU -n 5
# python3 src/run_protocol.py final_temp_rel_att configs/SBU/final/final_temp_rel_att.cfg SBU -n 5
# python3 src/run_protocol.py final_temp_no_rel_ave configs/SBU/final/final_temp_no_rel_ave.cfg SBU -n 5
# python3 src/run_protocol.py final_temp_no_rel_att configs/SBU/final/final_temp_no_rel_att.cfg SBU -n 5

##SBU joint, lstm no fusion
# python3 src/run_protocol.py final_joint_rel_ave_lstm configs/SBU/final/lstm/final_joint_rel_ave_lstm.cfg SBU -n 5 -t
python3 src/run_protocol.py final_joint_rel_att_lstm configs/SBU/final/lstm/final_joint_rel_att_lstm.cfg SBU -n 5 -t
# python3 src/run_protocol.py final_joint_no_rel_ave_lstm configs/SBU/final/lstm/final_joint_no_rel_ave_lstm.cfg SBU -n 5 -t
python3 src/run_protocol.py final_joint_no_rel_att_lstm configs/SBU/final/lstm/final_joint_no_rel_att_lstm.cfg SBU -n 5 -t

##SBU temp, lstm no fusion
# python3 src/run_protocol.py final_temp_rel_ave_lstm configs/SBU/final/lstm/final_temp_rel_ave_lstm.cfg SBU -n 5 -t
python3 src/run_protocol.py final_temp_rel_att_lstm configs/SBU/final/lstm/final_temp_rel_att_lstm.cfg SBU -n 5 -t
# python3 src/run_protocol.py final_temp_no_rel_ave_lstm configs/SBU/final/lstm/final_temp_no_rel_ave_lstm.cfg SBU -n 5 -t
python3 src/run_protocol.py final_temp_no_rel_att_lstm configs/SBU/final/lstm/final_temp_no_rel_att_lstm.cfg SBU -n 5 -t

#SBU no lstm, fusion
# python3 src/run_protocol.py IRN_final_rel_ave_before configs/SBU/final/IRN_final_rel_ave_before.cfg SBU -F middle -n 5
# python3 src/run_protocol.py IRN_final_rel_att_before configs/SBU/final/IRN_final_rel_att_before.cfg SBU -F middle -n 5
# python3 src/run_protocol.py IRN_final_no_rel_ave_before configs/SBU/final/IRN_final_no_rel_ave_before.cfg SBU -F middle -n 5
# python3 src/run_protocol.py IRN_final_no_rel_att_before configs/SBU/final/IRN_final_no_rel_att_before.cfg SBU -F middle -n 5

# python3 src/run_protocol.py IRN_final_rel_ave_after configs/SBU/final/IRN_final_rel_ave_after.cfg SBU -F middle -n 5
# python3 src/run_protocol.py IRN_final_rel_att_after configs/SBU/final/IRN_final_rel_att_after.cfg SBU -F middle -n 5
# python3 src/run_protocol.py IRN_final_no_rel_ave_after configs/SBU/final/IRN_final_no_rel_ave_after.cfg SBU -F middle -n 5
# python3 src/run_protocol.py IRN_final_no_rel_att_after configs/SBU/final/IRN_final_no_rel_att_after.cfg SBU -F middle -n 5

#SBU lstm fusion
python3 src/run_protocol.py IRN_final_rel_ave_before_lstm configs/SBU/final/lstm/IRN_final_rel_ave_before_lstm.cfg SBU -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_before_lstm configs/SBU/final/lstm/IRN_final_rel_att_before_lstm.cfg SBU -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_before_lstm configs/SBU/final/lstm/IRN_final_no_rel_ave_before_lstm.cfg SBU -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_before_lstm configs/SBU/final/lstm/IRN_final_no_rel_att_before_lstm.cfg SBU -t -F middle -n 5

python3 src/run_protocol.py IRN_final_rel_ave_after_lstm configs/SBU/final/lstm/IRN_final_rel_ave_after_lstm.cfg SBU -t -F middle -n 5
python3 src/run_protocol.py IRN_final_rel_att_after_lstm configs/SBU/final/lstm/IRN_final_rel_att_after_lstm.cfg SBU -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_ave_after_lstm configs/SBU/final/lstm/IRN_final_no_rel_ave_after_lstm.cfg SBU -t -F middle -n 5
python3 src/run_protocol.py IRN_final_no_rel_att_after_lstm configs/SBU/final/lstm/IRN_final_no_rel_att_after_lstm.cfg SBU -t -F middle -n 5
