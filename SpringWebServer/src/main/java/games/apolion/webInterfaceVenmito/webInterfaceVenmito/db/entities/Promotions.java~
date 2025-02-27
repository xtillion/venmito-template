package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.utils.TimeZoneConverter;
import jakarta.persistence.*;

import java.time.ZonedDateTime;

@Entity // This tells Hibernate to make a table out of this class
public class Promotions {
    @Id
    @GeneratedValue(strategy=GenerationType.UUID)
    private String id;

    private String telephoneGivenAtTheTimeOfRegistration;
    private String promotionName;
    private boolean responded;
    private String email;

    @Column(nullable = false)
    private ZonedDateTime createDate;
    private ZonedDateTime deleteDate;

    private boolean isDeleted;


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

    public String getTelephoneGivenAtTheTimeOfRegistration() {
        return telephoneGivenAtTheTimeOfRegistration;
    }

    public void setTelephoneGivenAtTheTimeOfRegistration(String telephoneGivenAtTheTimeOfRegistration) {
        this.telephoneGivenAtTheTimeOfRegistration = telephoneGivenAtTheTimeOfRegistration;
    }

    public String getPromotionName() {
        return promotionName;
    }

    public void setPromotionName(String promotionName) {
        this.promotionName = promotionName;
    }

    public boolean isResponded() {
        return responded;
    }

    public void setResponded(boolean responded) {
        this.responded = responded;
    }
}