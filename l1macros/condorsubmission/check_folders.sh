for i in $(seq 1 159);
do
    echo $i
    cat output_Run2024E_Muon1.txt_$i/log/scriptcondor_0.err
done
