#!/usr/bin/env bash
# POWERED BY RINTOD.DEV
RED='\033[0;31m'
GREEN='\e[32m'
BLUE='\e[34m'
WHITE='\033[0m'

header(){
cat <<EOF

APPLE VALID EMAIL
CODED BY RINTOD.DEV

FOR MORE: https://www.rintod.dev/

EOF
}
check(){
    cr=$(curl -s 'http://api.rintod.dev/valid/apple' -d '{"email":"'$email'"}')
    if [[ $cr =~ "LIVE" ]]; then
        echo -e "[$date][$2/$total] ${GREEN}$email${WHITE}"
        echo $email >> LIVE.txt
    elif [[ $cr =~ "DIE" ]]; then
        echo -e "[$date][$2/$total] ${RED}$email${WHITE}"
        echo $email >> DIE.txt
    else
        echo -e "[$date][$2/$total] ${BLUE}$email${WHITE}"
        echo $email >> UNCHECK.txt
    fi
}
header

read -p "[?] Mail List : " l
if [[ ! -f $l ]]; then
    echo "[-] File $l Not Exist"
    exit 1
fi

read -p "[?] Threads : " t

read -p "[?] Delay : " d

echo
echo -e "[!] Mail Loaded : ${BLUE}$(cat $l | wc -l)${WHITE}"
echo -e "[!] Threads     : ${BLUE}$t${WHITE}"
echo -e "[!] Delay       : ${BLUE}$d sec${WHITE}"
echo 
echo -e "[+] Start Check ...\n"

pp=1
IFS=$'\r\n'
for email in $(cat $l); do
   tt=$(expr $pp % $t)
   if [[ $tt == 0 && $pp > 0 ]]; then
       sleep $d
   fi
   date=$(date '+%H:%M:%S')
   total=$(cat $l | wc -l)
   check $email $pp &
   pp=$[$pp+1]
done
wait
