count="1"

file=$1
while read -r line; do

echo count $count

input_filename=$(echo $line | awk '{print $1}')

echo $input_filename

sh SubmitToCondor_nano.sh output_${1}_${count} MuonJet ${input_filename} /eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_378981_381152_Golden.json

count=$[$count+1]

done < $file

exit 0
