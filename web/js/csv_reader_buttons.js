import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "APZmedia.CSVReaderButtons",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        console.log("APZmedia.CSVReaderButtons: Checking node", nodeData?.name, "category:", nodeData?.category);
        
        if (!nodeData?.category?.startsWith("APZmedia")) {
            return;
        }
        
        console.log("APZmedia.CSVReaderButtons: Processing APZmedia node", nodeData.name);
        
        switch (nodeData.name) {
            case "APZmediaDynamicCSVReader":
            case "APZmediaCSVReader":
                console.log("APZmedia.CSVReaderButtons: Adding button to", nodeData.name);
                nodeType.prototype.onNodeCreated = function () {
                    console.log("APZmedia.CSVReaderButtons: Node created, adding button");
                    this.addWidget("button", "🔄 Update CSV", null, () => {
                        // Increment the force_reload parameter to trigger CSV reload
                        const forceReloadWidget = this.widgets.find(w => w.name === "force_reload");
                        if (forceReloadWidget) {
                            forceReloadWidget.value = (forceReloadWidget.value || 0) + 1;
                            // Trigger the node execution
                            this.graph.change();
                            console.log("CSV Update button clicked - force_reload incremented to", forceReloadWidget.value);
                        } else {
                            console.log("APZmedia.CSVReaderButtons: force_reload widget not found");
                        }
                    });
                }
                break;
        }
    }
}); 