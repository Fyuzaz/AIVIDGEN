/**
 * CropSelector — Interactive 9:16 crop overlay on a video preview image.
 * Allows dragging to position the crop area. Returns normalized (0-1) center coords.
 */
class CropSelector {
    constructor(containerEl, imageUrl, videoWidth, videoHeight) {
        this.container = containerEl;
        this.videoWidth = videoWidth;
        this.videoHeight = videoHeight;
        this.isDragging = false;
        this.dragOffsetX = 0;
        this.dragOffsetY = 0;

        // Clear container
        this.container.innerHTML = '';

        // Wrapper for relative positioning
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'crop-wrapper';
        this.container.appendChild(this.wrapper);

        // Preview image
        this.image = document.createElement('img');
        this.image.src = imageUrl;
        this.image.className = 'crop-image';
        this.image.draggable = false;
        this.wrapper.appendChild(this.image);

        // Overlay canvas (dark areas outside crop)
        this.overlay = document.createElement('canvas');
        this.overlay.className = 'crop-overlay';
        this.wrapper.appendChild(this.overlay);

        // Crop rectangle
        this.cropBox = document.createElement('div');
        this.cropBox.className = 'crop-box';
        this.wrapper.appendChild(this.cropBox);

        // Crop label
        this.cropLabel = document.createElement('div');
        this.cropLabel.className = 'crop-label';
        this.cropLabel.textContent = '9:16';
        this.cropBox.appendChild(this.cropLabel);

        // Wait for image to load to calculate dimensions
        this.image.onload = () => this._init();
        if (this.image.complete) this._init();
    }

    _init() {
        const imgRect = this.image.getBoundingClientRect();
        const wrapperRect = this.wrapper.getBoundingClientRect();

        this.displayW = this.image.offsetWidth;
        this.displayH = this.image.offsetHeight;

        // Set wrapper size to match image
        this.wrapper.style.width = this.displayW + 'px';
        this.wrapper.style.height = this.displayH + 'px';

        // Setup overlay canvas
        this.overlay.width = this.displayW;
        this.overlay.height = this.displayH;

        // Calculate 9:16 crop box size in display coordinates
        const targetRatio = 9 / 16;
        const imageRatio = this.displayW / this.displayH;

        if (imageRatio > targetRatio) {
            // Image is wider — crop width fits within height
            this.cropH = this.displayH;
            this.cropW = Math.round(this.displayH * targetRatio);
        } else {
            // Image is taller — crop height fits within width
            this.cropW = this.displayW;
            this.cropH = Math.round(this.displayW / targetRatio);
        }

        // Initial position: centered
        this.cropX = Math.round((this.displayW - this.cropW) / 2);
        this.cropY = Math.round((this.displayH - this.cropH) / 2);

        this._updateCropBox();
        this._drawOverlay();
        this._bindEvents();
    }

    _updateCropBox() {
        this.cropBox.style.left = this.cropX + 'px';
        this.cropBox.style.top = this.cropY + 'px';
        this.cropBox.style.width = this.cropW + 'px';
        this.cropBox.style.height = this.cropH + 'px';
    }

    _drawOverlay() {
        const ctx = this.overlay.getContext('2d');
        ctx.clearRect(0, 0, this.displayW, this.displayH);

        // Semi-transparent dark overlay
        ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
        ctx.fillRect(0, 0, this.displayW, this.displayH);

        // Clear the crop area (transparent)
        ctx.clearRect(this.cropX, this.cropY, this.cropW, this.cropH);
    }

    _bindEvents() {
        // Mouse events
        this.cropBox.addEventListener('mousedown', (e) => this._startDrag(e));
        document.addEventListener('mousemove', (e) => this._onDrag(e));
        document.addEventListener('mouseup', () => this._endDrag());

        // Touch events
        this.cropBox.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this._startDrag(e.touches[0]);
        });
        document.addEventListener('touchmove', (e) => {
            if (this.isDragging) {
                e.preventDefault();
                this._onDrag(e.touches[0]);
            }
        }, { passive: false });
        document.addEventListener('touchend', () => this._endDrag());
    }

    _startDrag(e) {
        this.isDragging = true;
        const rect = this.cropBox.getBoundingClientRect();
        this.dragOffsetX = e.clientX - rect.left;
        this.dragOffsetY = e.clientY - rect.top;
        this.cropBox.style.cursor = 'grabbing';
    }

    _onDrag(e) {
        if (!this.isDragging) return;

        const wrapperRect = this.wrapper.getBoundingClientRect();
        let newX = e.clientX - wrapperRect.left - this.dragOffsetX;
        let newY = e.clientY - wrapperRect.top - this.dragOffsetY;

        // Clamp within bounds
        newX = Math.max(0, Math.min(newX, this.displayW - this.cropW));
        newY = Math.max(0, Math.min(newY, this.displayH - this.cropH));

        this.cropX = newX;
        this.cropY = newY;

        this._updateCropBox();
        this._drawOverlay();
    }

    _endDrag() {
        this.isDragging = false;
        this.cropBox.style.cursor = 'grab';
    }

    /**
     * Returns the normalized center coordinates (0-1) of the crop area.
     */
    getNormalizedCenter() {
        const centerX = (this.cropX + this.cropW / 2) / this.displayW;
        const centerY = (this.cropY + this.cropH / 2) / this.displayH;
        return { x: centerX, y: centerY };
    }
}
