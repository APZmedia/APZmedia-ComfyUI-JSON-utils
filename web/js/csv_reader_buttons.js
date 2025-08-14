import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "APZmedia.CSVReaderButtons",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (!nodeData?.category?.startsWith("APZmedia")) {
            return;
        }
        
        switch (nodeData.name) {
            case "APZmediaDynamicCSVReader":
            case "APZmediaCSVReader":
                nodeType.prototype.onNodeCreated = function () {
                    this.addWidget("button", "🔄 Update CSV", null, () => {
                        // Trigger the CSV update by changing the update_csv parameter
                        const updateWidget = this.widgets.find(w => w.name === "update_csv");
                        if (updateWidget) {
                            updateWidget.value = true;
                            // Trigger the node execution
                            this.graph.change();
                        }
                    });
                }
                break;
        }
    }
}); 