package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import jakarta.persistence.*;

import java.io.Serializable;

@Entity
public class SaleItem  implements Serializable {
    @Id
    @GeneratedValue(strategy=GenerationType.UUID)
    private String id;

    private double value;
    private String name;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
