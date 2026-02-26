/**
 * TrendingBrowser — Loads and displays trending podcast videos from YouTube.
 * Click a card to select it and fill the URL input on the generator tab.
 */
class TrendingBrowser {
    constructor(containerEl, onSelect) {
        this.container = containerEl;
        this.onSelect = onSelect; // callback(url, title)
        this.videos = [];
        this.loading = false;
    }

    async search(query = 'podcast em alta') {
        if (this.loading) return;
        this.loading = true;
        this._showLoading();

        try {
            const resp = await fetch(`/trending?q=${encodeURIComponent(query)}`);
            if (!resp.ok) throw new Error('Falha na busca');
            const data = await resp.json();
            this.videos = data.videos || [];
            this._render();
        } catch (err) {
            console.error(err);
            this.container.innerHTML = `
                <div class="trending-error">
                    <p>❌ Erro ao buscar vídeos: ${err.message}</p>
                    <button class="btn-ghost" onclick="trendingBrowser.search()">Tentar novamente</button>
                </div>
            `;
        } finally {
            this.loading = false;
        }
    }

    _showLoading() {
        this.container.innerHTML = `
            <div class="trending-loading">
                <div class="loader-ring"></div>
                <p>Buscando podcasts em alta...</p>
            </div>
        `;
    }

    _render() {
        if (this.videos.length === 0) {
            this.container.innerHTML = '<div class="trending-empty"><p>Nenhum vídeo encontrado.</p></div>';
            return;
        }

        let html = '<div class="trending-grid">';
        for (const video of this.videos) {
            html += `
                <div class="trending-card" data-url="${this._escapeHtml(video.url)}" data-title="${this._escapeHtml(video.title)}">
                    <div class="trending-thumb">
                        <img src="${video.thumbnail}" alt="" loading="lazy">
                        ${video.duration ? `<span class="trending-duration">${video.duration}</span>` : ''}
                    </div>
                    <div class="trending-info">
                        <h4 class="trending-title">${this._escapeHtml(video.title)}</h4>
                        <div class="trending-meta">
                            ${video.channel ? `<span class="trending-channel">${this._escapeHtml(video.channel)}</span>` : ''}
                            ${video.views ? `<span class="trending-views">👁 ${video.views}</span>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }
        html += '</div>';
        this.container.innerHTML = html;

        // Bind click events
        this.container.querySelectorAll('.trending-card').forEach(card => {
            card.addEventListener('click', () => {
                const url = card.dataset.url;
                const title = card.dataset.title;
                this.onSelect(url, title);
            });
        });
    }

    _escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str || '';
        return div.innerHTML;
    }
}
