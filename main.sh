DATAPATH="/Users/john-paulroadman/boot.dev/staticsite/"
IMAGE_SOURCE=$DATAPATH"static"
CONTENT_SOURCE=$DATAPATH"content"
DESTIN=$DATAPATH"doc"
BASEPATH="/doc"


#if [[ -z "$1" ]]; then
#	echo "Usage: main.sh [source_path] [destination_path]"
#	exit 1 
#fi
#if [[ -z "$2" ]]; then
#	echo "Usage: main.sh [source_path] [destination_path]"
#	exit 1 
#fi

python3 src/main.py "$IMAGE_SOURCE" "$DESTIN" "$CONTENT_SOURCE" "$BASEPATH"
