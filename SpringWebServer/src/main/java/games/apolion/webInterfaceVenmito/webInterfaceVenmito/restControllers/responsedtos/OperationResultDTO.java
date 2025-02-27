package games.apolion.webInterfaceVenmito.webInterfaceVenmito.restControllers.responsedtos;

public class OperationResultDTO {
    private boolean wasSucessful=false;
    private String successMessage;

    public OperationResultDTO(boolean wasSucessful, String successMessage) {
        this.wasSucessful = wasSucessful;
        this.successMessage = successMessage;
    }

    public String getSuccessMessage() {
        return successMessage;
    }

    public void setSuccessMessage(String successMessage) {
        this.successMessage = successMessage;
    }

    public boolean isWasSucessful() {
        return wasSucessful;
    }

    public void setWasSucessful(boolean wasSucessful) {
        this.wasSucessful = wasSucessful;
    }
}
