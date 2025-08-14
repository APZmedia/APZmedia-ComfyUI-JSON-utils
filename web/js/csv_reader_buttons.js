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
            case "APZmediaDynamicCSVReader":
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
                        const updateButton = this.addWidget("button", "🔄 Update CSV Structure", null, () => {
                            console.log("🔄 APZmedia.CSVReaderButtons: Button clicked for", this.type);
                            
                            // Find the refresh_trigger widget
                            const refreshTriggerWidget = this.widgets.find(w => w.name === "refresh_trigger");
                            console.log("🔍 APZmedia.CSVReaderButtons: Looking for refresh_trigger widget, found:", refreshTriggerWidget);
                            
                            if (refreshTriggerWidget) {
                                // Generate a unique timestamp to trigger the refresh
                                const timestamp = Date.now().toString();
                                refreshTriggerWidget.value = timestamp;
                                console.log("✅ APZmedia.CSVReaderButtons: refresh_trigger set to timestamp:", timestamp);
                                
                                // For dynamic CSV reader, we need to handle output structure updates
                                if (this.type === "APZmediaDynamicCSVReader") {
                                    console.log("🔧 APZmedia.CSVReaderButtons: Dynamic CSV reader - attempting structure update");
                                    
                                    // Store current connections before potential structure change
                                    const currentConnections = [];
                                    if (this.outputs) {
                                        this.outputs.forEach((output, index) => {
                                            if (output.links && output.links.length > 0) {
                                                output.links.forEach(linkId => {
                                                    const link = this.graph.links[linkId];
                                                    if (link) {
                                                        currentConnections.push({
                                                            outputIndex: index,
                                                            outputName: output.name,
                                                            targetNodeId: link.target_id,
                                                            targetSlot: link.target_slot
                                                        });
                                                    }
                                                });
                                            }
                                        });
                                    }
                                    console.log("💾 APZmedia.CSVReaderButtons: Stored connections:", currentConnections);
                                }
                                
                                // Mark the node as changed to trigger execution
                                this.setDirtyCanvas(true, true);
                                if (this.graph) {
                                    this.graph.change();
                                    console.log("🔄 APZmedia.CSVReaderButtons: Graph change triggered");
                                }
                                
                                // For dynamic nodes, show a message about the limitation
                                if (this.type === "APZmediaDynamicCSVReader") {
                                    console.log("ℹ️ APZmedia.CSVReaderButtons: Note - ComfyUI doesn't support true dynamic outputs. The node will update its internal structure, but output ports remain fixed. Use the JSON output for dynamic column access.");
                                }
                                
                            } else {
                                console.log("❌ APZmedia.CSVReaderButtons: refresh_trigger widget not found!");
                                console.log("🔍 APZmedia.CSVReaderButtons: Available widgets:", this.widgets.map(w => w.name));
                            }
                        });
                        
                        // Customize button appearance based on node type
                        if (nodeData.name === "APZmediaDynamicCSVReader") {
                            updateButton.name = "🔄 Reload & Update Structure";
                        }
                        
                        console.log("✅ APZmedia.CSVReaderButtons: Button widget added successfully");
                        
                        // Add a custom method to handle dynamic output updates (for future use)
                        this.updateCSVStructure = function(columnNames) {
                            console.log("🔧 APZmedia.CSVReaderButtons: updateCSVStructure called with columns:", columnNames);
                            // This is where we would implement dynamic output updates if ComfyUI supported it
                            // For now, we log the structure change
                            if (columnNames && columnNames.length > 0) {
                                console.log("📊 APZmedia.CSVReaderButtons: CSV structure updated - columns:", columnNames.join(", "));
                                
                                // Update node title to show column count
                                this.title = `${this.type} (${columnNames.length} cols)`;
                                
                                // Force a visual update
                                if (this.graph && this.graph.canvas) {
                                    this.graph.canvas.draw(true, true);
                                }
                            }
                        };
                        
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
