import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "APZmedia.CSVReaderButtons",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        console.log("🔧 APZmedia.CSVReaderButtons: Extension loaded, checking node", nodeData?.name, "category:", nodeData?.category);
        
        if (!nodeData?.category?.startsWith("APZmedia")) {
            console.log("❌ APZmedia.CSVReaderButtons: Skipping non-APZmedia node", nodeData?.name);
            return;
        }
        
        console.log("✅ APZmedia.CSVReaderButtons: Processing APZmedia node", nodeData.name);
        
        switch (nodeData.name) {
            case "APZmediaCSVReader":
                console.log("🎯 APZmedia.CSVReaderButtons: Found CSV reader node, setting up button for", nodeData.name);
                
                const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
                nodeType.prototype.onNodeCreated = function () {
                    console.log("🚀 APZmedia.CSVReaderButtons: Node created, adding button to", this.title || this.type);
                    
                    // Call original onNodeCreated if it exists
                    if (originalOnNodeCreated) {
                        originalOnNodeCreated.apply(this, arguments);
                    }
                    
                    try {
                        // Add the update button
                        const updateButton = this.addWidget("button", "🔄 Update CSV", null, () => {
                            console.log("🔄 APZmedia.CSVReaderButtons: Button clicked!");
                            
                            // Find the force_reload widget
                            const forceReloadWidget = this.widgets.find(w => w.name === "force_reload");
                            console.log("🔍 APZmedia.CSVReaderButtons: Looking for force_reload widget, found:", forceReloadWidget);
                            
                            if (forceReloadWidget) {
                                const oldValue = forceReloadWidget.value || 0;
                                forceReloadWidget.value = oldValue + 1;
                                console.log("✅ APZmedia.CSVReaderButtons: force_reload incremented from", oldValue, "to", forceReloadWidget.value);
                                
                                // Mark the node as changed to trigger execution
                                this.setDirtyCanvas(true, true);
                                if (this.graph) {
                                    this.graph.change();
                                    console.log("🔄 APZmedia.CSVReaderButtons: Graph change triggered");
                                }
                            } else {
                                console.log("❌ APZmedia.CSVReaderButtons: force_reload widget not found!");
                                console.log("🔍 APZmedia.CSVReaderButtons: Available widgets:", this.widgets.map(w => w.name));
                            }
                        });
                        
                        console.log("✅ APZmedia.CSVReaderButtons: Button widget added successfully");
                    } catch (error) {
                        console.error("❌ APZmedia.CSVReaderButtons: Error adding button:", error);
                    }
                }
                break;
            default:
                console.log("ℹ️ APZmedia.CSVReaderButtons: APZmedia node found but not a CSV reader:", nodeData.name);
                break;
        }
    }
});
