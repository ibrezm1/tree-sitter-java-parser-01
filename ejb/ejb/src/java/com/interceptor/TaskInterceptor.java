package com.interceptor;

import com.jpa.Customer;

import java.lang.reflect.Method;

import javax.annotation.Resource;
import javax.interceptor.AroundInvoke;
import javax.interceptor.InvocationContext;
import javax.jms.*;

public class TaskInterceptor {
    
    @Resource(name="jms/__defaultConnectionFactory")
    private ConnectionFactory connectionFactory;
    
    @Resource(mappedName = "jms/ejbqueue")
    private Queue queue;
    
    public TaskInterceptor() {
    }
    
    @AroundInvoke
    public Object createTaskMessage(InvocationContext ic) {
        Object returnValue = null;
        try {
            Method method = ic.getMethod();
            returnValue = ic.proceed();
            Customer customer = ((Customer)returnValue);
            Connection connection = connectionFactory.createConnection();
            Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);
            MessageProducer producer = session.createProducer(queue);

//            Message message = session.createMessage();
//            message.setStringProperty("operation", method.getName());
//            message.setStringProperty("customer", customer.getFirstName() + " " + customer.getLastName() + " - " + customer.getId());
//            producer.send(message);

            ObjectMessage objectMessage = session.createObjectMessage();
            objectMessage.setStringProperty("operation", method.getName());
            objectMessage.setObject(customer);
            producer.send(objectMessage);

        } catch (Exception err) {
            err.printStackTrace();
        }
        return returnValue;
    }
}
