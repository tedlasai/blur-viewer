
class SimulatedViewer {
	constructor(prefix, max_idx, n_scenes, playback_speed = 1) {
		this.prefix = 'simulated';
		this.max_idx = max_idx;
		this.n_scenes = n_scenes;
		this.cur_frame = 0;
		this.base_im = '0000';
		this.method = 'present';
		this.playback_speed = 1;
		this.interval_id = null;
		this.anim_dir = 1;
		this.current_delay = 200;

		this.video_recon = document.getElementById(`${prefix}-ours`);
		this.video_tracks = document.getElementById(`${prefix}-ours-tracks`);
		this.input_img = document.getElementById(`${prefix}-input`);

		this.initSceneSelector();
		this.initSliderSync();
	}

	initSceneSelector() {
		const selector = document.getElementById(`${this.prefix}-scene-selector`);
		for (let i = 0; i < this.n_scenes; i++) {
			const padded = i.toString().padStart(4, '0');
			selector.innerHTML += `
				<div onclick="${this.prefix}_viewer.change_scene('${padded}')">
					<img class="selectable" style="border-radius:1em; max-width: 7em"
					     src="assets/${this.prefix}/icons/${padded}.png">
				</div>`;
		}
	}

	initSliderSync() {
		const slider = document.getElementById(`${this.prefix}_frame_control`);
		if (!this.video_recon || !slider) return;

		this.video_recon.addEventListener("loadedmetadata", () => {
			this.video_recon.addEventListener("timeupdate", () => {
				if (!this.video_recon.duration) return;

				const progress = this.video_recon.currentTime / this.video_recon.duration;
				const newVal = Math.round(progress * (this.max_idx - 1));  // Match .change_frame()
				
				if (parseInt(slider.value) !== newVal) {
					slider.value = newVal;
					this.cur_frame = newVal;
					this.applyGlowEffect();
				}
			});
		});
	}


	set_method(name) {
		this.method = name;
		this.loadVideos();

		// Update blurry image
		if (this.input_img)
			this.input_img.src = `assets/${this.prefix}/blurry/${this.base_im}_${name}.png`;

		// Toggle button styles
		document.querySelectorAll(`#${this.prefix}-method-toggle button`).forEach(btn => {
			btn.classList.toggle("is-info", btn.dataset.method === name);
			btn.classList.toggle("is-light", btn.dataset.method !== name);
		});

		const slider = document.getElementById(`${this.prefix}_frame_control`);
		const isPF = name === "pastfuture";
		slider.classList.toggle("pastfuture", isPF);
		document.getElementById(`${this.prefix}-legend-past`).style.display = isPF ? "inline-flex" : "none";
		document.getElementById(`${this.prefix}-legend-future`).style.display = isPF ? "inline-flex" : "none";

		this.update_ims();
	}

	change_scene(scene_id) {
		this.base_im = scene_id;
		this.cur_frame = 0;

		if (this.input_img)
			this.input_img.src = `assets/${this.prefix}/blurry/${scene_id}_${this.method}.png`;

		this.loadVideos();
		this.update_ims();
	}

	loadVideos() {
		const scene = this.base_im;
		const method = this.method;

		const reconPath = `assets/${this.prefix}/videos/${scene}/${method}/Ours.mp4`;
		const tracksPath = `assets/${this.prefix}/tracks/${scene}/${method}/Ours.mp4`;

		if (this.video_recon) {
			this.video_recon.src = reconPath;
			this.video_recon.load();
			this.video_recon.currentTime = 0;
			this.video_recon.pause();
		}

		if (this.video_tracks) {
			this.video_tracks.src = tracksPath;
			this.video_tracks.load();
			this.video_tracks.currentTime = 0;
			this.video_tracks.pause();
		}
	}

	toggle_play_pause() {
		const btn = document.getElementById(`${this.prefix}-play-pause-btn`);
		const icon = document.getElementById(`${this.prefix}-play-pause-icon`);
		const label = btn.querySelector("span:last-child");

		const isPlaying = !this.video_recon.paused;

		if (isPlaying) {
			this.video_recon.pause();
			this.video_tracks.pause();
			icon.className = "fas fa-play";
			label.textContent = "Play";
		} else {
			this.video_recon.playbackRate = this.playback_speed;
			this.video_tracks.playbackRate = this.playback_speed;
			this.video_recon.play();
			this.video_tracks.play();
			icon.className = "fas fa-pause";
			label.textContent = "Pause";
		}
	}

	change_frame(idx) {
		this.stop_anim();
		this.cur_frame = parseInt(idx);

		const norm = this.cur_frame / (this.max_idx - 1);
		if (this.video_recon?.duration) this.video_recon.currentTime = norm * this.video_recon.duration;
		if (this.video_tracks?.duration) this.video_tracks.currentTime = norm * this.video_tracks.duration;

		const icon = document.getElementById(`${this.prefix}-play-pause-icon`);
		const label = document.getElementById(`${this.prefix}-play-pause-btn`).querySelector("span:last-child");
		icon.className = "fas fa-play";
		label.textContent = "Play";

		this.applyGlowEffect();
	}

	update_ims() {
		this.change_frame(this.cur_frame);
	}

	next_frame() {
		if (this.cur_frame === this.max_idx - 1) this.anim_dir = -1;
		if (this.cur_frame === 0) this.anim_dir = 1;
		this.change_frame(this.cur_frame + this.anim_dir);
	}

	cycle_frames(delay) {
		this.stop_anim();
		this.interval_id = setInterval(() => this.next_frame(), delay);
	}

	stop_anim() {
		if (this.interval_id) clearInterval(this.interval_id);
		this.interval_id = null;
	}

	// GLOW SUPPORT
	getTemporalRegion(frameIndex) {
		if (frameIndex <= 4) return 'past';
		if (frameIndex >= 12) return 'future';
		return 'present';
	}

	applyGlowEffect() {
		if (this.method !== 'pastfuture') {
			this.removeAllGlows();
			return;
		}

		const region = this.getTemporalRegion(this.cur_frame);
		this.removeAllGlows();
		if (this.video_recon) this.video_recon.classList.add(`video-glow-${region}`);
		if (this.video_tracks) this.video_tracks.classList.add(`video-glow-${region}`);
	}

	removeAllGlows() {
		const classes = ['video-glow-past', 'video-glow-present', 'video-glow-future'];
		this.video_recon?.classList.remove(...classes);
		this.video_tracks?.classList.remove(...classes);
	}
}
