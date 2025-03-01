package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.UserDataConsolidated;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos.UserDataConsolidatedDTO;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface CrudUserDataConsolidatedRepository extends CrudRepository<UserDataConsolidated, String> {

}
