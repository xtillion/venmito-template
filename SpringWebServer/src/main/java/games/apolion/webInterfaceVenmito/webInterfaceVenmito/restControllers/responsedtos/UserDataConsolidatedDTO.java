package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.EOriginId;
import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.UserDataConsolidated;

import java.time.ZonedDateTime;

public class UserDataConsolidatedDTO {
    private String id;

    private EOriginId[] origin_ids;
    private String[] firstNames;
    private String[] lastNames;

    private String[] telephones;

    private String[] emails;


    private String[] userDevices;

    private String[] locationCity;
    private String[] locationCountry;

    private ZonedDateTime createDate;

    public UserDataConsolidatedDTO(UserDataConsolidated userDataConsolidated, EOriginId[] origin_ids) {
        this.id = userDataConsolidated.getId();
        this.origin_ids = origin_ids;
        this.firstNames = userDataConsolidated.getFirstNames();
        this.lastNames = userDataConsolidated.getLastNames();
        this.telephones = userDataConsolidated.getTelephones();
        this.emails = userDataConsolidated.getEmails();
        this.userDevices = userDataConsolidated.getUserDevices();
        this.locationCity = userDataConsolidated.getLocationCity();
        this.locationCountry = userDataConsolidated.getLocationCountry();
        this.createDate = userDataConsolidated.getCreateDate();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
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

    public String[] getUserDevices() {
        return userDevices;
    }

    public void setUserDevices(String[] userDevices) {
        this.userDevices = userDevices;
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

    public ZonedDateTime getCreateDate() {
        return createDate;
    }

    public void setCreateDate(ZonedDateTime createDate) {
        this.createDate = createDate;
    }


}
