package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.PagableUserRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.ProfileDTO;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.UserDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;

@RestController // This means that this class is a Controller
public class UserController {

    private PagableUserRepository userRepository;

    @Autowired
    public UserController(PagableUserRepository userRepository) {
        this.userRepository = userRepository;
    }


    /**
     * Gets the authenticated user's data after login the user in and sending a JWT token
     * @param authentication user authentication data
     * @return the users data
     */
    @PostMapping(path = "/app/v1/login")
    public UserDTO getUser(Authentication authentication) {
        if(authentication == null)
            return null;
        Optional<User> optUser = userRepository.findByEmailAndIsDeletedFalse(authentication.getName());
        return new UserDTO(optUser.orElse(null));
    }



}