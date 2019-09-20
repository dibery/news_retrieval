# Download historical exchange rate data from Taiwan Futures Exchange (TFE)
# Usage: bash $0
# Input: None
# Output: "yyyy mm dd rate", ONLY today's exchange rate, separated by a blank
# Author: Po-Chuan Chien

curl -s https://www.taifex.com.tw/cht/3/dailyFXRate | 
	grep -A1 '	*<td align="center" bg' | tail -20 | html2text |
	sed -n '1h;4{H;g;s/\(\/\|\n\)/ /g;s/ 0/ /gp;q}'
