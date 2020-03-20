# xconsole
Open serial /dev/ttyUSB via Local | ssh | sol

## Install
	$git clone https://github.com/quanghuyen1301/xconsole.git
	$cd xconsole 
	$pip install .
## Open /dev/ttyUSB0 | FTAXMM1E
	$python -m xconsole ttyUSB0|FTAXMM1E [logfile]

## Open /dev/ttyUSB0 via ssh 
	$python -m xconsole <user@hostip> <password> ttyUSB0|FTAXMM1E [logfile]

## Open by SOL 
	$python -m xconsole <IP> <SOL>
