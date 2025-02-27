package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos;

import games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities.Profile;

public class ProfileDTO {
    private String aboutMe;

    private String hobbies;

    private String skills;

    private String desiredSkills;

    private int avgReviewScore;

    private String mentoringClasses;

    public ProfileDTO() {
    }

    public ProfileDTO(Profile profile) {
        if(profile == null) return;
        this.aboutMe = profile.getAboutMe();
        this.hobbies = profile.getHobbies();
        this.skills = profile.getSkills();
        this.desiredSkills = profile.getDesiredSkills();
        this.avgReviewScore = profile.getAvgReviewScore();
        this.mentoringClasses = profile.getMentoringClasses();
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
}
