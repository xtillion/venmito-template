package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import org.springframework.data.repository.CrudRepository;

import java.util.Optional;

public interface CrudUserRepository extends CrudRepository<User, String> {

    Optional<User> findByEmailAndIsDeletedFalseAndIsDeletedFalse(String email);
}
