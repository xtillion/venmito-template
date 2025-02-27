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
    @PostMapping(path="/addMentor") // Map ONLY POST Requests
    public ResponseEntity<OperationResultDTO> addMentor (@RequestBody RegisterUserDTO regiterUserDTO
    ) {
        try{
            ResponseEntity<OperationResultDTO> BAD_REQUEST = validateRequest(regiterUserDTO);
            if (BAD_REQUEST != null) return BAD_REQUEST;

            User n = createNewMenteeUser(regiterUserDTO,"mentor");
            User u = userRepository.save(n);
            if(u!=null&&u.getId()!=null){
                Authorities auth = createAndSaveMenteeRole(n,"ROLE_MENTOR");
                if(auth!=null){
                    u = saveAuthorityForNewUser(u, auth);
                    if(u==null){
                        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                .body(new OperationResultDTO(false,"Could save role"));
                    }
                }
                else {
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body(new OperationResultDTO(false,"Could not create role"));
                }
                return ResponseEntity.status(HttpStatus.CREATED).body(new OperationResultDTO(true,"Saved"));
            }
        } catch (Exception e){
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new OperationResultDTO(false,"Failed as "+e.getMessage()));
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new OperationResultDTO(false,"Failed"));
    }



    @PostMapping(path="/addMentee") // Map ONLY POST Requests
    public ResponseEntity<OperationResultDTO> addNewUser (@RequestBody RegisterUserDTO regiterUserDTO
    ) {
        try{
            ResponseEntity<OperationResultDTO> BAD_REQUEST = validateRequest(regiterUserDTO);
            if (BAD_REQUEST != null) return BAD_REQUEST;

            User n = createNewMenteeUser(regiterUserDTO,"mentee");
            User u = userRepository.save(n);
            if(u!=null&&u.getId()!=null){
                Authorities auth = createAndSaveMenteeRole(n,"ROLE_MENTEE");
                if(auth!=null){
                    u = saveAuthorityForNewUser(u, auth);
                    if(u==null){
                        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                .body(new OperationResultDTO(false,"Could save role"));
                    }
                }
                else {
                    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                            .body(new OperationResultDTO(false,"Could not create role"));
                }
                return ResponseEntity.status(HttpStatus.CREATED).body(new OperationResultDTO(true,"Saved"));
            }
        } catch (Exception e){
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new OperationResultDTO(false,"Failed as "+e.getMessage()));
        }
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new OperationResultDTO(false,"Failed"));
    }

    private static ResponseEntity<OperationResultDTO> validateRequest(RegisterUserDTO regiterUserDTO) {
        if(!regiterUserDTO.getEmail().contains("@")){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new OperationResultDTO(false, "Invalid email"));
        }
        if(!regiterUserDTO.getEmail().contains(".")){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new OperationResultDTO(false, "Invalid email"));
        }
        if(regiterUserDTO.getEmail().contains("mailinator.com")){
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new OperationResultDTO(false, "Invalid email"));
        }
        return null;
    }
    private User createNewMenteeUser(RegisterUserDTO regiterUserDTO,String userType) {
        User n = new User();
        String hashPwd = passwordEncoder.encode(regiterUserDTO.getPasswordHash());
        n.setPassword(hashPwd);
        n.setName(regiterUserDTO.getName());
        n.setSalt(regiterUserDTO.getSalt());
        n.setUsrType(userType);
        n.setEmail(regiterUserDTO.getEmail());
        n.setNmbrMentees(0);
        n.setEnabled(true);
        n.setCreateDate(ZonedDateTime.now());
        return n;
    }

    private User saveAuthorityForNewUser(User u, Authorities auth) {
        u.setAuthority(new ArrayList<>());
        u.getAuthority().add(auth);
        u = userRepository.save(u);
        return u;
    }

    private Authorities createAndSaveMenteeRole(User n,String role) {
        Authorities auth = new Authorities();
        auth.setUser(n);
        auth.setCreateDate(ZonedDateTime.now());
        auth.setName(role);
        auth = authoritiesRepository.save(auth);
        return auth;
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