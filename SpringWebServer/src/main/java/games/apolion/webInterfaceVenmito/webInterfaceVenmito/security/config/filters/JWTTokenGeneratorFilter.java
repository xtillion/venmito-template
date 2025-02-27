package games.apolion.webInterfaceVenmito.webInterfaceVenmito.security.config.filters;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.constants.ApplicationConstants;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.core.env.Environment;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.crypto.SecretKey;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.stream.Collectors;
@Component
public class JWTTokenGeneratorFilter extends OncePerRequestFilter {


    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if(null!=authentication) {
            if (authentication.getName().length() <= 0 || authentication.getName().equals("anonymousUser")){
                filterChain.doFilter(request, response);
                return;
             }
            Environment environment = getEnvironment();
            if(null!= environment){
                String secret = environment.getProperty(ApplicationConstants.JWT_SECRET_KEY,ApplicationConstants.JWT_SECRET_KEY_DEFAULT);
                SecretKey secretKey = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
                String jwt = Jwts.builder().issuer("ProfileService")
                    .subject("JWT Token")
                    .claim("username",authentication.getName())
                    .claim("authorities",authentication.getAuthorities().stream().map(
                            GrantedAuthority::getAuthority
                    ).collect(Collectors.joining(","))
                    ).issuedAt(new Date())
                        .expiration(new Date(new Date().getTime() + 30_000_000))
                        .signWith(secretKey).compact();
                response.setHeader(ApplicationConstants.JWT_HEADER,jwt);
            }
        }
        filterChain.doFilter(request,response);
    }

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) throws ServletException {
        return !request.getServletPath().equals("/app/v1/login");
    }
}
