package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.utils.TimeZoneConverter;
import jakarta.persistence.*;

import java.time.ZonedDateTime;

@Entity
public class Profile {

    @Id
    @GeneratedValue(strategy= GenerationType.UUID)
    private String id;

    private String aboutMe;

    private String hobbies;

    private String skills;

    private String desiredSkills;


    private int avgReviewScore;

    private String mentoringClasses;

    @OneToOne
    private User userID;

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

    public void setId(String id) {
        this.id = id;
    }

    public String getAboutMe() {
        return aboutMe;
    }

    public void setAboutMe(String aboutMe) {
        this.aboutMe = aboutMe;
    }

    public String getHobbies() {
        return hobbies;
    }

    public void setHobbies(String hobbies) {
        this.hobbies = hobbies;
    }

    public String getSkills() {
        return skills;
    }

    public void setSkills(String skills) {
        this.skills = skills;
    }

    public String getDesiredSkills() {
        return desiredSkills;
    }

    public void setDesiredSkills(String desiredSkills) {
        this.desiredSkills = desiredSkills;
    }

    public int getAvgReviewScore() {
        return avgReviewScore;
    }

    public void setAvgReviewScore(int avgReviewScore) {
        this.avgReviewScore = avgReviewScore;
    }

    public String getMentoringClasses() {
        return mentoringClasses;
    }

    public void setMentoringClasses(String mentoringClasses) {
        this.mentoringClasses = mentoringClasses;
    }

    public User getUserID() {
        return userID;
    }

    public void setUserID(User userID) {
        this.userID = userID;
    }
}
