package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import jakarta.persistence.*;

import java.util.List;

@Entity
public class ItemList {
    @Id
    @GeneratedValue(strategy= GenerationType.UUID)
    private String id;
    @Column(nullable = false)
    @OneToMany(fetch = FetchType.EAGER)
    private ItemListEntry[] entries;
    private double totalOfPurchase;

    public void setTotalOfPurchase(double totalOfPurchase) {
        this.totalOfPurchase = totalOfPurchase;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public ItemListEntry[] getEntries() {
        return entries;
    }

    public void setEntries(ItemListEntry[] entries) {
        this.entries = entries;
    }

    public double getTotalOfPurchase() {
        return totalOfPurchase;
    }
}
