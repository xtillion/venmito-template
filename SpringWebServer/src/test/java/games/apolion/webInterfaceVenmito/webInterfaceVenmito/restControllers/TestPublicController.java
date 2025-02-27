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
    void test_addNewUser_HappyPath(){
        //Prepare
        resetVariablesPublicController();
        RegisterUserDTO registerUserDTO = new RegisterUserDTO();
        registerUserDTO.setEmail("a@apolion.games");
        registerUserDTO.setPasswordHash("password");
        when(passwordEncoder.encode(anyString())).thenReturn("hashedpassword");
        User user = new User();
        user.setId("1");
        when(userRep.save(any())).thenReturn(user);
        Authorities auth = new Authorities();
        when(authoritiesRepository.save(any())).thenReturn(auth);

        //Execute
        ResponseEntity<OperationResultDTO> responseEntity = publicController.addNewUser(registerUserDTO);

        //Assert
        assert (responseEntity.getStatusCode()==HttpStatus.CREATED);
        verify(passwordEncoder, times(1)).encode(anyString());
        verify(authoritiesRepository, times(1)).save(any());
        verify(userRep, times(2)).save(any());
    }

    @Test
    void test_addMentor_HappyPath(){
        //Prepare
        resetVariablesPublicController();
        RegisterUserDTO registerUserDTO = new RegisterUserDTO();
        registerUserDTO.setEmail("a@apolion.games");
        registerUserDTO.setPasswordHash("password");
        when(passwordEncoder.encode(anyString())).thenReturn("hashedpassword");
        Authorities auth = new Authorities();
        when(authoritiesRepository.save(any())).thenReturn(auth);
        when(userRep.save(any(User.class))).thenAnswer(new Answer<User>() {
            @Override
            public User answer(InvocationOnMock invocationOnMock) throws Throwable {
                assert (invocationOnMock.getArgument(0) instanceof User);
                User user= (User) invocationOnMock.getArgument(0);
                assert(user.getEmail().equals(registerUserDTO.getEmail()));
                assert(user.getPassword().equals("hashedpassword"));
                user.setId("1");
                return user;
            }
        });
        //Execute
        ResponseEntity<OperationResultDTO> responseEntity = publicController.addMentor(registerUserDTO);

        //Assert
        assert (responseEntity.getStatusCode()==HttpStatus.CREATED);
        verify(passwordEncoder, times(1)).encode(anyString());
        verify(authoritiesRepository, times(1)).save(any());
        verify(userRep, times(2)).save(any());
    }

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
