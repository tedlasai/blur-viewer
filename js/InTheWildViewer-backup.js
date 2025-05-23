class InTheWildViewer {
    constructor() {
        this.prefix = 'wild';
        this.max_idx = 12;
        this.n_scenes = 8;
        this.playback_speed = 0.2;

        this.num_videos = 6;
        
        this.cur_frame = 0;
        this.base_im = '0000';
        this.method = 'present';
        this.interval_id = null;
        this.anim_dir = 1;

        this.ours_recon = document.getElementById(`${this.prefix}-ours`);
        this.ours_tracks = document.getElementById(`${this.prefix}-ours-tracks`);
        this.motionetr_recon = document.getElementById(`${this.prefix}-motionetr`);
        this.motionetr_tracks = document.getElementById(`${this.prefix}-motionetr-tracks`);
        this.jin_recon = document.getElementById(`${this.prefix}-jin`);
        this.jin_tracks = document.getElementById(`${this.prefix}-jin-tracks`);
        this.input_img = document.getElementById(`${this.prefix}-input`);

        this.video_elements = [this.ours_recon, this.ours_tracks, this.motionetr_recon, this.motionetr_tracks, this.jin_recon, this.jin_tracks];

        this.initSceneSelector();
        this.initVideos();
        this.initSliderSync();
        //this.initialize_slider_sync();
        this.sync_other_videos();
    }

    /* Scene selector from SimulatedViewer */
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

    /* Video management from ComplexViewer */
    initVideos() {
        for (let i = 0; i < this.num_videos; i++) {
            const video = document.getElementById(`${this.prefix}-output-${i}`);
            if (video) {
                video.pause();
                video.currentTime = 0;
                this.video_elements.push(video);
            }
        }
    }

    /* Slider sync combining both versions */
    initSliderSync() {
        if (!this.ours_recon) return;
        const slider = document.getElementById(`${this.prefix}_frame_control`);
        if (!slider) return;
        this.ours_recon.addEventListener('loadedmetadata', () => {
            this.ours_recon.addEventListener('timeupdate', () => {
                if (!this.ours_recon.duration) return;
                console.log("Current time: ", this.ours_recon.currentTime);
                console.log("Duration: ", this.ours_recon.duration);
                const progress = this.ours_recon.currentTime / this.ours_recon.duration;

                const newVal = Math.round(progress * (parseInt(slider.max) || (this.max_idx)));
                console.log("Intermediate new val: ", progress * (parseInt(slider.max) || (this.max_idx)));

                console.log("Slider value changed to: ", newVal);
                console.log("Current slider value: ", slider.value);
                if (parseInt(slider.value) !== newVal) {
                    slider.value = newVal;
                    this.cur_frame = newVal;
                    this.applyGlowEffect();
                }
            });
        });
    }

    /* Legacy slider sync for other videos */
    // initialize_slider_sync() {
    //     const master = this.video_elements[0];
    //     const slider = document.getElementById(`${this.prefix}_frame_control`);
    //     if (!master || !slider) return;
    //     master.addEventListener("timeupdate", () => {
    //         if (!master.duration) return;
    //         const progress = master.currentTime / master.duration;
    //         const newVal = Math.round(progress * parseInt(slider.max));
    //         slider.value = newVal;
    //         this.cur_frame = newVal;
    //         this.applyGlowEffect();
    //     });
    // }

    /* Keep all videos in sync */
    sync_other_videos() {
        const master = this.video_elements[0];
        const others = this.video_elements.slice(1);
        master.addEventListener("timeupdate", () => {
            if (!master.duration) return;
            const time = master.currentTime;
            others.forEach(video => {
                if (Math.abs(video.currentTime - time) > 0.03) {
                    video.currentTime = time;
                }
            });
        });
    }

    /* Update frame on slider change */
    change_frame(idx) {
        this.stop_anim();
        this.cur_frame = parseInt(idx);
        const norm = this.cur_frame / (this.max_idx);
        console.log("Video duration: ", this.video_elements[0].duration);
        console.log("this.cur_frame: ", this.cur_frame);
        console.log("norm: ", norm);
        this.video_elements.forEach(video => {
            console.log("Video duration: ", video.duration);
            if (video && video.duration) {
                video.currentTime = norm * video.duration;
                console.log("Video currentTime: ", video.currentTime);

            }

        });
        this.applyGlowEffect();
        this.resetPlayButton();
    }

    /* Scene change handler */
    change_scene(scene_id) {
        this.base_im = scene_id;
        this.cur_frame = 0;
        if (this.input_img) {
            this.input_img.src = `assets/${this.prefix}/blurry/${scene_id}_${this.method}.png`;
        }
        this.loadVideos();
        this.change_frame(0);
    }

    /* Load video sources */
    loadVideos() {
        const scene = this.base_im;
        const method = this.method;
        const ours_reconPath = `assets/${this.prefix}/videos/${scene}/${method}/Ours.mp4`;
        const ours_tracksPath = `assets/${this.prefix}/tracks/${scene}/${method}/Ours.mp4`;
        const motionetr_reconPath = `assets/${this.prefix}/videos/${scene}/${method}/MotionETR.mp4`;
        const motionetr_tracksPath = `assets/${this.prefix}/tracks/${scene}/${method}/MotionETR.mp4`;
        const jin_reconPath = `assets/${this.prefix}/videos/${scene}/${method}/Jin.mp4`;
        const jin_tracksPath = `assets/${this.prefix}/tracks/${scene}/${method}/Jin.mp4`;




        this.ours_recon.src = ours_reconPath;
        this.ours_recon.load();
        this.ours_recon.currentTime = 0;
        this.ours_recon.pause();

        this.ours_tracks.src = ours_tracksPath;
        this.ours_tracks.load();
        this.ours_tracks.currentTime = 0;
        this.ours_tracks.pause();

        this.motionetr_recon.src = motionetr_reconPath;
        this.motionetr_recon.load();
        this.motionetr_recon.currentTime = 0;
        this.motionetr_recon.pause();

        this.motionetr_tracks.src = motionetr_tracksPath;
        this.motionetr_tracks.load();
        this.motionetr_tracks.currentTime = 0;
        this.motionetr_tracks.pause();

        this.jin_recon.src = jin_reconPath;
        this.jin_recon.load();
        this.jin_recon.currentTime = 0;
        this.jin_recon.pause();

        this.jin_tracks.src = jin_tracksPath;
        this.jin_tracks.load();
        this.jin_tracks.currentTime = 0;
        this.jin_tracks.pause();
    }

    /* Play/pause toggle */
    toggle_play_pause() {
        const isPlaying = this.video_elements.some(v => !v.paused);
        this.video_elements.forEach(v => {
            if (isPlaying) {
                v.pause();
            } else {
                v.playbackRate = this.playback_speed;
                //v.play();
            }
        });
        this.updatePlayButton(!isPlaying);
    }

    /* Update UI play button */
    updatePlayButton(isPlaying) {
        const btn = document.getElementById(`${this.prefix}-play-pause-btn`);
        const icon = document.getElementById(`${this.prefix}-play-pause-icon`);
        const label = btn.querySelector("span:last-child");
        if (isPlaying) {
            icon.className = "fas fa-pause";
            label.textContent = "Pause";
        } else {
            icon.className = "fas fa-play";
            label.textContent = "Play";
        }
    }

    /* Reset play button to initial state */
    resetPlayButton() {
        const icon = document.getElementById(`${this.prefix}-play-pause-icon`);
        const label = document.getElementById(`${this.prefix}-play-pause-btn`).querySelector("span:last-child");
        icon.className = "fas fa-play";
        label.textContent = "Play";
    }

    /* Animation controls */
    next_frame() {
        if (this.cur_frame === this.max_idx - 1) this.anim_dir = -1;
        if (this.cur_frame === 0) this.anim_dir = 1;
        this.change_frame(this.cur_frame + this.anim_dir);
    }
    cycle_frames(delay = 200) {
        this.stop_anim();
        this.interval_id = setInterval(() => this.next_frame(), delay);
    }
    stop_anim() {
        if (this.interval_id) clearInterval(this.interval_id);
        this.interval_id = null;
    }

    /* Glow effect for pastfuture method */
    applyGlowEffect() {
        const classes = ['video-glow-past', 'video-glow-present', 'video-glow-future'];
        this.video_elements.forEach(video => video.classList.remove(...classes));
        if (this.method !== 'pastfuture') return;

        const region = this.getTemporalRegion(this.cur_frame);
        this.video_elements.forEach(video => video.classList.add(`video-glow-${region}`));
    }
    getTemporalRegion(frameIndex) {
        if (frameIndex <= 4) return 'past';
        if (frameIndex >= 12) return 'future';
        return 'present';
    }

    /* Method switcher */
    set_method(name) {
        this.method = name;
        this.loadVideos();
        if (this.input_img) {
            this.input_img.src = `assets/${this.prefix}/blurry/${this.base_im}_${name}.png`;
        }
        document.querySelectorAll(`#${this.prefix}-method-toggle button`).forEach(btn => {
            btn.classList.toggle("is-info", btn.dataset.method === name);
            btn.classList.toggle("is-light", btn.dataset.method !== name);
        });
        const slider = document.getElementById(`${this.prefix}_frame_control`);
        if (slider) slider.classList.toggle("pastfuture", name === "pastfuture");
        ['past', 'future'].forEach(region => {
            const el = document.getElementById(`${this.prefix}-legend-${region}`);
            if (el) el.style.display = name === "pastfuture" ? "inline-flex" : "none";
        });
        this.change_frame(this.cur_frame);
    }
}
