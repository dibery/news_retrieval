# Extract all English news from Refinitiv dataset (gzipped json)
# Usage: bash $0
# Author: Po-Chuan Chien

IFS=$'\n'

for month in 2018-{01..12} 2019-{01..08}
do
	for i in `ls /tmp2/esun_2019/E.Sun_AI_report/Refinitiv\ 試用資料/news/${month:0:4}/$month/*`
	do
		for j in $i
		do
			zcat $j | jq -c '[.Items[]|select(.data.language == "en" and .data.body != "")]' > news_text/json/`basename $j .${j##*.}`.json &
			zcat $j | jq -c '.Items[]|select(.data.language == "en" and .data.body != "")|.data.body' > news_text/text/`basename $j .${j##*.}` &
			sleep .5
		done
	done
done

wait
