#!/bin/bash
java -Xmx1G -Xms512M -jar server.jar nogui


java -Xmx4G -Xms2G \
-Djava.net.preferIPv4Stack=true \
-Dhttps.protocols=TLSv1.2,TLSv1.3 \
-Djdk.tls.client.protocols=TLSv1.2,TLSv1.3 \
-Dsun.net.client.defaultConnectTimeout=10000 \
-Dsun.net.client.defaultReadTimeout=10000 \
-jar server.jar nogui
