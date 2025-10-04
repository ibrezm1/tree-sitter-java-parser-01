package com.jms;

import javax.ejb.ActivationConfigProperty;
import javax.ejb.MessageDriven;
import javax.jms.*;

import com.jpa.Customer;

@MessageDriven(activationConfig = {
        @ActivationConfigProperty(
            propertyName = "destination",
            propertyValue = "ejbQueue"
        ),
        @ActivationConfigProperty(
            propertyName = "destinationType",
            propertyValue = "javax.jms.Queue"
        ),
        @ActivationConfigProperty(
            propertyName = "messageSelector",
            propertyValue = "operation = 'createCustomer'"
        )
    }
)
public class TaskMessage implements MessageListener {
    
    @Override
    public void onMessage(Message message) {
        try {
            if (message instanceof ObjectMessage) {
                String operation = message.getStringProperty("operation");
                Object object = ((ObjectMessage)message).getObject();
                Customer customer = ((Customer) object);
                System.err.println("##### JMS Object Message - Operation: " + operation + " - " + customer.getFirstName() + " " + customer.getLastName() + " - " + customer.getId());
            } else {
                String operation = message.getStringProperty("operation");
                String customer = message.getStringProperty("customer");
                System.err.println("##### JMS Text Message - Operation: " + operation + " - " + customer);
            }
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }
    
}
