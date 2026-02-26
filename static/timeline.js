/**
 * TimelineEditor — Video player with interactive timeline for marking segments.
 * Users can mark start/end points to create segments for shorts generation.
 */
class TimelineEditor {
    constructor(containerEl, videoUrl, duration, captions) {
        this.container = containerEl;
        this.duration = duration;
        this.captions = captions || [];
        this.segments = [];
        this.markStart = null;

        this.container.innerHTML = '';
        this._buildUI(videoUrl);
        this._bindEvents();
    }

    _buildUI(videoUrl) {
        // Video player
        this.video = document.createElement('video');
        this.video.src = videoUrl;
        this.video.controls = true;
        this.video.className = 'timeline-video';
        this.video.preload = 'auto';
        this.container.appendChild(this.video);

        // Timeline bar area
        const timelineArea = document.createElement('div');
        timelineArea.className = 'timeline-area';
        this.container.appendChild(timelineArea);

        // Timeline bar
        this.timelineBar = document.createElement('div');
        this.timelineBar.className = 'timeline-bar';
        timelineArea.appendChild(this.timelineBar);

        // Progress indicator
        this.timelineProgress = document.createElement('div');
        this.timelineProgress.className = 'timeline-progress';
        this.timelineBar.appendChild(this.timelineProgress);

        // Playhead
        this.playhead = document.createElement('div');
        this.playhead.className = 'timeline-playhead';
        this.timelineBar.appendChild(this.playhead);

        // Segment markers layer
        this.segmentLayer = document.createElement('div');
        this.segmentLayer.className = 'timeline-segments-layer';
        this.timelineBar.appendChild(this.segmentLayer);

        // Caption markers
        if (this.captions.length > 0) {
            this._renderCaptionMarkers();
        }

        // Time display
        const timeRow = document.createElement('div');
        timeRow.className = 'timeline-time-row';
        timelineArea.appendChild(timeRow);

        this.currentTimeDisplay = document.createElement('span');
        this.currentTimeDisplay.className = 'time-display';
        this.currentTimeDisplay.textContent = '0:00';
        timeRow.appendChild(this.currentTimeDisplay);

        this.durationDisplay = document.createElement('span');
        this.durationDisplay.className = 'time-display';
        this.durationDisplay.textContent = this._formatTime(this.duration);
        timeRow.appendChild(this.durationDisplay);

        // Controls
        const controls = document.createElement('div');
        controls.className = 'timeline-controls';
        this.container.appendChild(controls);

        // Mark Start button
        this.markStartBtn = document.createElement('button');
        this.markStartBtn.className = 'btn-mark btn-mark-start';
        this.markStartBtn.innerHTML = '🟢 Marcar Início';
        controls.appendChild(this.markStartBtn);

        // Mark End button
        this.markEndBtn = document.createElement('button');
        this.markEndBtn.className = 'btn-mark btn-mark-end';
        this.markEndBtn.innerHTML = '🔴 Marcar Fim';
        this.markEndBtn.disabled = true;
        controls.appendChild(this.markEndBtn);

        // Current marking indicator
        this.markIndicator = document.createElement('span');
        this.markIndicator.className = 'mark-indicator hidden';
        controls.appendChild(this.markIndicator);

        // Segments list
        this.segmentsList = document.createElement('div');
        this.segmentsList.className = 'segments-list';
        this.container.appendChild(this.segmentsList);

        this._updateSegmentsList();
    }

