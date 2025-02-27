package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.utils.TimeZoneConverter;
import jakarta.persistence.*;

import java.time.ZonedDateTime;
import java.util.List;

@Entity // This tells Hibernate to make a table out of this class
public class UserDataConsolidated {
    @Id
    @GeneratedValue(strategy=GenerationType.UUID)
    private String id;

    @OneToMany
    private EOriginId[] origin_ids;
    private String[] firstNames;
    private String[] lastNames;

    @Column(nullable = false)
    private String[] telephones;

    @Column(nullable = false)
    private String[] emails;

    @Column(nullable = false)
    private boolean enabled;

    private String[] userDevices;

    private String[] locationCity;
    private String[] locationCountry;

    @Column(nullable = false)
    private ZonedDateTime createDate;
    private ZonedDateTime deleteDate;

    private boolean isDeleted;

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

    public EOriginId[] getOrigin_ids() {
        return origin_ids;
    }

    public void setOrigin_ids(EOriginId[] origin_ids) {
        this.origin_ids = origin_ids;
    }

    public String[] getFirstNames() {
        return firstNames;
    }

    public void setFirstNames(String[] firstNames) {
        this.firstNames = firstNames;
    }

    public String[] getLastNames() {
        return lastNames;
    }

    public void setLastNames(String[] lastNames) {
        this.lastNames = lastNames;
    }

    public String[] getTelephones() {
        return telephones;
    }

    public void setTelephones(String[] telephones) {
        this.telephones = telephones;
    }

    public String[] getEmails() {
        return emails;
    }

    public void setEmails(String[] emails) {
        this.emails = emails;
    }

    public String[] getLocationCity() {
        return locationCity;
    }

    public void setLocationCity(String[] locationCity) {
        this.locationCity = locationCity;
    }

    public String[] getLocationCountry() {
        return locationCountry;
    }

    public void setLocationCountry(String[] locationCountry) {
        this.locationCountry = locationCountry;
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