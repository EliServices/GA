#tput civis #Hide cursor, unhide with tput cvvis
clear
sleep 0.1
printf "               \e[91mStartwagen-Assistent\e[0m\n"
printf " \e[93mFlugzeuge im Landeanflug (10 - 150m AGL):\e[0m\n"
printf "     Initialisiere...\n"
printf "     Initialisiere...\n"
printf "     Initialisiere...\n"
printf "\n"
printf " \e[92mFlugzeuge in der Platzrunde (Unter 400m AGL):\e[0m\n"
printf "     Initialisiere...\n"
printf "     Initialisiere...\n"
printf "     Initialisiere...\n"
printf "Muss landen,03" > one.tmp
printf "Platzrunde ,03" > two.tmp
sleep 1

while [ true ]
do

printf "\033[H"
inp=$(python bashsupply.py < one.tmp)
printf "\033[2B"
printf "\033[K"   # delete till end of line
printf "\033[1B"  # move cursor one line down
printf "\033[K"   # delete till end of line
printf "\033[1B"  # move cursor one line down
printf "\033[K"   # delete till end of line
printf "\033[1A"  # move cursor one line up
printf "\033[1A"  # move cursor one line up
printf "${inp}"

printf "\033[H"
inp=$(python bashsupply.py < two.tmp)
printf "\033[7B"
printf "\033[K"   # delete till end of line
printf "\033[1B"  # move cursor one line down
printf "\033[K"   # delete till end of line
printf "\033[1B"  # move cursor one line down
printf "\033[K"   # delete till end of line
printf "\033[1A"  # move cursor one line up
printf "\033[1A"  # move cursor one line up
printf "${inp}"

#tput civis #Hide cursor, unhide with tput cvvis
sleep 2
done

#inp="     M1  ASK-21     100m%s\n     M1  ASK-21     100m%s\n     M1  ASK-21     100m%s\n"
