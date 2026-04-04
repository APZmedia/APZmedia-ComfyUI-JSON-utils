import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "APZmedia.CSVReaderButtons",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (!nodeData?.category?.startsWith("APZmedia")) {
            return;
        }

        switch (nodeData.name) {
            case "APZmediaCSVReader":
            case "APZmediaDynamicCSVReader": {
                const originalOnNodeCreated = nodeType.prototype.onNodeCreated;
                nodeType.prototype.onNodeCreated = function () {
                    if (originalOnNodeCreated) {
                        originalOnNodeCreated.apply(this, arguments);
                    }

                    try {
                        const buttonLabel = nodeData.name === "APZmediaDynamicCSVReader"
                            ? "🔄 Reload & Update Structure"
                            : "🔄 Update CSV Structure";

                        this.addWidget("button", buttonLabel, null, () => {
                            const refreshTriggerWidget = this.widgets.find(w => w.name === "refresh_trigger");

                            if (refreshTriggerWidget) {
                                refreshTriggerWidget.value = Date.now().toString();
                                this.setDirtyCanvas(true, true);
                                if (this.graph) {
                                    this.graph.change();
                                }
                            } else {
                                console.error("[APZmedia] refresh_trigger widget not found on", this.type);
                            }
                        });

                        this.updateCSVStructure = function (columnNames) {
                            if (columnNames && columnNames.length > 0) {
                                this.title = `${this.type} (${columnNames.length} cols)`;
                                if (this.graph && this.graph.canvas) {
                                    this.graph.canvas.draw(true, true);
                                }
                            }
                        };

                    } catch (error) {
                        console.error("[APZmedia] Error adding button:", error);
                    }
                };
                break;
            }
            default:
                break;
        }
    }
});
