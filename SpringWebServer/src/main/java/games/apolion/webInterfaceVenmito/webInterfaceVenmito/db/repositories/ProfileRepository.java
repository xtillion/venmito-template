package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.Profile;
import org.springframework.data.repository.CrudRepository;

public interface ProfileRepository  extends CrudRepository<Profile, String> {
}
