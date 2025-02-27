package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class EOriginId {
    @Id
    @GeneratedValue(strategy= GenerationType.UUID)
    private String id;
    private int myIdValue;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getMyIdValue() {
        return myIdValue;
    }

    public void setMyIdValue(int myIdValue) {
        this.myIdValue = myIdValue;
    }
}
