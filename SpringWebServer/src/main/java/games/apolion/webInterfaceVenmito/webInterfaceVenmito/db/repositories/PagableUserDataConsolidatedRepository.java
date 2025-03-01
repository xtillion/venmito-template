package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.UserDataConsolidated;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.repository.PagingAndSortingRepository;


// This will be AUTO IMPLEMENTED by Spring into a Bean called userRepository
// CRUD refers Create, Read, Update, Delete

public interface PagableUserDataConsolidatedRepository extends PagingAndSortingRepository<UserDataConsolidated, String> {
    Page<UserDataConsolidated> findAll(Pageable pageable);
}