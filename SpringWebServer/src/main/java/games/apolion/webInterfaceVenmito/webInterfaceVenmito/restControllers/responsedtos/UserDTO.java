package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.User;

import java.util.List;

public class UserDTO {

    private String id;

    private String name;

    private int dailyScore;

    private String frndType="unassociated";

    private int nmbrMentees;

    private String profilePicture;

    private String accessModifier;

    private ProfileDTO profileInfo;

    private String usrType;

    private String email;

    private boolean isRequestForFriends;

    public UserDTO() {

    }
    public UserDTO(User user) {
        if(user == null) return;
        this.id = user.getId();
        this.name = user.getName();
        this.profilePicture = user.getProfilePicture();
        this.accessModifier = user.getAccessModifier();
        this.profileInfo = new ProfileDTO(user.getProfileInfo());
        this.usrType = user.getUsrType();
        this.email = user.getEmail();
    }


    public boolean isRequestForFriends() {
        return isRequestForFriends;
    }

    public void setRequestForFriends(boolean requestForFriends) {
        isRequestForFriends = requestForFriends;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getDailyScore() {
        return dailyScore;
    }

    public void setDailyScore(int dailyScore) {
        this.dailyScore = dailyScore;
    }

    public String getFrndType() {
        return frndType;
    }

    public void setFrndType(String frndType) {
        this.frndType = frndType;
    }

    public int getNmbrMentees() {
        return nmbrMentees;
    }

    public void setNmbrMentees(int nmbrMentees) {
        this.nmbrMentees = nmbrMentees;
    }

    public String getProfilePicture() {
        return profilePicture;
    }

    public void setProfilePicture(String profilePicture) {
        this.profilePicture = profilePicture;
    }

    public String getAccessModifier() {
        return accessModifier;
    }

    public void setAccessModifier(String accessModifier) {
        this.accessModifier = accessModifier;
    }


    public ProfileDTO getProfileInfo() {
        return profileInfo;
    }

    public void setProfileInfo(ProfileDTO profileInfo) {
        this.profileInfo = profileInfo;
    }

    public String getUsrType() {
        return usrType;
    }

    public void setUsrType(String usrType) {
        this.usrType = usrType;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
