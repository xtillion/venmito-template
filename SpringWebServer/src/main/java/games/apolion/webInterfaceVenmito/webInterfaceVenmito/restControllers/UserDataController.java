package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.EOriginId;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.UserDataConsolidated;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.CrudUserDataConsolidatedRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.PagableUserDataConsolidatedRepository;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.UserDataConsolidatedDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Optional;

@RestController // This means that this class is a Controller
public class UserDataController {

    private PagableUserDataConsolidatedRepository userDataConPageRepository;
    private CrudUserDataConsolidatedRepository userDataConCRUDRepository;

    @Autowired
    public UserDataController(PagableUserDataConsolidatedRepository userDataConPageRepository, CrudUserDataConsolidatedRepository userDataConCRUDRepository) {
        this.userDataConPageRepository = userDataConPageRepository;
        this.userDataConCRUDRepository = userDataConCRUDRepository;
    }




    /**
     * Gets the authenticated user's data after login the user in and sending a JWT token
     * @param authentication user authentication data
     * @return the users data
     */
    @GetMapping(path = "/app/v1/userdata/all")
    public Iterable<UserDataConsolidatedDTO> getUserData(@RequestParam(required = false) Optional<Integer> pageSize,
                                                         @RequestParam(required = false) Optional<Integer> pageNumber,
                                                         Authentication authentication) {
        int size = 10;
        int page = 1;
        if(pageSize.isPresent() ){
            size = pageSize.get();
        }
        if(pageNumber.isPresent()){
            page = pageNumber.get();
        }

        Pageable pageable = PageRequest.of(page, size);
        if(authentication == null)
            return null;
        List<UserDataConsolidatedDTO> userDataDTOList = new ArrayList<>();
        Iterable<UserDataConsolidated> iterUserData = userDataConPageRepository.findAll(pageable);
        Iterator<UserDataConsolidated> iter = iterUserData.iterator();
        while(iter.hasNext()){
            userDataDTOList.add(new UserDataConsolidatedDTO(iter.next(),null));
        }
        return userDataDTOList;
    }



}