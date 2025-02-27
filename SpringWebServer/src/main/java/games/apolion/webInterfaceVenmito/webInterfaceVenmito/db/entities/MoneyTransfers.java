package games.apolion.webInterfaceVenmito.webInterfaceVenmito.db.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import java.io.Serializable;
import java.time.ZonedDateTime;

@Entity
public class MoneyTransfers implements Serializable {
    @Id
    @GeneratedValue(strategy=GenerationType.UUID)
    private String id;
    private String senderID;
    private String receiverID;
    private double amount;
    private ZonedDateTime transferDate;
    private ZonedDateTime createDate;

    public ZonedDateTime getTransferDate() {
        return transferDate;
    }

    public void setTransferDate(ZonedDateTime transferDate) {
        this.transferDate = transferDate;
    }
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getSenderID() {
        return senderID;
    }

    public void setSenderID(String senderID) {
        this.senderID = senderID;
    }

    public String getReceiverID() {
        return receiverID;
    }

    public void setReceiverID(String receiverID) {
        this.receiverID = receiverID;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public ZonedDateTime getCreateDate() {
        return createDate;
    }

    public void setCreateDate(ZonedDateTime createDate) {
        this.createDate = createDate;
    }
}
