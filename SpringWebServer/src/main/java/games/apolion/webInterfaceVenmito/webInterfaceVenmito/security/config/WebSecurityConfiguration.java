package games.apolion.webInterfaceVenmito.webInterfaceVenmito.security.config;


import games.apolion.webInterfaceVenmito.webInterfaceVenmito.exceptionhandling.CustomAccessDeniedHandler;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.exceptionhandling.CustomBasicAuthenticationEntryPoint;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.security.config.filters.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.ProviderManager;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.www.BasicAuthenticationFilter;
import org.springframework.stereotype.Component;

@Configuration
@EnableWebSecurity
@Component
public class WebSecurityConfiguration {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
//                .requiresChannel(rcc->rcc.anyRequest().requiresSecure())//Only for HTTPS
//                .sessionManagement((smc) -> smc.maximumSessions(1))
//                .sessionManagement((smc) -> smc.sessionFixation(
//                                (sessionFixationConfigurer -> sessionFixationConfigurer.newSession())
//                        )
//                )
                .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .csrf(csrf -> csrf.disable())
                .authorizeRequests(authorize -> authorize
//                    .requestMatchers("/app/v1/**").hasAnyAuthority("ROLE_ADMIN","ROLE_MENTEE")
                    .requestMatchers("/error","/index.html","/").permitAll()
                    .requestMatchers("/app/v1/**","/**").hasAnyAuthority("ADMIN","USER")
                )
                .httpBasic(
                        hbc->
                        hbc.authenticationEntryPoint(new CustomBasicAuthenticationEntryPoint()));
        http.exceptionHandling(ehc->ehc.accessDeniedHandler(new CustomAccessDeniedHandler()));
//        http.logout(loc -> loc.invalidateHttpSession(true).clearAuthentication(true).deleteCookies("JSESSIONID"));
        http.addFilterBefore(new RequestValidationBeforeFilter(), BasicAuthenticationFilter.class)
                .addFilterAfter(new AuthoritiesLoggingAfterFilter(), BasicAuthenticationFilter.class)
                .addFilterAt(new AuthoritiesLoggingAtFilter(), BasicAuthenticationFilter.class)
                .addFilterAfter(new JWTTokenGeneratorFilter(), BasicAuthenticationFilter.class)
                .addFilterBefore(new JWTTokenValidatorFilter(), BasicAuthenticationFilter.class);
        ;
        return http.build();
    }

//    @Bean
//    public UserDetailsService userDetailsService() {
//        UserDetails user = User.withUsername("user").password("{bcrypt}$2a$12$KN.uBC3NmyNU..6.yfZF6u.KKDPR.D3ne3vrmLxzvBcveryDHYdkq").authorities("read").build();
//        UserDetails admin = User.withUsername("admin").password("{bcrypt}$2a$12$KN.uBC3NmyNU..6.yfZF6u.KKDPR.D3ne3vrmLxzvBcveryDHYdkq").authorities("admin").build();
//
//        return new InMemoryUserDetailsManager(user, admin);
//    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }

//    @Bean
//    public CompromisedPasswordChecker compromisedPasswordChecker() {
//        return new HaveIBeenPwnedRestApiPasswordChecker();
//    }

    @Bean
    public AuthenticationManager authenticationManager(ProfileServiceUserDetailsService userDetailsService,
                                                       PasswordEncoder passwordEncoder) {
        ProfileServiceUsernamePwdAuthenticationProvider authenticationProvider =
                new ProfileServiceUsernamePwdAuthenticationProvider(userDetailsService, passwordEncoder);
        ProviderManager providerManager = new ProviderManager(authenticationProvider);
        providerManager.setEraseCredentialsAfterAuthentication(false);
        return  providerManager;
    }
}