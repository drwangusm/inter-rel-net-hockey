#!/bin/bash
#python3 src/run_protocol.py IRN_joint_stream_att_cs3 configs/NTU-V1/IRN_joint_stream_att_cs.cfg NTU -f cross_subject -n 3
#python3 src/run_protocol.py IRN_temporal_stream_att_cs3 configs/NTU-V1/IRN_temporal_stream_att_cs.cfg NTU -f cross_subject -n 3
python3 src/run_protocol.py IRN_two_stream_att_cs3 configs/NTU-V1/IRN_two_stream_att_cs.cfg NTU -F middle -f cross_subject -n 3
python3 src/run_protocol.py IRN_two_stream_att_avg_cs3 configs/NTU-V1/IRN_two_stream_att_avg_cs.cfg NTU -F middle -f cross_subject -n 3

#python3 src/run_protocol.py IRN_joint_stream_att_no_rel_cs3 configs/NTU-V1/IRN_joint_stream_att_no_rel_cs.cfg NTU -f cross_subject -n 3
#python3 src/run_protocol.py IRN_temporal_stream_att_no_rel_cs3 configs/NTU-V1/IRN_temporal_stream_att_no_rel_cs.cfg NTU -f cross_subject -n 3
python3 src/run_protocol.py IRN_two_stream_att_no_rel_cs3 configs/NTU-V1/IRN_two_stream_att_no_rel_cs.cfg NTU -F middle -f cross_subject -n 3
python3 src/run_protocol.py IRN_two_stream_att_no_rel_avg_cs3 configs/NTU-V1/IRN_two_stream_att_no_rel_avg_cs.cfg NTU -F middle -f cross_subject -n 3
