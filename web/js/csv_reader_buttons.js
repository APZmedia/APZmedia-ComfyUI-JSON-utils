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
                        // Increment the force_reload parameter to trigger CSV reload
                        const forceReloadWidget = this.widgets.find(w => w.name === "force_reload");
                        if (forceReloadWidget) {
                            forceReloadWidget.value = (forceReloadWidget.value || 0) + 1;
                            // Trigger the node execution
                            this.graph.change();
                            console.log("CSV Update button clicked - force_reload incremented to", forceReloadWidget.value);
                        }
                    });
                }
                break;
        }
    }
}); 