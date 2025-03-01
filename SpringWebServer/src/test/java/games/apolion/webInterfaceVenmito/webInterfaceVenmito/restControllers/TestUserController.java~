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
    void test_getAllUsersByEmailUsername_HappyPath(){
        //Prepare
        resetVariablesUser();
        User myFirstUser = new User();
        myFirstUser.setId("1");
        myFirstUser.setName("a");
        List<User> users = List.of(myFirstUser);
        Pageable pageable = PageRequest.of(0, 1);
        when(pageRep.findAllByEmailNameLike(anyString(), anyString(),any(Pageable.class))).thenReturn(new PageImpl<>(users,pageable,users.size()));
        when(pageRep.findByEmailAndIsDeletedFalse(anyString())).thenReturn(Optional.of(myFirstUser));
        when(authentication.getName()).thenReturn("a");

        //Execute
        ResponseEntity<Iterable<UserDTO>> respUsersDTOs = userController.getAllUsersByEmailUsername(Optional.empty(), Optional.empty(), "a", authentication);

        //Assert
        List <UserDTO> userDTOsList = StreamSupport.stream(respUsersDTOs.getBody().spliterator(), false).toList();
        assert(userDTOsList.size()==1);
        verify(pageRep, times(1)).findAllByEmailNameLike(anyString(),anyString(),any(Pageable.class));
        verify(pageRep, times(1)).findByEmailAndIsDeletedFalse(anyString());
        verify(authentication, times(1)).getName();
    }


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

    @Test
    void test_getUserProfile_HappyPathSameUser(){
        //Prepare
        resetVariablesUser();
        User myFirstUser = new User();
        myFirstUser.setId("1");
        myFirstUser.setName("a");
        myFirstUser.setEmail("a");
        Profile myFirstProfile = new Profile();
        myFirstUser.setName("Antonio");
        myFirstUser.setProfileInfo(myFirstProfile);
        when(pageRep.findByEmailAndIsDeletedFalse(anyString())).thenReturn(Optional.of(myFirstUser));
        when(authentication.getName()).thenReturn("a");

        //Execute
        ResponseEntity<ProfileDTO> responseProfileDTO = userController.getUserProfile("1",authentication);

        //Assert
        assert(responseProfileDTO.getBody()!=null);
        verify(authentication, times(2)).getName();
    }
    @Test
    void test_getUserProfile_HappyPathDiffrentUser(){
        //Prepare
        resetVariablesUser();
        User myFirstUser = new User();
        myFirstUser.setId("1");
        myFirstUser.setName("a");
        myFirstUser.setEmail("a@apolion.games");
        Profile myFirstProfile = new Profile();
        myFirstUser.setName("Antonio");
        myFirstUser.setProfileInfo(myFirstProfile);
        when(pageRep.findByEmailAndIsDeletedFalse(anyString())).thenReturn(Optional.of(myFirstUser));
        when(authentication.getName()).thenReturn("a");

        //Execute
        ResponseEntity<ProfileDTO> respprofileDTO = userController.getUserProfile("1",authentication);

        //Assert
        assert(respprofileDTO.getBody()!=null);
        verify(authentication, times(2)).getName();
    }

    private void resetVariablesUser() {
        pageRep = Mockito.mock(PagableUserRepository.class);
       authentication = Mockito.mock(Authentication.class);
        userController = new UserController(pageRep);
    }
}
