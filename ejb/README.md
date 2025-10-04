# JavaEE EJB Example Code

This is a small and very simple example for the people who wants to learn Java EE EJB technology. It covers EJB stateless session beans, JPA Entity beans, JMS Point-to-Point Message transport and CDI Interceptors.

The Code is very small, simple and lightweight with the aims helping developers to understand and Learn how EJBs work. 

In order to test the code, you have to import two Projects as Gradle Project in IDE:

`ejb`  
This Project contains the ejb, jms, jpa files. The jar file of this project must be included in ejb-client project.

`ejb-client`  
This Project provides a servlet that uses ejb Project jar file. You have to deploy the war file of this project in an application server. Giving firstname and lastname and submitting it, you will be able to persist the data and getting messages in server error log via jms. 

Before deploing the war file in application server you have to create JDBC Pool and JNDI Resource, for jms functionality you have to define JMS Messaging factory and JMS Resource.

JTA-Data-Source on Server must be named as **jdbc/ejb**

For more Information about how to create a jdbc pool and jndi resource under Glassfish application server  please refer to https://docs.oracle.com/cd/E19798-01/821-1752/beamk/index.html

JMS-Data-Source must have the following properties:  
destination **ejbQueue**  
destinationType **javax.jms.Queue**

JMS Connection factory must be named as **jms/__defaultConnectionFactory**  
JMS Queue **jms/ejbqueue**

For more Information about how to create a JMS Messaging Factory and Resource please refer to https://docs.oracle.com/cd/E19798-01/821-1751/giotd/index.html 

Don't forget to build the projects ebj and ejb-client respectively with:

`./gradlew clean build`

After configuring the application server, you have to start it and run the servlet in ejb-client project.

Enjoy it !
