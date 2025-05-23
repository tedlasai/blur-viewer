const methods = ['present', 'pastfuture'];


// Global initialization
let wild_viewer = null;
let simulated_viewer = null;

document.addEventListener("DOMContentLoaded", () => {
	simulated_viewer = new SimulatedViewer('simulated', 9, 8);
	wild_viewer = new InTheWildViewer('wild', 17, 8);
});

