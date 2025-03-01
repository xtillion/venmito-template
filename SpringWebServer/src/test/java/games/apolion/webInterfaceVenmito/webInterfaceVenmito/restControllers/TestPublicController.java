package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.Authorities;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.AuthoritiesRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.CrudUserRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.PagableUserRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.requestdtos.RegisterUserDTO;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.OperationResultDTO;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;


public class TestPublicController {

    private PagableUserRepository pageRep;
    private CrudUserRepository userRep;
    private PasswordEncoder passwordEncoder;
    private AuthoritiesRepository authoritiesRepository;
    private PublicController publicController;




    @Test
    void test_getUserSalt_HappyPath(){
        //Prepare
        resetVariablesPublicController();
        String email = "a@apolion.games";
        User user = new User();
        user.setSalt("lol");
        user.setEmail(email);
        when(pageRep.findByEmailAndIsDeletedFalse(email)).thenReturn(Optional.of(user));

        //Execute
        ResponseEntity<String> responseEntity = publicController.getUserSalt(email);

        //Assert
        assert(responseEntity.getStatusCode()==HttpStatus.OK);
        assert(responseEntity.getBody()==user.getSalt());
        verify(pageRep,times(1)).findByEmailAndIsDeletedFalse(email);
    }

    @Test
    void test_getNewUserSalt_HappyPath(){
        //Prepare
        resetVariablesPublicController();

        //Execute
        ResponseEntity<String> entity = publicController.getNewUserSalt();

        //Assert
        assert (entity.getStatusCode()==HttpStatus.OK);
        assert (entity.getBody().toString().length()>0);
    }

    private void resetVariablesPublicController() {
        pageRep = Mockito.mock(PagableUserRepository.class);
        userRep = Mockito.mock(CrudUserRepository.class);
        passwordEncoder = Mockito.mock(PasswordEncoder.class);
        authoritiesRepository = Mockito.mock(AuthoritiesRepository.class);
        publicController = new PublicController(userRep,pageRep,passwordEncoder,authoritiesRepository);
    }
}
