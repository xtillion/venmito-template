package games.apolion.webInterfaceVenmito.webInterfaceVenmito.security.config;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.repositories.CrudUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Component
public class ProfileServiceUserDetailsService implements UserDetailsService {

    @Autowired
    private CrudUserRepository userRepository;


    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepository.findByEmailAndIsDeletedFalseAndIsDeletedFalse(username)
                .orElseThrow(()-> new UsernameNotFoundException("User not found: "+username));
        List<GrantedAuthority> authorities = user.getAuthority()
                .stream()
                .map(authority -> new SimpleGrantedAuthority(
                        authority.getName())
                ).collect(Collectors.toList());
        return new org.springframework.
                security.core.userdetails.User(user.getEmail(),user.getPassword(),authorities);
    }

}
