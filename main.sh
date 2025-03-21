DATAPATH="/Users/john-paulroadman/boot.dev/staticsite/"
SOURCE=$DATAPATH"static"
DESTIN=$DATAPATH"public"

#if [[ -z "$1" ]]; then
#	echo "Usage: main.sh [source_path] [destination_path]"
#	exit 1 
#fi
#if [[ -z "$2" ]]; then
#	echo "Usage: main.sh [source_path] [destination_path]"
#	exit 1 
#fi

python3 src/main.py "$SOURCE" "$DESTIN"
