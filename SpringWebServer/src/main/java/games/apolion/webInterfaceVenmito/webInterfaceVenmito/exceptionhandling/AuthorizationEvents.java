package games.apolion.webInterfaceVenmito.webInterfaceVenmito.exceptionhandling;

import org.springframework.context.event.EventListener;
import org.springframework.security.authorization.event.AuthorizationDeniedEvent;
import org.springframework.stereotype.Component;

@Component
public class AuthorizationEvents {


    @EventListener
    public void onFailure(AuthorizationDeniedEvent deniedEvent) {
        System.out.println(""+deniedEvent.getAuthentication().get().getName()+" "+
                deniedEvent.getAuthorizationDecision().toString());
    }

}
