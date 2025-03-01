package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.Profile;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.PagableUserRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.ProfileDTO;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.UserDTO;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Optional;
import java.util.stream.StreamSupport;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;


public class TestUserController {

    private PagableUserRepository pageRep;
   private Authentication authentication;
    private UserController userController;



    @Test
    void test_getUser_HappyPath(){
        //Prepare
        resetVariablesUser();
        User myFirstUser = new User();
        myFirstUser.setId("1");
        myFirstUser.setName("a");
        when(pageRep.findByEmailAndIsDeletedFalse(anyString())).thenReturn(Optional.of(myFirstUser));
        when(authentication.getName()).thenReturn("a");

        //Execute
        UserDTO userDTO = userController.getUser(authentication);

        //Assert
        assert(userDTO!=null);
        verify(pageRep, times(1)).findByEmailAndIsDeletedFalse(anyString());
        verify(authentication, times(1)).getName();
    }


    private void resetVariablesUser() {
        pageRep = Mockito.mock(PagableUserRepository.class);
       authentication = Mockito.mock(Authentication.class);
        userController = new UserController(pageRep);
    }
}
