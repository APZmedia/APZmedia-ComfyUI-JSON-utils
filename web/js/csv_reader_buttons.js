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
                
                const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
                nodeType.prototype.onNodeCreated = function () {
                    // Call original onNodeCreated if it exists
                    if (originalOnNodeCreated) {
                        originalOnNodeCreated.apply(this, arguments);
                    }
                    
                    console.log("APZmedia.CSVReaderButtons: Node created, adding button");
                    
                    // Add the update button
                    const updateButton = this.addWidget("button", "🔄 Update CSV", null, () => {
                        console.log("APZmedia.CSVReaderButtons: Update button clicked");
                        
                        // Find the force_reload widget
                        const forceReloadWidget = this.widgets.find(w => w.name === "force_reload");
                        if (forceReloadWidget) {
                            forceReloadWidget.value = (forceReloadWidget.value || 0) + 1;
                            console.log("CSV Update button clicked - force_reload incremented to", forceReloadWidget.value);
                            
                            // Mark the node as changed to trigger execution
                            this.setDirtyCanvas(true, true);
                            if (this.graph) {
                                this.graph.change();
                            }
                        } else {
                            console.error("APZmedia.CSVReaderButtons: force_reload widget not found in widgets:", this.widgets.map(w => w.name));
                        }
                    });
                    
                    console.log("APZmedia.CSVReaderButtons: Button added successfully");
                }
                break;
        }
    }
});
