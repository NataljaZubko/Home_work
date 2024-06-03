 #!/bin/bash

	 FILE_LIST=$(ls -p /opt/220424-ptm | grep -v /)
 for FILE in $FILE_LIST
 do
    if [[ "$FILE" == *.sh ]]; then
        chmod +x "/opt/220424-ptm/$FILE"
        echo "Добавлены права на исполнение для файла: $FILE"
    fi
 done
 echo "Права на исполнение успешно добавлены!"

