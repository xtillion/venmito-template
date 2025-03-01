package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.Authorities;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.AuthoritiesRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.CrudUserRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.PagableUserRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.requestdtos.RegisterUserDTO;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.OperationResultDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.time.ZonedDateTime;
import java.util.ArrayList;
import java.util.Optional;

@RestController // This means that this class is a Controller
@RequestMapping(path="/public/app/v1") // This means URL's start with /demo (after Application path)
public class PublicController {


    private CrudUserRepository userRepository;
    private PagableUserRepository pagableRepository;
    private PasswordEncoder passwordEncoder;
    private AuthoritiesRepository authoritiesRepository;

    @Autowired
    public PublicController(CrudUserRepository userRepository, PagableUserRepository pagableRepository, PasswordEncoder passwordEncoder, AuthoritiesRepository authoritiesRepository) {
        this.userRepository = userRepository;
        this.pagableRepository = pagableRepository;
        this.passwordEncoder = passwordEncoder;
        this.authoritiesRepository = authoritiesRepository;
    }

    @GetMapping(path="/getUserSalt")
    public @ResponseBody  ResponseEntity<String> getUserSalt(@RequestParam String email) {
        Optional<User> user = pagableRepository.findByEmailAndIsDeletedFalse(email);
        if(user.isPresent()){
            return ResponseEntity.status(HttpStatus.OK).body(user.get().getSalt());
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed");

    }

    @GetMapping(path="/getNewUserSalt")
    public @ResponseBody  ResponseEntity<String> getNewUserSalt() {
        return ResponseEntity.status(HttpStatus.OK).body(ZonedDateTime.now().toString());
    }



}