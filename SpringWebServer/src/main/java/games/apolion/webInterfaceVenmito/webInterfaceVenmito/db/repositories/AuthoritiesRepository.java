package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.Authorities;
import org.springframework.data.repository.CrudRepository;


// This will be AUTO IMPLEMENTED by Spring into a Bean called userRepository
// CRUD refers Create, Read, Update, Delete

public interface AuthoritiesRepository extends CrudRepository<Authorities, String> {

}