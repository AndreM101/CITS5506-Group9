test = $(arp)
echo $test
if [[ $test == '' ]]; then
	echo 'not empty'
fi
