package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.utils.TimeZoneConverter;
import jakarta.persistence.*;

import java.time.ZonedDateTime;
import java.util.List;

@Entity // This tells Hibernate to make a table out of this class
public class UserData {
    @Id
    @GeneratedValue(strategy=GenerationType.UUID)
    private String id;

    private String firstName;
    private String lastName;

    private String origin;

    @Column(nullable = false)
    private String telephone;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private boolean enabled;

    private String[] userDevices;

    private String originId;

    private String locationCity;
    private String locationCountry;

    @Column(nullable = false)
    private ZonedDateTime createDate;
    private ZonedDateTime deleteDate;

    private boolean isDeleted;

    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getTelephone() {
        return telephone;
    }

    public void setTelephone(String telephone) {
        this.telephone = telephone;
    }

    public String[] getUserDevcices() {
        return userDevices;
    }

    public void setUserDevcices(String[] userDevcices) {
        this.userDevices = userDevcices;
    }

    public String[] getUserDevices() {
        return userDevices;
    }

    public void setUserDevices(String[] userDevices) {
        this.userDevices = userDevices;
    }

    public String getLocationCity() {
        return locationCity;
    }

    public void setLocationCity(String locationCity) {
        this.locationCity = locationCity;
    }

    public String getLocationCountry() {
        return locationCountry;
    }

    public void setLocationCountry(String locationCountry) {
        this.locationCountry = locationCountry;
    }

    public String getOriginId() {
        return originId;
    }

    public void setOriginId(String originId) {
        this.originId = originId;
    }

    public ZonedDateTime getDeleteDate() {
        return deleteDate;
    }

    public void setDeleteDate(ZonedDateTime deleteDate) {
        this.deleteDate = deleteDate;
    }
    public ZonedDateTime getDeleteDate(String timeZone) {
        TimeZoneConverter converter = new TimeZoneConverter();
        ZonedDateTime localDateTime = converter.convertFromUTC(deleteDate,timeZone);
        return localDateTime;
    }
    public boolean isDeleted() {
        return isDeleted;
    }

    public void setDeleted(boolean deleted) {
        isDeleted = deleted;
    }
    public ZonedDateTime getCreateDate() {
        return createDate;
    }
    public ZonedDateTime getCreateDate(String timeZone) {
        TimeZoneConverter converter = new TimeZoneConverter();
        ZonedDateTime localDateTime = converter.convertFromUTC(createDate,timeZone);
        return localDateTime;
    }
    public void setCreateDate(ZonedDateTime createDate) {
        this.createDate = createDate;
    }


    public String getId() {
        return id;
    }


    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }


    public void setId(String id) {
        this.id = id;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }
    
}