    _bindEvents() {
        // Video time update → move playhead
        this.video.addEventListener('timeupdate', () => {
            const pct = (this.video.currentTime / this.duration) * 100;
            this.playhead.style.left = `${pct}%`;
            this.timelineProgress.style.width = `${pct}%`;
            this.currentTimeDisplay.textContent = this._formatTime(this.video.currentTime);
        });

        // Click on timeline → seek
        this.timelineBar.addEventListener('click', (e) => {
            const rect = this.timelineBar.getBoundingClientRect();
            const pct = (e.clientX - rect.left) / rect.width;
            this.video.currentTime = pct * this.duration;
        });

        // Mark Start
        this.markStartBtn.addEventListener('click', () => {
            this.markStart = this.video.currentTime;
            this.markEndBtn.disabled = false;
            this.markIndicator.classList.remove('hidden');
            this.markIndicator.textContent = `⏱ Início: ${this._formatTime(this.markStart)}`;
            this.markStartBtn.innerHTML = `🟢 Início: ${this._formatTime(this.markStart)}`;
        });

        // Mark End
        this.markEndBtn.addEventListener('click', () => {
            if (this.markStart === null) return;

            const end = this.video.currentTime;
            const start = this.markStart;

            if (end <= start) {
                alert('O fim deve ser após o início!');
                return;
            }

            if (end - start < 3) {
                alert('O segmento deve ter pelo menos 3 segundos!');
                return;
            }

            if (end - start > 90) {
                alert('O segmento deve ter no máximo 90 segundos para shorts!');
                return;
            }

            this.segments.push({ start, end });
            this.markStart = null;
            this.markEndBtn.disabled = true;
            this.markIndicator.classList.add('hidden');
            this.markStartBtn.innerHTML = '🟢 Marcar Início';

            this._updateSegmentsList();
            this._renderSegmentMarkers();
        });
    }

    _renderCaptionMarkers() {
        // Light markers on the timeline for each caption segment
        this.captions.forEach(cap => {
            const startPct = (cap.start / this.duration) * 100;
            const widthPct = ((cap.end - cap.start) / this.duration) * 100;
            const marker = document.createElement('div');
            marker.className = 'timeline-caption-marker';
            marker.style.left = `${startPct}%`;
            marker.style.width = `${Math.max(0.3, widthPct)}%`;
            marker.title = cap.text;
            this.timelineBar.appendChild(marker);
        });
    }

    _renderSegmentMarkers() {
        this.segmentLayer.innerHTML = '';
        this.segments.forEach((seg, i) => {
            const startPct = (seg.start / this.duration) * 100;
            const widthPct = ((seg.end - seg.start) / this.duration) * 100;
            const marker = document.createElement('div');
            marker.className = 'timeline-segment-marker';
            marker.style.left = `${startPct}%`;
            marker.style.width = `${widthPct}%`;

            const label = document.createElement('span');
            label.className = 'segment-marker-label';
            label.textContent = `${i + 1}`;
            marker.appendChild(label);

            // Click to seek to segment start
            marker.addEventListener('click', (e) => {
                e.stopPropagation();
                this.video.currentTime = seg.start;
            });

            this.segmentLayer.appendChild(marker);
        });
    }

    _updateSegmentsList() {
        if (this.segments.length === 0) {
            this.segmentsList.innerHTML = `
                <div class="segments-empty">
                    <p>Nenhum segmento selecionado.</p>
                    <p class="segments-hint">Use o player acima, navegue até o trecho desejado e clique em <strong>"Marcar Início"</strong> e <strong>"Marcar Fim"</strong>.</p>
                </div>
            `;
            return;
        }

        let html = '<div class="segments-header"><h4>📋 Segmentos Selecionados</h4></div>';
        this.segments.forEach((seg, i) => {
            const dur = seg.end - seg.start;
            html += `
                <div class="segment-item" data-index="${i}">
                    <div class="segment-info">
                        <span class="segment-number">${i + 1}</span>
                        <span class="segment-time">${this._formatTime(seg.start)} → ${this._formatTime(seg.end)}</span>
                        <span class="segment-duration">(${dur.toFixed(0)}s)</span>
                    </div>
                    <div class="segment-actions">
                        <button class="btn-segment-play" onclick="timelineEditor.playSegment(${i})" title="Reproduzir">▶</button>
                        <button class="btn-segment-remove" onclick="timelineEditor.removeSegment(${i})" title="Remover">✕</button>
                    </div>
                </div>
            `;
        });
        this.segmentsList.innerHTML = html;
    }

    playSegment(index) {
        const seg = this.segments[index];
        if (!seg) return;
        this.video.currentTime = seg.start;
        this.video.play();

        // Auto-pause at segment end
        const checkEnd = () => {
            if (this.video.currentTime >= seg.end) {
                this.video.pause();
                this.video.removeEventListener('timeupdate', checkEnd);
            }
        };
        this.video.addEventListener('timeupdate', checkEnd);
    }

    removeSegment(index) {
        this.segments.splice(index, 1);
        this._updateSegmentsList();
        this._renderSegmentMarkers();
    }

    getSegments() {
        return this.segments.map(s => ({ start: s.start, end: s.end }));
    }

    _formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s.toString().padStart(2, '0')}`;
    }
}
