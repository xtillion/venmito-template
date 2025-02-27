package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;

import java.util.Optional;


// This will be AUTO IMPLEMENTED by Spring into a Bean called userRepository
// CRUD refers Create, Read, Update, Delete

public interface PagableUserRepository extends PagingAndSortingRepository<User, String> {

   @Query("SELECT u FROM User u WHERE (u.name LIKE %:email% OR u.email LIKE %:name%) AND u.isDeleted = false")
    Page<User> findAllByEmailNameLike(@Param("email") String email,@Param("name") String name, Pageable pageable);


    Optional<User> findByIdAndIsDeletedFalse(String id);
    Optional<User> findByEmailAndIsDeletedFalse(String email);

}