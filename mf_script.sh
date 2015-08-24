

maxfilter -f p_01_data.fif -o p_02_data_raw_tsss1.fif -st 30 -corr 0.95 -autobad on -movecomp -hp p_01_data_tsss_hp.txt -v > p_01_data_tsss.log

maxfilter -f p_01_data-1.fif -o p_02_data_raw_tsss-1.fif -st 30 -corr 0.95 -autobad on -movecomp -hp p_01_data_tsss_hp-1.txt -v > p_01_data_tsss-1.log

maxfilter -f p_01_data-2.fif -o p_02_data_raw_tsss-2.fif -st 30 -corr 0.95 -autobad on -movecomp -hp p_01_data_tsss_hp-2.txt -v > p_01_data_tsss-2.log
