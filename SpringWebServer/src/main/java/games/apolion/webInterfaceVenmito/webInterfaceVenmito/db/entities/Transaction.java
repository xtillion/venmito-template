package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import jakarta.persistence.*;

import java.io.Serializable;

@Entity
public class Transaction implements Serializable {
    @Id
    @GeneratedValue(strategy= GenerationType.UUID)
    private String id;
    private String userTelephone;
    private String storeName;
    private String originID;
    @OneToMany
    private ItemListEntry[] entries;
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getUserTelephone() {
        return userTelephone;
    }

    public void setUserTelephone(String userTelephone) {
        this.userTelephone = userTelephone;
    }

    public String getStoreName() {
        return storeName;
    }

    public void setStoreName(String storeName) {
        this.storeName = storeName;
    }

    public String getOriginID() {
        return originID;
    }

    public void setOriginID(String originID) {
        this.originID = originID;
    }

    public ItemListEntry[] getEntries() {
        return entries;
    }

    public void setEntries(ItemListEntry[] entries) {
        this.entries = entries;
    }

}
