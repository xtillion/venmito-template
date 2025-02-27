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
     * returns a list of users that fit the search term criteria pagination optional
     * @param pageSize
     * @param pageNumber
     * @param searchTerm
     * @param authentication
     * @return
     */
    @GetMapping(path="/app/v1/user/{searchTerm}/findByUsernameOrEmail")
    public @ResponseBody ResponseEntity<Iterable<UserDTO>> getAllUsersByEmailUsername(@RequestParam(required = false) Optional<Integer> pageSize,
                                                                                     @RequestParam(required = false) Optional<Integer> pageNumber,
                                                                                     @PathVariable(required = true) String searchTerm,
                                                                                     Authentication authentication) {
        User u = userRepository.findByEmailAndIsDeletedFalse(authentication.getName()).orElse(null);
        if(u == null){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(null);
        }
        int size = 50;
        int page = 0;
        if(pageSize.isPresent() ){
            size = pageSize.get();
        }
        if(pageNumber.isPresent()){
            page = pageNumber.get();
        }

        if(size<=0)
            size=1;
        if(page<0)
            page=0;
        List<UserDTO> usersDTOs = new ArrayList<UserDTO>();
        Pageable  pageable = PageRequest.of(page, size);
        Iterable<User> users = userRepository.findAllByEmailNameLike(searchTerm, searchTerm, pageable).getContent();
        Iterator<User> ite = users.iterator();
        while(ite.hasNext()){
            User user = ite.next();
            usersDTOs.add(new UserDTO(user));
        }
        return ResponseEntity.status(HttpStatus.OK).body(usersDTOs);
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

    /**
     * Gets the user's profile data if permission allow
     * @param authentication
     * @param userId id of the user to get the data from
     * @return the users profile
     */
    @GetMapping(path="/app/v1/user/{userId}")
    public ResponseEntity<ProfileDTO> getUserProfile(@PathVariable(required = true) String userId, Authentication authentication) {
        User u = userRepository.findByEmailAndIsDeletedFalse(authentication.getName()).orElse(null);
        if(u == null){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(null);
        }
        if(u.getEmail()==authentication.getName()){
            return ResponseEntity.status(HttpStatus.OK).body(new ProfileDTO(u.getProfileInfo()));
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ProfileDTO(null));
    }


}