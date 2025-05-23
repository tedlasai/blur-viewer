const methods = ['present', 'pastfuture'];


// Global initialization
let wild_viewer = null;
let simulated_viewer = null;

document.addEventListener("DOMContentLoaded", () => {
	simulated_viewer = new SimulatedViewer();
	wild_viewer = new InTheWildViewer();
});

