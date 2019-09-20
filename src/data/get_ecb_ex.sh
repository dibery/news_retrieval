# Download historical exchange rate data from European Central Bank (ECB) website
# Usage: bash $0
# Input: None
# Output: "yyyy mm dd rate", one day per line, separated by a blank
# Author: Po-Chuan Chien

curl -s https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.en.html | grep chartData.push | tr -c [0-9.\\n] ' ' | awk '{print $2, $3 + 1, $4, $5}' 
